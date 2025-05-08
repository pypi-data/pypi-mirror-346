"""
modul with main class
"""
import logging
import os
from copy import deepcopy
from .optsargs import cliparser
from .yavault import VaultData, YamlVault
from .utils import ask_vault_id_passwd, gen_secrets, load_yaml, dump_yaml, VachSummary
from .excs import *

# create summary object to save important infos about every file
summary=VachSummary()

class ChangeVaultPasswd():
  """ class for changing vault passwords
  in files with ansible vault values
  """
  def __init__(self):
    logging.debug("start of the starts")
    self.cliargs=cliparser.parse_args()
    self._set_cliargs_to_myself()

  def __str__(self):
    s=("cliargs", "run")
    l=[f"{k}={v}" for k,v in self.__dict__.items() if (not  k.startswith("_")) and (k not in s) ]
    return " ".join(l)   

  def _set_cliargs_to_myself(self):
    """ set class attributes from parsed opts
    with argparse
    """
    for k,v in vars(self.cliargs).items():
      self.__dict__.update({k:v})

  def read_vault_passwd(self):
    """ read old vault paswords from stdin
    if '-g' option provided generate new vault passwds
    else read new passwords from stdin
    """ 
    # asking for old passwords
    for vid in self.vault_id:
      p=ask_vault_id_passwd(vid)
      VaultData.data.update({vid: p})
    # generate new passwords
    if self.gen_passwd is not None:
      ps=gen_secrets(length=self.gen_passwd, count=len(self.vault_id))
      for c,vid in enumerate(self.vault_id):
        VaultData.data_new.update({vid: ps[c]})
    else:
      for vid in self.vault_id:
        # type new password
        p1=ask_vault_id_passwd(vid, False)
        # retype new password
        p2=ask_vault_id_passwd(vid, False, True)
        if p1!=p2:
          raise ValueError("different passwords for the same vault_id")
        VaultData.data_new.update({vid: p1})

  def _create_new_vault_obj(self, old_vobj):
    """ create vault object with new password 
    """
    new_vobj=YamlVault(use_new=True, vault_id=old_vobj.vault_id, plain_text=old_vobj.plain_text)
    return new_vobj
    

  def _search_for_vault(self, obj, var_path="",deep=0):
    """ searching recursiv in obj for vaults
    """
    if type(obj)==dict:
      for k,v in obj.items():
        #logging.info("deep=%s obj=dict key=%s value=%s value_type=%s(%s)", deep,k,v,type(v),type(v).__name__)
        new_var_path=f"{var_path}:{k}"
        if isinstance(v, (list,dict)):
          self._search_for_vault(v, f"{var_path}:{k}",deep+1)
        elif isinstance(v, (YamlVault)):
          logging.info("++ found vault: vid=%s plain=%s var_path=%s"%( v.vault_id, v.plain_text, new_var_path))
          summary.vault_var(new_var_path)
          obj[k]=self._create_new_vault_obj(v)
    elif type(obj)==list:
      for c,v in enumerate(obj):
        #logging.info("deep=%s obj=list value=%s value_type=%s(%s)", deep,v,type(v),type(v).__name__)
        new_var_path=f"{var_path}[{c}]"
        if isinstance(v, (list,dict)):
          self._search_for_vault(v, f"{var_path}[{c}]",deep+1)
        elif isinstance(v, (YamlVault)):
          logging.info("++ found vault: vid=%s plain=%s var_path=%s"% (v.vault_id, v.plain_text, new_var_path))
          summary.vault_var(new_var_path)
          obj[c]=self._create_new_vault_obj(v)
    elif isinstance(obj, (YamlVault)):
      logging.info("++ found lonely vault: vid=%s plain=%s var_path=" % (obj.vault_id, obj.plain_text))
      obj=self._create_new_vault_obj(obj)
    else:
      #logging.error("something wrong with obj")
      raise TypeError("loaded object is neigher dict,list or yamlvault")
    return obj

  def handle_file(self):
    """ check file (should it be ignored or not)
    load file as yaml
    search for vaults in file
    write file if neccessery
    """
    cur_path=summary.cur_file.path
    #logging.debug("handle path: %s", cur_path)
    logging.debug("start to handle file")
    # ignore check
    if summary.check_dir(self.ign_dir_rgx):
      return
    if summary.check_file(self.ign_file_rgx):
      return
    if not summary.match_file(self.match_file_rgx):
      return
    try:
      #logging.debug("try to load %s as yaml", cur_path)
      logging.debug("try to load file as yaml")
      obj=load_yaml(cur_path)
      logging.debug("loaded obj:%s%s", "\n",obj)
      obj_copy=self._search_for_vault(deepcopy(obj))
      logging.debug("modified obj:%s%s", "\n",obj_copy)
      if self.no_dry:
        if summary.cur_file.vault_vars:
          #logging.info("writing file with vault vars: %s",cur_path)
          logging.info("writing file with vault vars")
          dump_yaml(obj_copy,cur_path)
          summary.written()
    except Exception as exc:
      logging.error("troubles every day with file: %s", exc)
      summary.error(exc)
    else:
      summary.success()


  def run(self):
    """ go through all files founden in positional src arguments 
    in self.wpath. walk recursively through src if it is directory
    add every file to summary
    write at the end summary file
    """
    logging.info("run forest run...")
    logging.debug("about a girl:%s%s", "\n",self) 
    self.read_vault_passwd()
    #VaultData._show()
    for src in self.wpath:
      if os.path.isfile(src):
        logging.info("try to handle file '%s'", src)
        summary.add_new_file(src)
        self.handle_file()
        summary.show_cur()
      elif os.path.isdir(src):
        logging.info("try to handle directory '%s'", src)
        try:
          for walk_dir,_,filenames in os.walk(src):
            for filename in filenames:
              summary.add_new_file(walk_dir+"/"+filename)
              self.handle_file()
              summary.show_cur()
        except:
          logging.error("can't walk through '%s'", src)
          summary.bad_src(src)
      else:
        logging.error("'%s' src doesn't exist", src)
        summary.bad_src(src)
    #summary.add_new_file()
    summary.push()
    summary.summary()
    if not self.no_sum_file:
      summary.write()
    #print(summary)
