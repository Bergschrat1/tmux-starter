import os
import json
import libtmux

with open('./session_data.json', 'r') as f:
    session_data = json.load(f)

def tmux(command):
    os.system(f'tmux {command}')

def select_layout(window):

for session in session_data:
    tmux(f"""new-session -d -s "{session['name']}"\
              -n {session['windows'][0]['name']}""")
    for window in session['windows'][1:]:
        tmux(f"""new-window -t "={session['name']}" -n "{window['name']}" """)

