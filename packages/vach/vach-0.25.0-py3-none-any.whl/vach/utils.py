
"""
modul with helper functions
- yaml vault dumpers
- generating password
"""
__all__=["dumps_obj", "load_yaml", "dump_yaml", "gen_secrets", "ask_vault_id_passwd"]

import logging
import os
import re
import string
import secrets
import json
from getpass import getpass
from datetime import datetime
import yaml
from .yavault import get_plain_dumper,get_cipher_dumper,get_loader
from .defs import VachDefs

# decorators
def expand_user(f):
  """ expand user ~ in paths
  """
  def inner(*args):
    #print("len args %s" % len(args))
    new_args=list(args)
    try:
      #print(new_args)
      new_args[-1]=os.path.expanduser(args[-1])
    except:
      pass
    return f(*new_args)
  return inner

def cur_file_not_none(f):
  """ used for functions to check
  for not empty cur_file attribute in 
  VachSummary class 
  """
  def inner(*args):
    inst=args[0]
    if inst.cur_file is not None:
      return f(*args)
    logging.debug("entering the void with yout cur_file in function '%s'", f.__name__)
    return
  return inner

@expand_user
def load_yaml(path):
  """ load yaml file
  params:
    path: str -> path to yaml file
  return:
    y: dict,list -> loaded yaml object
  """
  logging.debug("trying to read %s as yaml", path)
  with open(path) as f:
    y=yaml.load(f, Loader=get_loader())  
  return y
   
def dumps_obj(obj):
  """ return indentet json object
  as string. converting to ascii is disabled

  params: 
    obj: object to dump
  return: 
    s: str -> object as json string
  """
  s=yaml.dump(obj, Dumper=get_plain_dumper(), explicit_end=False, indent=2, default_style='')
  return s

@expand_user
def dump_yaml(obj, path):
  """ write obj to path as yaml
  params:
    obj: yaml -> yaml object to write
    path: str -> path to file where obj will be written
  return: -
  """
  logging.debug("writing yaml object to %s", path)
  with open(path, 'w') as _fw:
    _fw.write(yaml.dump(obj, Dumper=get_cipher_dumper()))

def gen_secrets(**kwargs):
  """ generate password(s)
  or url safe token(s)
  """
  secs=[]
  token=kwargs.get("token", False)
  length=kwargs.get("length", VachDefs.passwd_length)
  count=kwargs.get("count", 1)
  for _ in range(count):
    if not token:
      a = string.ascii_letters + \
          "_" + \
          string.digits
      secs.append(''.join(secrets.choice(a) for i in range(length))) 
    else:
      secs.append(secrets.token_urlsafe())
  return secs

def ask_vault_id_passwd(vid, old=True, retype=False):
  """ function to read vault id(s) and passwords  
  from stdin
  """
  for _ in range(2):
    try:
      if old:
        p=getpass("old password for vault_id=%s: " % vid)
      else:
        if retype:
          p=getpass("retype new password for vault_id=%s: " % vid)
        else:
          p=getpass("new password for vault_id=%s: " % vid)
    except KeyboardInterrupt:
      logging.info("ctrl-c received")
      continue
    p=p.strip()
    if not p:
      logging.warning("invalid or empty password provided")
      continue
    return p
  raise ValueError("invalid or empty password provided")


class VachContext:
  """ context class for logging
  and general purpose.
  """
  path=""

  @classmethod
  def reset(cls):
    """ class method to reset some values
    """
    cls.path=""

class VachFile:
  """ class to keep all informations
  about handled files
  """
  def __init__(self, path):
    self.path=os.path.abspath(path)
    self.name=os.path.basename(path)
    self.directory=os.path.dirname(self.path)
    self.vault_vars=[]
    self.written=False
    self.errors=[]
    self.ignored=False
    self.succeeded=False

  def __str__(self):
    if self.ignored:
      s=f"IGNORED"
    elif self.errors:
      s=f"MAYDAY={self.errors}"
    elif self.vault_vars:
      s=f"VAULT={self.vault_vars}"
    else:
      s=f"UNKNOWN PLEASURES"
    return s

class VachSummary:
  """ class with all informations about
  what file and what variables was written
  """
  def __init__(self):
    self.ignored_dirs=set()
    self.ignored_files=set()
    self.bad_srcs=set()
    self.all_files=[]
    self.cur_file=None
    self.cnt_errors=0
    self.cnt_ignored=0
    self.cnt_success=0
    self.cnt_vaults=0
    self.cnt_written=0

  def __str__(self):
    s="\n-----------------------------------\n"+\
      "\n".join([o.path for o in self.all_files])+\
      "\n-----------------------------------\n"
    return s

  def add_new_file(self, path=None):
    """ add new VachFile object to summary.
    before new Vachfile obj created, old one (if exists)
    will be pushed to list 
    """
    self.push()
    if path:
      self.cur_file=VachFile(path)
      VachContext.path=self.cur_file.path

  @cur_file_not_none
  def written(self):
    """ increment written count if file was written
    """
    self.cnt_written+=1
    self.cur_file.written=True

  @cur_file_not_none
  def push(self):
    """ append cutrrent VachFile to list of Vachfiles
    """
    self.all_files.append(self.cur_file)
    self.cur_file=None
    VachContext.reset()

  @cur_file_not_none
  def success(self):
    """ increment succes counter
    """
    self.cnt_success+=1
    self.cur_file.succeeded=True

  @cur_file_not_none
  def error(self, exc):
    """ increment error counter and save type 
    and message of exception 
    """
    exc_name=type(exc).__name__
    self.cur_file.errors.append((exc_name, exc))
    self.cnt_errors+=1

  @cur_file_not_none
  def ignore_dir(self):
    """ increment ignore dir counter
    and add  dir to list 
    """
    self.ignored_dirs.add(self.cur_file.directory)
    self.cur_file.ignored=True
    self.cnt_ignored+=1
      
  @cur_file_not_none
  def ignore_file(self):
    """ increment ignore file counter
    and add it to list of ignored files
    """
    self.ignored_files.add(self.cur_file.path)
    self.cur_file.ignored=True
    self.cnt_ignored+=1

  def bad_src(self,src):
    """ add bad positional argument to list
    """
    self.bad_srcs.add(src)

  @cur_file_not_none
  def vault_var(self, varname):
    """ incremnt files with vault counter
    andd add all vault vars to list
    """
    if not len(self.cur_file.vault_vars):
      self.cnt_vaults+=1
    self.cur_file.vault_vars.append(varname)

  @cur_file_not_none
  def check_dir(self, rgx=""):
    """ should dir will be ignored if it match rgx
    """
    if rgx:
      if re.search(rgx,self.cur_file.directory):
        self.ignore_dir()
        return True
    return False

  @cur_file_not_none
  def check_file(self, rgx=""):
    """ should file will be ignored if it match rgx
    """
    if rgx:
      if re.search(rgx, self.cur_file.name):
        self.ignore_file()
        return True
    return False

  @cur_file_not_none
  def match_file(self, rgx=""):
    """ go on with file if filename match rgx
    """
    if rgx:
      if re.search(rgx, self.cur_file.name):
        return True
    self.ignore_file()
    return False
  
  def show_cur(self):
    """ show current VachFile object
    """
    logging.info("current file: %s", self.cur_file)

  def write(self):
    """ write json summary file
    in $HOME
    """
    t=datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
    summary_file=f"vach_summary_{t}.json"
    logging.info("writing summary file: %s", summary_file)
    smry={"general": {}, "files": []}
    smry['general'].update({'all': len(self.all_files),
                            'success': self.cnt_success,
                            'vault': self.cnt_vaults,
                            'written': self.cnt_written,
                            'ignored': self.cnt_ignored,
                            'len_bad_srcs': len(self.bad_srcs),
                            'bad_srcs': list(self.bad_srcs),
                            'error': self.cnt_errors})
    for o in self.all_files:
      smry['files'].append({'path': o.path,
                          'succeeded': o.succeeded,
                          'written': o.written,
                          'ignored': o.ignored,
                          'errors': [str(x) for x in o.errors],
                          'vault_vars': list(o.vault_vars)})
    try:
      with open(summary_file, "w") as fw:
        json.dump(smry, fw, indent=2, ensure_ascii=False)
    except Exception as exc:
      logging.error("not possible to write summary file, nevermind (%s)", exc)
 
  

  def summary(self, write_to_file=False ):
    """ logg summary
    """
    logging.info("-----------------------------------------------")
    logging.info("-----------------------------------------------")
    logging.info("all files            : %s", len(self.all_files))
    logging.info("succes files count   : %s", self.cnt_success)
    logging.info("files with vault vars: %s", self.cnt_vaults)
    logging.info("files written        : %s", self.cnt_written)
    if self.cnt_ignored:
      logging.warning("ignored all        : %s", self.cnt_ignored)
      logging.warning("ignored directories: %s", len(self.ignored_dirs))
      logging.warning("ignored files      : %s", len(self.ignored_files))
    if self.cnt_errors:
      logging.error("files with errors  : %s", self.cnt_errors)
    if len(self.bad_srcs):
      logging.error("bad positional srcs: %s", len(self.bad_srcs))
    #logging.info("summary 2: files_with_errors=%s,
