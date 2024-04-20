import os
import sys
import json

yes = {"yes", "y", "ye", ""}
no = {"no", "n"}

print("Creating new Release!")
print("---------------------")

with open("Syncogram/config.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    CURRENT_VERSION = data["APP"]["VERSION"]

NEW_VERSION = str(input(f"Specify the new version ({CURRENT_VERSION}): "))
print("---------------------")
print(f"New version: {NEW_VERSION}")
data["APP"]["VERSION"] = NEW_VERSION
print("---------------------")
choice = input("Start merge? yes/no: ").lower()


def merge():
    with open("Syncogram/config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.system("git add .")
    os.system(f"""git commit -am "Version {NEW_VERSION}" """)
    os.system("git push")
    os.system("git checkout master")
    os.system("git merge dev")


if choice in yes:
    merge()
elif choice in no:
    sys.exit()
else:
    sys.stdout.write("Please respond with 'yes' or 'no'")
