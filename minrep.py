import pandas as pd
import json
import datetime
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re

class Scrap:

  def get_soup(self, url):

    try: 
      html = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
      print("URLError", e.reason)
      html = "<html></html>"

    soup = BeautifulSoup(html, "lxml")

    return soup

  def get_dfs(self, soup):

    dfs = [pd.DataFrame()]
    if soup.find("table") == None:
      print("get_dfs: a table is not found.")
    else:
      dfs = pd.io.html.read_html(soup.prettify())

    return dfs

if __name__=='__main__':

  kodama = "/埼玉県/児玉郡/"
  isesaki = "/群馬県/伊勢崎市/"
  takasaki = "/群馬県/高崎市/"
  target = takasaki

  srp = Scrap()
  url = "https://min-repo.com/category" + urllib.parse.quote(target)
  soup = srp.get_soup(url)
  
  title_tags = soup.select(".ichiran_title a")
  comments = [tag.text for tag in soup.select(".ichiran_result2")]
  url_tags = [a.get("href")  for a in soup.select(".ichiran_title a")]
  contents = ""
  for title, comment, url in zip(title_tags, comments, url_tags):
    content = "### " + title.text + " "
    soup = srp.get_soup(url)
    dfs = srp.get_dfs(soup)
    prevent = re.sub(" ", "", dfs[0].loc[0, 1])
    all_pay = dfs[0].loc[1, 1]
    avg_pay = dfs[0].loc[2, 1]
    avg_g = dfs[0].loc[3, 1]
    win_rate = dfs[0].loc[4, 1]
    content += prevent + "\n"
    content += f" - 総差枚 {all_pay} 平均差枚 {avg_pay} 平均G数 {avg_g} 勝率 {win_rate}"
    content += "\n" + " - " + comment
    tbl = dfs[1].head(10).to_html()
    contents += content + "\n" + tbl + "<br/>" + "\n"


  markdown_text = f"""---
layout: post
---

# MinRep

{contents}

"""
  dt_now = datetime.datetime.now()
  oneday = datetime.timedelta(days=1)
  if dt_now.hour < 9: dt_now -= oneday
  # dt_now -= oneday
  yyyymmdd = dt_now.strftime('%Y-%m-%d')
  
  area = target.split("/")[2]
  p_m = f"./else/_posts/{yyyymmdd}-minrep-{area}.md"
  with open(p_m, "w", encoding="utf-8") as f:
    f.write(markdown_text)