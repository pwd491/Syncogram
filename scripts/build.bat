cd Syncogram
flet pack application.py --name "Syncogram" --icon "assets/logo/icns/duck512x512.icns" --add-binary locales:locales --add-data assets:assets --add-data config.json:. --distpath ../craft
cd ../