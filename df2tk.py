import tkinter as tk
from tkinter import ttk
import pandas as pd
import json
import unicodedata


class Df2tk:

  def __init__(self, df: pd.DataFrame):
    
    self.df = df
    self.root = tk.Tk()
    self.root.title("tk for dataframe")
    w = self.root_width()
    h = self.root_hight()
    if h > 900: h = 900
    nw_x = 600
    nw_y = 50 
    self.root.geometry(f"{w}x{h}+{nw_x}+{nw_y}")

    self.headingcolor = "lightgrey"
    self.alternatecolor = "whitesmoke"
    
    canvas = tk.Canvas(self.root)
    barregion_y = 900
    b_h = self.root_hight()
    if b_h > 900: barregion_y = b_h + 100
    bar = tk.Scrollbar(canvas, orient=tk.VERTICAL)
    bar.pack(side=tk.RIGHT, fill=tk.Y)
    bar.config(command=canvas.yview)
    canvas.config(yscrollcommand=bar.set)
    canvas.config(scrollregion=(0, 0, 0, barregion_y)) # スクロール範囲を設定
    # canvas.config(bg=self.bgcolor)
    canvas.pack(fill=tk.BOTH, expand=True) # tk.BOTH：縦横両方向に対して引き伸ばす
    # Canvasの上にFrameを載せる
    self.Frame = tk.Frame(canvas, bd=5)
    # self.Frame.config(bg=self.bgcolor)
    canvas.create_window((0,0), window=self.Frame, anchor=tk.NW)
    
  def treetable(self):
    tree = ttk.Treeview(self.Frame, height=len(self.df)+1)
    # ★バグ対応を処理

    s = ttk.Style()
    # バグ対応
    def fixed_map(option):
      return [e for e in s.map('Treeview', query_opt=option) if e[:2] != ('!disabled', '!selected')]
    
    s.theme_use("clam")
    s.configure("Treeview.Heading", background=self.headingcolor)
    s.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    
    tree["show"] = "headings"
    cols = tuple(range(1, len(self.df.columns)+1))
    tree['columns'] = cols
    sizes = self.column_sizes()
    for i, col, size in zip(cols, self.df.columns, sizes):
      tree.heading(i, text=f"{col}")
      tree.column(i, width=size+8) # 
    
    lst = [tuple(t)[1:] for t in self.df.itertuples()]
    for i, tpl in enumerate(lst):
      tree.insert("", "end", tags=i, values=tpl)
      if i & 1:
        tree.tag_configure(i, background=self.alternatecolor)
    
    tree.pack(pady=10, padx=10)
    
  def column_sizes(self) -> list:

    def ea_width_count(text):
      count = 0
      for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
          count += 2
        else:
          count += 1
      return count * 8
    
    lst_columns = [[col] + list(self.df[col]) for col in self.df.columns]
    col_sizes = []
    for lst in lst_columns:
      col_sizes.append(max([ea_width_count(str(e)) for e in lst]))

    return col_sizes
    
  def root_width(self):
    sizes = self.column_sizes()
    return sum([s+12 for s in sizes]) + 24
    
  def root_hight(self):
    return len(self.df) * 24 + 24
  
  def run(self):
    self.treetable()
    self.root.mainloop()

if __name__ == '__main__':

  p = "./works/zerogame_2021-08-29.json"
  with open(p, "r", encoding="utf-8") as f:
    read_dic = json.load(f)

  lst = [v for k, v in read_dic.items()]
  # print(lst)
  # read_dic.values()
  col = ["No", "machine", "date", "title", "hits", "next", "total", "last"]
  df = pd.DataFrame(lst, columns=col)
  
  # merge_p = "./works/zerogame_2021-08-29.json"

  # merge_d = {k: list(row) for k, row in df.iterrows()}
  # merge_json = json.dumps(merge_d, ensure_ascii=False)
  # with open(merge_p, "w", encoding="utf-8") as f:
  #   f.write(merge_json)

  t = Df2tk(df)
  t.run()
