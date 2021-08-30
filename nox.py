import subprocess
from time import sleep
import pathlib
import pyautogui as gui
import win32gui
import pyperclip
from PIL import Image, ImageGrab
import numpy as np
import pandas as pd
import re
import datetime
import json
import sys
import io
import pyocr
import pyocr.builders
from tts import Tts
# from tkdf import TkDf
# sys.stdout = io.TextIOWrapper(
  # sys.stdout.buffer, encoding=sys.stdout.encoding, errors="replace"
# )

class Ocr:
  
  def scan(self, img) -> str:
  
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    
    tool = tools[0]
    txt = tool.image_to_string(
        img,
        lang="jpn+eng",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    return txt

class DmmCrawl(Ocr):
  
  nox_p = "C:\\Program Files (x86)\\Nox\\bin\\Nox.exe"
  tts = Tts()
  
  def openDmm(self) -> subprocess.Popen:
  
    dmm_icon = "./images/dmm.png"
    mypage_icon = "./images/mypage.png"
    dstation_icon = "./images/dstation_kuragano.png"
    dskamisato_icon = "./images/dstation_kamisato.png"
  
    proc = subprocess.Popen(self.nox_p)
    sleep(60)
    
    dmm_pos = None
    while dmm_pos is None:
      dmm_pos = gui.locateCenterOnScreen(dmm_icon, confidence=0.9)
      sleep(5)
    gui.click(dmm_pos)
    sleep(10)

    mypage_pos = None
    while mypage_pos is None:
      mypage_pos = gui.locateCenterOnScreen(mypage_icon, confidence=0.9)
      sleep(5)
    gui.click(mypage_pos)
    sleep(5)
    
    return proc

  def clickHall(sefl, icon_path: str) -> None:
  
    p = pathlib.Path(icon_path)
    if not p.exists():
      print("icon path does not exists.")
      return
    sleep(5)
    ds_pos = None
    while ds_pos is None:
      ds_pos = gui.locateCenterOnScreen(icon_path, confidence=0.9)
      sleep(5)
    gui.click(ds_pos)
    sleep(5)
  
  def truning_col(self, img):
    img_arr = np.asarray(img)
    img_cpy = img_arr.copy()
    for i in range(3):
      img_cpy[:,:,i] = 255 - img_cpy[:,:,i]
    img_new = Image.fromarray(np.uint8(img_cpy))
    
    return(img_new)
    
  def ocr_process(self, img):
  
    title_rec = (5, 212, 300, 250)
    hits_rec = (200, 340, 275, 400)
    continue_rec = (200, 410, 275, 470)
    games_rec = (200, 550, 275, 610)
    prv_rec = (340, 625, 415, 685)
    
    title_crop = img.crop(title_rec)
    hits_crop = img.crop(hits_rec)
    continue_crop = img.crop(continue_rec)
    games_crop = img.crop(games_rec)
    prv_crop = img.crop(prv_rec)

    trn_title_crop = self.truning_col(title_crop)

    title = self.scan(trn_title_crop)
    hits = self.scan(hits_crop)
    continues = self.scan(continue_crop)
    games = self.scan(games_crop)
    prvGames = self.scan(prv_crop)

    title = re.sub(",", "", title)
    
    return title, hits, continues, games, prvGames

  def machine(self, no: int, machine: str):
  
    data_icon = "./images/data_kokai.png"
    search_icon = "./images/search_no.png"
    star_icon = "./images/yellow_star.png"
    daino_icon = "./images/dai_no.png"
    x_icon = "./images/x.png"
    img_p = "./im.png"
    
    data_pos = None
    while data_pos is None:
      data_pos = gui.locateCenterOnScreen(data_icon, confidence=0.9)
      sleep(3)
    gui.click(data_pos)
    sleep(5)
  
    search_pos = None
    while search_pos is None:
      search_pos = gui.locateCenterOnScreen(search_icon, confidence=0.9)
      sleep(3)
    gui.click(search_pos)
    sleep(5)
    # machine_no = no
    pyperclip.copy(no)
    gui.hotkey("ctrl", "v")
    sleep(1)
    gui.hotkey("return")
    sleep(3)
    
    daino_pos = None
    while daino_pos is None:
      sleep(3)
      daino_pos = gui.locateCenterOnScreen(daino_icon, confidence=0.9)

    star_pos = None
    while star_pos is None:
      sleep(3)
      star_pos = gui.locateCenterOnScreen(star_icon, confidence=0.9)
    
    sleep(1)
    x, y = star_pos
    gui.moveTo(x + 100, y + 500)
    sleep(1)
    gui.dragRel(0, -450, duration=3, button='left')
    sleep(3)
    handle = win32gui.FindWindow(None, 'NoxPlayer')
    rect = win32gui.GetWindowRect(handle)
    img = ImageGrab.grab(rect)
    tpl = self.ocr_process(img)
    dt_now = datetime.datetime.now()
    dt = dt_now.strftime('%m/%d %H:%M')
    dic = {no: [machine, dt] + list(tpl)}
    
    # self.tts.talk(f"No. {no} processing completed.")

    x_pos = None
    while x_pos is None:
      x_pos = gui.locateCenterOnScreen(x_icon, confidence=0.9)
      sleep(3)
    gui.click(x_pos)
    sleep(3)
    
    return dic

  def waitdialog(self):
    wait_icon = "./images/wait.png"
    count = 0
    wait_pos = None
    while wait_pos is None:
      wait_pos = gui.locateCenterOnScreen(wait_icon, confidence=0.9)
      sleep(3)
      count += 1
      if count == 200: # 10 minute
        print("click wait-dialog processing is timeout.")
        break
    if wait_pos:
      gui.click(wait_pos)
    print("click wait-dialog processing completed.")
    

# def is_num(self, str_num):
  # try:
    # float(str_num)
  # except ValueError:
    # return False
  # else:
    # return True

if __name__=='__main__':

  img = Image.open("./im.png")
  print(img.size)

  crawl = DmmCrawl()
  ret = crawl.ocr_process(img)
  print(ret)

  # dsKuragano_icon = "./images/dstation_kuragano.png"
  # p = "./ds.json"
  # with open(p, "r", encoding="utf-8") as f:
    # read_dic = json.load(f)
  # print(read_dic)
  
  # crawl = DmmCrawl()
  # proc = crawl.openDmm()
  # crawl.clickHall(dsKuragano_icon)
  # sleep(5)
  # works = {}
  # for key, item in read_dic.items():
    # dic = crawl.machine(int(key), item)
    # works.update(dic)
  # proc.terminate()
  # print(works)
  
  # dt_now = datetime.datetime.now()
  # dt_day = dt_now.day
  # if dt_now.hour < 9: dt_day -= 1
  # yyyymmdd = dt_now.strftime('%Y-%m-') + str(dt_day).rjust(2, "0")
  
  # read_json = json.dumps(works, ensure_ascii=False)
  # p_w = f"./ds_works_{yyyymmdd}.json"
  # with open(p_w, "w", encoding="utf-8") as f:
    # f.write(read_json)
  
