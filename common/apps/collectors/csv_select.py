import sqlite3
import pandas as pd

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select_one_from_csv(csv_url,query):
  # load data
  df = pd.read_csv(csv_url,parse_dates=True)
  # strip whitespace from headers
  # df.columns = df.columns.str.strip()
  con = sqlite3.connect(":memory:")
  con.row_factory = dict_factory

  # drop data into database table named csv
  df.to_sql("csv", con)
  cur = con.cursor()
  cur.execute(query)
  row = cur.fetchone()
  con.close()
  return row

