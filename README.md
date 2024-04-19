# Syncogram
The application allows you to quickly transfer your channels, saved messages to another telegram account.

![GitHub License](https://img.shields.io/github/license/pwd491/syncogram)
![GitHub Release](https://img.shields.io/github/v/release/pwd491/Syncogram?display_name=release&label=latest-release)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/pwd491/syncogram/.github%2Fworkflows%2Frelease.yml)


![Preview of Telegram Desktop][preview_image]

[preview_image]: ./docs/assets/preview.jpg "Preview of Syncogram Application"

# Installation
Fortunately, you can use [binary files](https://github.com/pwd491/syncogram/releases). If you don't want using binaries, you can build or execute your own application.

### Steps:
1. `git clone https://github.com/pwd491/Syncogram.git`
2. `cd Syncogram`
3. `python -m venv venv`
4. `venv/Scripts/activate` if **Windows** or `source venv\bin\activate` **MacOS** & **Linux**
5. `pip install -r requirements.txt`
6. You need get your own **API_ID** and **API_HASH**, login to [https://my.telegram.org/auth](https://my.telegram.org/auth).
7. Create **environments.py** file into `./Syncogram/sourcefiles/telegram/` and paste your **API** data like `API_ID=***` `API_HASH=***`.
8. **Build** or **Execute** *application.py* and enjoy :)

# Features
* Syncing first name, last name and biography.
# Support Languages
* English
* Russian

# Contacts
[Telegram](https://t.me/@sergeydegtyar)