# PYTHON_ARGCOMPLETE_OK

import logging
import traceback
import argcomplete
from .vach import ChangeVaultPasswd

def main():
  try:
    a=ChangeVaultPasswd()
    a.run()
  except Exception as exc:
    logging.error("ups.. exception a la '%s' with message: %s", type(exc).__name__, exc)
    if a.tb:
      print(traceback.format_exc())
    return 1
  return 0
