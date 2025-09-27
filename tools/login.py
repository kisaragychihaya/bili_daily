import json
import os
import time
from tools.str2enc import str2enc,enc2str
from selenium.webdriver.common.by import By
from selenium import webdriver
def login(save=""):
    driver = webdriver.Edge()
    driver.get("https://www.bilibili.com/")
    if save and os.path.exists(save):
        with open(save, "rb") as f:
            cookies=json.loads(enc2str(f.read()))
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    time.sleep(1)
    butt=driver.find_elements(by=By.CLASS_NAME, value="header-login-entry")
    if butt:butt[0].click()
    while True:
        if driver.find_elements(by=By.CLASS_NAME, value="header-login-entry"):
            time.sleep(1)
        else:
            break
    cookies = driver.get_cookies()
    ret = []
    for cookie in cookies:
        d = {}
        d.update(dict(cookie))
        ret.append(d)
    with open(save, 'wb') as f:
        s=json.dumps(ret)
        f.write(str2enc(s))
    return driver