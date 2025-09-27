import time
from lib2to3.pgen2 import driver
import sys
from bs4 import BeautifulSoup
from rich.progress import track, Progress
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By



e_options = webdriver.EdgeOptions()
def str2sec(s:str):
    td=s.split(':')
    t = 0
    for idx, tx in enumerate(reversed(td)):
        t = t + int(tx) * (60 ** (idx))
    return t
class Watch:
    def __init__(self,cookies=None,bvlist=None):
        e_options = webdriver.EdgeOptions()
        # e_options.add_argument("--headless")
        e_options.add_argument("--window-size=1920,1080")
        self.bvlist=bvlist
        if not cookies:raise AttributeError("不登录你刷个屁等级")
        self.driver = webdriver.Edge(options=e_options)
        self.driver.get("https://www.bilibili.com/")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        if self.driver.find_elements(by=By.CLASS_NAME, value="header-login-entry"):
            raise AttributeError("登录出问题了，重新走一边流程吧")

    def run(self):
        for bv in self.bvlist:
            self.driver.get(bv)
            time.sleep(2)
            ta = 0
            tc = 0
            html = BeautifulSoup(self.driver.page_source, features="html.parser")
            for td in html.find_all(attrs={"class": "bpx-player-ctrl-time-duration"}):
                ta = str2sec(td.text)
            for td in html.find_all(attrs={"class": "bpx-player-ctrl-time-current"}):
                tc = str2sec(td.text)
            print("wait {}s".format(ta - tc))
            with Progress() as progress:
                task2 = progress.add_task(f"[green]Processing...{self.driver.title}", total=ta - tc + 10)
                while not progress.finished:
                    progress.update(task2, advance=1)
                    time.sleep(1)
            if bv==self.bvlist[0]:
                webdriver.ActionChains(self.driver).send_keys("w").perform()
                i=0
                while self.driver.current_url == bv:
                    time.sleep(1)
                    if i >12:
                        break
                    i=i+1
                self.driver.find_element(by=By.CLASS_NAME, value="left-con").click()
                self.driver.find_element(by=By.CLASS_NAME, value="bi-btn").click()