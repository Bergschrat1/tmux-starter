#!/bin/env python

import os
import json
import libtmux
import argparse
import sys
import logging


global home

parser = argparse.ArgumentParser(description='Sets up your Tmux sessions.')
parser.add_argument('--python', '-p', action='store_true')
parser.add_argument('--session', '-s')
parser.add_argument('--config', '-c')
parser.add_argument('--debug', '-d', action='store_true')
args = parser.parse_args()

home = os.path.expanduser('~')

if args.debug:
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s = %(levelname)s = %(message)s')
else:
    logging.disable()
logging.debug('Start of programm')

## Utility functions
def getConfigPath():
    logging.debug('Getting config path.')
    if args.config:
        confPath = os.path.expanduser(args.config)
    else:
        confPath = f'{home}/.config/pymux/session_data.json'
    if not os.path.exists(confPath):
        raise FileNotFoundError(f'''Config file not found at {confPath}.
Specify another config path with the --config option''')
    logging.debug(f'Returning config path {confPath}')
    return confPath


def getPossibleSessionNames(srvData):
    sessionOptions = [n['name'].lower() for n in srvData if n['default'] == False]
    return sessionOptions


def decideLayout(paneCount):
    if paneCount == 3:
        return 'main-vertical'
    elif paneCount == 4:
        return 'tiled'
    else:
        return 'even-horizontal'


## Session setup functions
def setupWindow(windowObj, windowData):
    """Sets up all panes in the window"""
    paneCount = int(windowData['panes'])
    layout = decideLayout(paneCount)
    for _ in range(paneCount-1):
        windowObj.split_window(start_directory=home)
    windowObj.select_layout(layout)
    if 'commands' in windowData:
        if len(windowData['commands']) != paneCount:
            raise ValueError('In session_data.json: Same amount of commands as # of panes must be given.')
        for pane, command in zip(windowObj.panes, windowData['commands']):
            if command:
                pane.send_keys(command)
    windowObj.rename_window(windowData['name'])


def setupSession(serverObj, sessionData, sessionIndex):
    """Sets up all windows in the session"""
    sessionName = sessionData['name']
    # check if this is the first session
    if serverObj.get_by_id(f'${sessionIndex}') is not None:
        session = serverObj.get_by_id(f'${sessionIndex}')
        session.rename_session(sessionName)
    else:
        session = serverObj.new_session(session_name=sessionName, 
                                        start_directory=home)

    for windowIndex, windowInfo in enumerate(sessionData['windows']):
        window = session.new_window(start_directory=home)
        setupWindow(window, windowInfo)

    # delete the first window which was create automatically
    session.list_windows()[0].kill_window()

    # select first window
    session.list_windows()[0].select_window()


def setupServer(server, serverData):
    """Sets up all session on the server.
    The sessions can be specified in the config file"""
    for sessionIndex, sessionInfo in enumerate(serverData):
        # setup default sessions
        if sessionInfo['default'] == True:
            setupSession(server, sessionInfo, sessionIndex)


if __name__ == "__main__":
    serverObj = libtmux.Server()
    configPath = getConfigPath()
    with open(configPath, 'r') as f:
        serverData = json.load(f)
    if args.python:
        os.system('setup_python_tmux')
    elif args.session:
        for session in serverData:
            if session['name'].lower() == args.session.lower():
                sessionIndex = len(serverObj.list_sessions())
                setupSession(serverObj, session, sessionIndex)
                sys.exit(1)

        raise ValueError(f"""This session name is undefined.
Possible options are {getPossibleSessionNames(serverData)}""")
    else:
        setupServer(serverObj, serverData)
