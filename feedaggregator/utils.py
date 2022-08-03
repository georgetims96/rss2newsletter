from datetime import datetime
from time import mktime

def st_to_dt(st):
  return datetime.fromtimestamp(mktime(st))