#!/bin/env python

import os
import json
import libtmux
import argparse
import sys

global home
home = os.path.expanduser('~')

parser = argparse.ArgumentParser(description='Sets up your Tmux sessions.')
parser.add_argument('--python', '-p', action='store_true')
parser.add_argument('--session', '-s')
args = parser.parse_args()


## Utility functions
def getSessionOptions(srvData):
    sessionOptions = [n['name'].lower() for n in srvData if n['default'] == False]
    return sessionOptions


def tmux(command):
    os.system(f'tmux {command}')

def decideLayout(paneCount):
    if paneCount == 3:
        return 'main-vertical'
    elif paneCount == 4:
        return 'tiled'
    else:
        return 'even-horizontal'

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
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(f'{directory}/session_data.json', 'r') as f:
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
Possible options are {getSessionOptions(serverData)}""")
            #setupSession(serverObj, serverData)
    else:
        setupServer(serverObj, serverData)
