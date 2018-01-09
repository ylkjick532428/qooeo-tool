# -*- coding: utf-8 -*-
import os
import sys
import logging
import math
import argparse
import datetime
import time
import urllib.request
# import requests


def get_html(url):
    return ""


def get_html_auth(url, user, pwd, code=""):
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    top_level_url = "http://db.vastio.com/"
    password_mgr.add_password(None, top_level_url, user, pwd)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url)
    if code:
        html = str(response.read().decode(code))
    else:
        html = str(response.read())
    html_count = len(html)
    html = html[2:html_count-1]
    return html

if __name__ == '__main__':
    user="pps"
    passwd="cTW6YAwTXciDm4"
    url = "url"
    html = get_html_auth(url, user, passwd)
    print (html)