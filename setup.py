from setuptools import setup

setup(
    name='tmux-starter',
    version='0.1',
    author='Josua Kehlenbach',
    description='Quickly setup tmux sessions with predefined panes and window configurations ',
    install_requires=[
        'libtmux'
    ],
    scripts=['tmux-starter'],
    data_files=[('share/doc/tmux-starter', ['LICENSE', 'session_data.json.example'])],
    license="MIT",
    url="https://github.com/Bergschrat1/tmux-starter"
)
