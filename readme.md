
# BGMBot
A straightforward script to expose and loop opus files through a discord bot using the next discord library (the thing after discordpy). Uses slash commands and a nice Select UI.

## Installation
1. Install `libffi`, `libnacl`, `python3-dev` for your preferred system
    - For those using `apt`, use `apt install libffi-dev libnacl-dev python3-dev`
    - N.B. Since Ubuntu doesn't have 3.8+ in the default repos, you'll need to add one and install the relevant `python3.x-dev` where x is the version number you installed
    - e.g. If I installed `python-3.10`, I would use the command `apt install libffi-dev libnacl-dev python3.10-dev`

2. Create your venv however you like, ensure you have python3.8+
    - If using the above python version, make sure you use the correct python version when creating your venv
    - e.g. `python-3.10 -m venv env` is how I create my venv

3. Enter your Virtual Environment (e.g. `source ./env/bin/activate` for Linux | `env\Scripts\activate.bat` for Windows)

4. Run `pip install -r requirements.txt`

5. Create a dir called `bgms/` in the project root and fill it with opus files using the naming scheme `example_bgm.opus`

## Running
1. `export KEY={YOUR_KEY}`

2. `python main.py`


# License
Do whatever, I don't really care.
