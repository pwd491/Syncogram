import os
import sys
import json
import time
import datetime

yes = {"yes", "y", "ye", ""}
no = {"no", "n"}

print("Creating new Release!")
print("---------------------")

with open("Syncogram/config.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    CURRENT_APP_VERSION = data["APP"]["VERSION"]
    CURRENT_DB_VERSION = data["DATABASE"]["VERSION"]

now = datetime.datetime.strftime(datetime.datetime.now(), "%Y.%d.%m")
NEW_APP_VERSION = str(input(f"What is new application version ({CURRENT_APP_VERSION}) -> ({now}): "))

if NEW_APP_VERSION == "":
    NEW_APP_VERSION = now
print("---------------------")
print(f"New application version: {NEW_APP_VERSION}")

NEW_DB_VERSION = str(input(f"What is new Database version ({CURRENT_DB_VERSION}): ")) 
if NEW_DB_VERSION == "":
    NEW_DB_VERSION = CURRENT_DB_VERSION
    print(f"Stay on: {NEW_DB_VERSION}")
else:
    print(f"New database version: {NEW_DB_VERSION}")

data["DATABASE"]["VERSION"] = NEW_DB_VERSION
data["APP"]["VERSION"] = NEW_APP_VERSION
print("---------------------")
choice = input("Start merge? yes/no: ").lower()


def merge():
    with open("Syncogram/config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.system("git add .")
    time.sleep(1)
    os.system(f"""git commit -am "Version {NEW_APP_VERSION}" """)
    time.sleep(1)
    os.system("git push")
    time.sleep(3)
    os.system("git checkout master")
    os.system("git add .")
    os.system(f"""git commit -am "Version {NEW_APP_VERSION}" """)
    os.system("git push")
    time.sleep(3)
    os.system("git merge dev")
    os.system("git push origin master")


if choice in yes:
    merge()
elif choice in no:
    sys.exit()
else:
    sys.stdout.write("Please respond with 'yes' or 'no'")
