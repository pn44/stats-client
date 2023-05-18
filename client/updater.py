import os
import random
from tkinter import messagebox

import requests

GH_API_RELEASES = "https://api.github.com/repos/{user}/{repo}/releases/latest"
USER = "pn44"
REPO = "stats-client"


def vstr_to_tup(string):
    return tuple(map(int, string.split('.')))


def is_latest(vcurr: tuple, vlat: tuple) -> bool:
    return vcurr >= vlat


def gh_get_version(user: str, repo: str) -> tuple:
    response = requests.get(GH_API_RELEASES.format(user=user, repo=repo))
    vstr = response.json()["tag_name"][1:]
    return vstr_to_tup(vstr)

def gh_get_installer(user: str, repo: str, asset_no: int = 0) -> tuple:
    response = requests.get(GH_API_RELEASES.format(user=user, repo=repo))
    return response.json()["assets"][asset_no]["browser_download_url"]


def main(current_version):
    cv = vstr_to_tup(current_version)
    lv = gh_get_version(USER, REPO)
    if not is_latest(cv, lv):
        messagebox.showinfo("Update Available", "There is an update a"
        "vailable, contact admin to get updated.")          


if __name__=="__main__":
    main()
    
