"""
- logging configuration
- read configuration
"""
import logging
import os
import re
from .defs import read_vach_cfg
from .utils import VachContext

LOG_DIR=os.path.expanduser('~/log')
LOG_FILE=f"{LOG_DIR}/vach.log"

try:
  os.mkdir(LOG_DIR)
except FileExistsError:
  pass
except Exception as exc:
  print(f"ERROR [__init__.py] can't create log directory '{LOG_DIR}': ({type(exc).__name__}) {exc}")
  pass

# add some custom atributes to log records
old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.wfile = VachContext.path
    return record
logging.setLogRecordFactory(record_factory)

# define plain Filter
class PlainLogFilter(logging.Filter):
  def filter(self, record):
    record.msg=re.sub(r"plain=(.+?) ", r"plain=*** ", record.msg)
    return True

plf=PlainLogFilter()


lfh=logging.FileHandler(LOG_FILE)
lfh.setLevel(logging.DEBUG)
lfh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(process)d %(module)s %(funcName)s %(wfile)s] %(message)s"))
lfh.addFilter(plf)
lsh=logging.StreamHandler()
lsh.setLevel(logging.INFO)
lsh.setFormatter(logging.Formatter("%(levelname)s [%(module)s %(funcName)s %(wfile)s] %(message)s"))
logging.basicConfig(level=logging.DEBUG, handlers=[lsh, lfh])

read_vach_cfg()
