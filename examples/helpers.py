from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
import pandas as pd

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_months(start_date,end_date ):
  strt_dt = datetime.strptime(start_date, '%Y-%m-%d')
  end_dt = datetime.strptime(end_date, '%Y-%m-%d')
  return rrule(MONTHLY, dtstart=strt_dt, until=end_dt).count()



def print_profiles(accounts):

  out = []
  out_l = []

  for a in accounts: 
    out.append({"accounts":a.name, "webproperties":""})
    for w in a.webproperties:
      out.append({"accounts": "", "webproperties":w.name})
  
  display(pd.DataFrame(out,columns= ['accounts','webproperties']))
