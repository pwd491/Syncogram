# Syncogram
The application allows you to quickly transfer your channels, saved messages to another telegram account.

<sub>All data associated with the account is stored only on your local computer. We do not transfer or store anything.</sub>

![GitHub License](https://img.shields.io/github/license/pwd491/syncogram)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/pwd491/syncogram/latest/total?style=social&label=Download&link=https%3A%2F%2Fgithub.com%2Fpwd491%2FSyncogram%2Freleases)
![GitHub Release](https://img.shields.io/github/v/release/pwd491/Syncogram?display_name=release&label=latest-release)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/pwd491/syncogram/.github%2Fworkflows%2Frelease.yml)


![Preview of Telegram Desktop][preview_image]

[preview_image]: ./docs/assets/preview.jpg "Preview of Syncogram Application"

# Features
* Syncing first name, last name and biography.
* Syncing personal photos with right sequence.
* Syncing favorite messages with right sequence. _(An inefficient algorithm is used)_
* Backup personals chats with all media and pins. _(soon)_
* Syncing all settings. _(soon)_

# Supports
### Operation Systems
* Windows 10+ x64
* Linux (tested on Ubuntu)
* MacOS 13.04 +

### Pythons
* Windows: Python 3.10+
* Linux: Python 3.9+
* MacOS: Python 3.9+
### Languages
* English
* Russian

# Installation Guide
Fortunately, you can use [binary files](https://github.com/pwd491/syncogram/releases). If you don't want using binaries, you can build or execute your own application.


# MacOS trouble
If you're execute binary files on your mac machine, you can have this problem.

![MacOS Error](./docs/assets//macos_error1.jpg)

To fix it go to **Settings** → **Privacy & Security** and submit **Open Anyway** like on picture.

![MacOS Error](./docs/assets//macos_error2.jpg)

If you want to build your own application go to [https://my.telegram.org/auth](https://my.telegram.org/auth) and get **API** data. Be careful and do not transfer this data to strangers, telegram does not allow you to reset this data.

# Build MacOS & Linux
1. `git clone https://github.com/pwd491/Syncogram.git`
2. `cd Syncogram`
3. `python -m venv venv`
4. `source venv\bin\activate`
5. `pip install -r requirements.txt`
6. Create **environments.py** file into `./Syncogram/sourcefiles/telegram/` and paste your **API** data like `API_ID=***` `API_HASH=***`.
7. `source scripts\build.sh`
8. `open craft\Syncogram.app`

# Build Windows
1. `git clone https://github.com/pwd491/Syncogram.git`
2. `cd Syncogram`
3. `python -m venv venv`
4. `venv/Scripts/activate`
5. `pip install -r requirements.txt`
6. Create **environments.py** file into `./Syncogram/sourcefiles/telegram/` and paste your **API** data like `API_ID=***` `API_HASH=***`.
8. `.\craft\Syncogram.exe`


# Execute source code
1. `git clone https://github.com/pwd491/Syncogram.git`
2. `cd Syncogram`
3. `python -m venv venv`
4. `venv/Scripts/activate`
5. `pip install -r requirements.txt`
6. Create **environments.py** file into `./Syncogram/sourcefiles/telegram/` and paste your **API** data like `API_ID=***` `API_HASH=***`.
7. `flet run Syncogram\application.py`

# Contacts
### [Telegram](https://t.me/sergeydegtyar)