"""
# достаём все строки для перевода 
pybabel extract Syncogram/ -o Syncogram/locales/base.pot 
# вносим переводы в base.pot!!! и продолжаем
pybabel init -D base -i Syncogram/locales/base.pot -l ru_RU -d Syncogram/locales
pybabel compile -D base -l ru_RU -d Syncogram/locales/ -i Syncogram/locales/ru_RU/LC_MESSAGES/base.po
pybabel update -D base -i Syncogram/locales/base.pot -d Syncogram/locales
"""
import os
import sys
import shutil

yes = {"yes", "y", "ye", ""}
no = {"no", "n"}

WORK_DIR = os.path.abspath(os.path.curdir)
pot = WORK_DIR + "/Syncogram/locales/base.pot"

if os.path.isfile(pot):
    shutil.copy(pot, pot + ".old")


os.system("pybabel extract Syncogram -o Syncogram/locales/base.pot")
os.system("code Syncogram/locales/base.pot")

choice = input("Переведите локали и нажмите y/n: ")

if choice in yes:
    os.system("pybabel init -D base -i Syncogram/locales/base.pot -l ru_RU -d Syncogram/locales")
    os.system("pybabel compile -D base -l ru_RU -d Syncogram/locales/ -i Syncogram/locales/ru_RU/LC_MESSAGES/base.po")
elif choice in no:
    sys.exit()
else:
    sys.stdout.write("Please respond with 'yes' or 'no'")
