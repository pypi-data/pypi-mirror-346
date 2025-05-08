"""
module to handle default and config files values
"""
import logging
import os
import re
import configparser
import sys

# config file
CFG_DEFAULT_SECTION='main'
CFG_FILE='vach.cfg'
CFG_DIR=os.path.expanduser('~/.vach/')
CFG_SEARCH_DIRS=('.', os.path.expanduser('~'), CFG_DIR)
# paswd
PASSWD_LEN_MIN=12
PASSWD_LEN_MAX=64
PASSWD_LEN_DEF=20


class VachDefs:
  """ class with default config values
  implements also funtions for checking 
  values from config files
  """
  wpath=['.']
  vault_id=['vid']
  passwd_length=PASSWD_LEN_DEF
  match_file_regex='.+'
  ignore_dir_regex='/?\.git/?'
  ignore_file_regex=None

  @classmethod
  def _show(cls):
    for k,v in cls.__dict__.items():
      if k.startswith('_') :
        continue
      logging.debug("defs: %s=%s", k, v)

  @classmethod
  def _check_wpath(cls, value):
    """ build working path list
    from comma separated string
    """
    logging.debug("wpath config check..")
    cls.wpath=list(set([os.path.expanduser(p) for p in re.split(',\s*', value) if p]))
    if not cls.wpath:
      logging.error("wpath value in config is empty or make no sense")
      return 1
    return 0

  @classmethod
  def _check_vault_id(cls, value):
    """ build vault id list
    from comma separated string
    """
    logging.debug("vault_id config check..")
    cls.vault_id=list(set([v for v in re.split(',\s*', value) if v]))
    if not cls.vault_id:
      logging.error("vault_id value in config is empty or make no sense")
      return 1
    return 0

  @classmethod
  def _check_passwd_length(cls, value):
    """ check value of passwd_length
    """
    logging.debug("passwd_length config check..")
    try:
      value=int(value)
    except:
      logging.error("can't cast passwd_length from config to int. please provide only integers (%s..%s)",PASSWD_LEN_MIN,PASSWD_LEN_MAX)
      return 1
    if isinstance(value, (int)):
      if value<PASSWD_LEN_MIN or value>PASSWD_LEN_MAX:
        logging.error("wrong passwd_length in config. please provide only integers %s..%s",PASSWD_LEN_MIN,PASSWD_LEN_MAX)
        return 1
    return 0
    

def read_vach_cfg():
  """ read vach config file(s)
  and set default values in VachDefs class
  """
  #VachDefs.show()
  def_sec=CFG_DEFAULT_SECTION
  cfg=configparser.ConfigParser()
  cfg.SECTRE=re.compile(r"\[ *(?P<header>[^]]+?) *\]")
  try:
    ff=cfg.read([f"{d}/{CFG_FILE}" for d in reversed(CFG_SEARCH_DIRS)])
  except Exception as exc:
    logging.error("reading config files: %s: %s:", type(exc).__name__, exc)
    return 
  if not ff:
    logging.info("no config files found")
    return
  logging.info("found config files: %s", ff)
  if not cfg.has_section(def_sec):
    logging.warning("no '%s' section found in cfg. ignore cfg", def_sec)
    return
  logging.debug("items in cfg  %s section: %s", def_sec, cfg.items(def_sec))
  for k,v in cfg.items(def_sec):
    if hasattr(VachDefs, f"_check_{k}"):
      check_func=getattr(VachDefs, f"_check_{k}")
      if check_func(v):
        logging.error("some trouble with your config values in %s",ff)
        sys.exit(1)
    else: 
      setattr(VachDefs, k, v)
  VachDefs._show()


  
