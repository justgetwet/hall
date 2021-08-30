import datetime
from time import sleep
import json
import pandas as pd
import threading
from nox import DmmCrawl
from df2tk import Df2tk
from upload import Upload, Df2md

# def datestring():
#   dt_now = datetime.datetime.now()
#   oneday = datetime.timedelta(days=1)
#   if dt_now.hour < 13: dt_now -= oneday
#   yyyymmdd = dt_now.strftime('%Y-%m-%d')
  
#   return yyyymmdd

def datestring(i: int): # i -> 1 or 2
  dt_now = datetime.datetime.now()
  if dt_now.hour < 13:
    dt_now -= datetime.timedelta(days=i)
  yyyymmdd = dt_now.strftime('%Y-%m-%d')
  
  return yyyymmdd

def main():
  icon_p = "./images/ds_kamisato.png"
  # json_p = "./jsons/zerogames.json"
  json_p = "./jsons/test.json"
      
  with open(json_p, "r", encoding="utf-8") as f:
    read_dic = json.load(f)
  # print(read_dic)
  
  crawl = DmmCrawl()
  proc = crawl.openDmm()
  crawl.clickHall(icon_p)
  work_d = {}
  for key, item in read_dic.items():
    dic = crawl.machine(int(key), item)
    work_d.update(dic)

  proc.terminate()
  
  # work_d = {2: ["madoka", "2021-07-07", "まどか☆", "0", "0", "0", "0"]}
  col = ["No", "machine", "date", "title", "hits", "next", "total", "last"]
  
  works = [[key, *item] for key, item in work_d.items()]
  df = pd.DataFrame(works, columns=col)
  this_df = df[df["hits"] == "0"]
  print(this_df)

  # まえのでーた
  last_yyyymmdd = datestring(2)
  last_p = f"./works/zerogame_{last_yyyymmdd}.json"
  # last_p = "./works/zerogame_2021-08-29.json"
  with open(last_p, "r", encoding="utf-8") as f:
      read_dic = json.load(f)
  lasts = [[int(v[0])] + v[1:] for v in read_dic.values()]
  last_df = pd.DataFrame(lasts)

  # まーじ
  lst = []
  for row in this_df.itertuples():
      lst.append(list(row[1:]))
      lst += [list(r[1:]) for r in last_df.itertuples() if r._1 == row.No]
  merge_df = pd.DataFrame(lst, columns=col).sort_values(['No', 'date']).reset_index(drop=True)
  print(merge_df)

  # ほぞん
  yyyymmdd = datestring(1)
  merge_p = f"./works/zerogame_{yyyymmdd}.json"
  
  merge_d = {k: list(row) for k, row in merge_df.iterrows()}
  merge_json = json.dumps(merge_d, ensure_ascii=False)
  with open(merge_p, "w", encoding="utf-8") as f:
    f.write(merge_json)

  # あっぷろーど
  dm = Df2md("zero-game", merge_df.drop("title", axis=1))
  dm.save2md()
  Upload().run()

  # t = Df2tk(merge_df)
  # t.run()

def waitdialog():
  crawl = DmmCrawl()
  crawl.waitdialog()

if __name__=='__main__':

  mainprocess = threading.Thread(target=main)
  # subprocess = threading.Thread(target=waitdialog)
  
  mainprocess.start()
  # subprocess.start()

  # main()