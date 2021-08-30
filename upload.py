import subprocess, sys
import pandas as pd
import datetime
import json
import os

class Df2md:

  def __init__(self, title: str, df: pd.DataFrame):
    self.df = df
    self.yyyymmdd = self.datestring()
    self.p = "./jekyll/_posts/" + self.yyyymmdd + f"-{title}.md"

  def datestring(self):
    dt_now = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    yyyymmdd = dt_now.strftime('%Y-%m-%d')
    
    return yyyymmdd

  def save2md(self):
    markdown_text = f"""---
layout: post
---

### sub title

{self.df.to_html()}

"""
    with open(self.p, "w", encoding="utf-8") as f:
      f.write(markdown_text)
      
    while not os.path.isfile(self.p):
      sleep(1)

class Upload:

  def run(self):
    
    p = "C:/Users/frog7/python/hall/jekyll"

    try:
      proc = subprocess.run('bundle exec jekyll build', cwd=p, shell=True)
      print(proc.returncode)
    except subprocess.CalledProcessError:
      print("a jekyll processing failed")
      sys.exit(1)

    try:
      proc = subprocess.run('surge _site/ brown-jellyfish.surge.sh', cwd=p, shell=True)
    except subprocess.CalledProcessError:
      print("a surge processing failed")
      sys.exit(1)

if __name__=='__main__':

  p = "./works/overnight_2021-08-28.json"
  with open(p, "r", encoding="utf-8") as f:
    read_dic = json.load(f)
    
  lst = [v[:3] + v[4:] for v in read_dic.values()]
  col = ["No", "machine", "date", "hits", "next", "total", "last"]
  df = pd.DataFrame(lst, columns=col)
  # print(df)

  m = MdDf("over-test", df)
  m.save2md()
  Upload().run()
