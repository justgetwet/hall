import subprocess, sys
import pandas as pd
import datetime
from time import sleep
import json
import os
import threading
from nox import DmmCrawl
from upload import Upload, Df2md

def datestring():
  dt_now = datetime.datetime.now()
  oneday = datetime.timedelta(days=1)
  yyyymmdd = dt_now.strftime('%Y-%m-%d')
  
  return yyyymmdd

def crawl_dsk():
  icon_p = "./images/ds_kamisato.png"
  json_p = "./jsons/zerogames.json"
  # json_p = "./jsons/test.json"


  yyyymmdd = datestring()
  work_p = f"./works/overnight_{yyyymmdd}.json"
    
  with open(json_p, "r", encoding="utf-8") as f:
    read_dic = json.load(f)
  # print(read_dic)
  
  crawl = DmmCrawl()
  proc = crawl.openDmm()
  crawl.clickHall(icon_p)
  works = {}
  for key, item in read_dic.items():
    dic = crawl.machine(int(key), item)
    works.update(dic)

	# 確認用
  read_json = json.dumps(works, ensure_ascii=False)
  with open(work_p, "w", encoding="utf-8") as f:
    f.write(read_json)

  proc.terminate()
  
  # works = {2: ["madoka", "2021-07-07", "まどか☆", "0", "0", "0", "0"]}
  lst = [[key, *item] for key, item in works.items()]
  col = ["No", "machine", "date", "title", "hits", "next", "total", "last"]
  df = pd.DataFrame(lst, columns=col)
  dm = Df2md("over-night", df.drop("title", axis=1))
  dm.save2md()
  Upload().run()

	
  

def waitmonitor():
  crawl = DmmCrawl()
  crawl.clickwait()


if __name__=='__main__':

  mainprocess = threading.Thread(target=crawl_dsk)
  # subprocess = threading.Thread(target=waitmonitor)
  
  mainprocess.start()
  # subprocess.start()


  # work_json = nox
  # df = work_json
  # df.loc[] = []
  # lst <- marge <- df
  # zerogame_json = dic <- lst

  # markdown = zerogame_json

  # bundle exec jekyll build
  # surge _site/ brown-jellyfish.surge.sh
  
  