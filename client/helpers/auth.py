import keyring

from client.globals import config

def store_creds(apiurl, username, password):
    config.set("login", "apiurl", apiurl)
    config.set("login", "username", username)
    keyring.set_password(apiurl, username, password)
    config.set("login", "auto", "on")
    config.write()
    

def read_creds():
    url = config.get("login", "apiurl")
    usn = config.get("login", "username")
    return url, usn, keyring.get_password(url, usn)


def del_creds():
    url = config.get("login", "apiurl")
    usn = config.get("login", "username")
    keyring.delete_password(url, usn)
    config.remove_option("login", "apiurl")
    config.remove_option("login", "username")
    config.set("login", "auto", "off")
    config.write()