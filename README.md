# Olympus 1.0

Welcome to Olympus, the all-in one Wizard101 file downloader.
- Olympus is a Python script that downloads all the game's files so you don't have to download them while playing.
- Olympus is based in Python3.11.
- Olympus is licensed under the MIT License.

# Installation
Create a virtual environment and install the requirements:
## Linux
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
## Windows
```bash
python -m venv venv
. venv\Scripts\activate
pip install -r requirements.txt
```
# Usage
To use Olympus, simply run the following command:
## Configure Olympus
* Modify the `config.json` file to your needs:

  * `game_path`: The folder where the your Wizard101's `Data/GameData` folder is. If in windows, use two backslashes `\\` instead of one.
  * `game_version`: It can either be `NA` or `EU`.
  * `download_new_only`: If `true`, Olympus will only download the files that you haven't already downloaded.

## Execute Olympus
```bash
python olympus.py
```
## Download only new files
```bash
python olympus.py --new
```
