from nox import DmmCrawl
from tkdf import TkDf
import datetime
import json
import pandas as pd

def datestring():
  dt_now = datetime.datetime.now()
  oneday = datetime.timedelta(days=1)
  if dt_now.hour < 12: dt_now -= oneday
  yyyymmdd = dt_now.strftime('%Y-%m-%d')
  
  return yyyymmdd

if __name__=='__main__':

  # DS倉賀野
  icon_p = "./images/kuragano.png"
  json_p = "./ds_kuragano.json"
  yyyymmdd = datestring()
  work_p = f"./ds_kuragano_works_{yyyymmdd}.json"

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
  proc.terminate()
  
  # works = {2: ["madoka", "date", "0", "0", "0", "0"]}
  lst = [[key, *item] for key, item in works.items()]
  col = ["No", "machine", "date", "初当", "継続", "最終", "前日"]
  df = pd.DataFrame(lst, columns=col)
  
  app = TkDf(df)
  app.geometry("+600+50")
  app.mainloop()
  
  df_0 = df[df["初当"] == "0"]
  
  app_0 = TkDf(df_0)
  app_0.geometry("+700+100")
  app_0.mainloop()
  
  dic = {idx: list(row) for idx, row in df_0.iterrows()}
  read_json = json.dumps(dic, ensure_ascii=False)
  with open(work_p, "w", encoding="utf-8") as f:
    f.write(read_json)