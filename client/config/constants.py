import os

SETTINGS_FILE_NAMES = ["config.ini", os.path.expanduser("~/.amsdc/stats-client/config.ini")]
DEFAULT_SETTINGS = {
    "login": {
        "auto": "off"
    }
}
