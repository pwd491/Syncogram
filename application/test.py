from configparser import ConfigParser

cfg = ConfigParser()
print(cfg.get('Application', "APPLICATION_NAME"))
