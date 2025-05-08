"""
parse command line arguments

"""

import argparse
import argcomplete
from importlib.metadata import version
#from .yavault import VaultData
from .defs import VachDefs, PASSWD_LEN_MIN, PASSWD_LEN_MAX


cliparser=argparse.ArgumentParser(
                    prog='vach',
                    description='change vault password in yaml files with ansible vault strings',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                    epilog='be carefull with this prog. make backup bevor changing or track your changes with some version control prog')

# positional arguments files or directories
cliparser.add_argument('wpath',
                      nargs='*',
                      metavar="DIR_OR_FILE",
                      help='search in DIR for yaml files with ansible vault strings or in FILE for vault strings',
                      # TODO. default=['.']
                      default=VachDefs.wpath)
# provide vault ids
cliparser.add_argument('-i', '--vault-id',
                      action='append',
                      dest='vault_id',
                      metavar='VID',
                      help='vault ids which password should be changed',
                      type=str,
                      # TODO: no default,
                      default=VachDefs.vault_id,
                      # TODO: required=True
                      required=False)
# generate password ?
cliparser.add_argument('-g', '--gen-passwd',
                      dest='gen_passwd',
                      nargs='?',
                      help='generate passwords for new vault ids.\nif no LENGTH is provided use default length',
                      default=None,
                      const=VachDefs.passwd_length,
                      type=int,
                      metavar="LENGTH",
                      choices=list(range(PASSWD_LEN_MIN, PASSWD_LEN_MAX)))
# no dry mode
cliparser.add_argument('-n', '--no-dry',
                        help='no dry mode. files will be really written',
                        action='store_true')

# don't write summary file 
cliparser.add_argument('--no-sum-file',
                        help='don\'t write summary json file in $HOME',
                        action='store_true')


cliparser.add_argument('--tb',
                        help='show traceback on exceptions',
                        action='store_true')

# filename regex
cliparser.add_argument('-m', '--match-file',
                        help='handle only files that match REGEX',
                        dest='match_file_rgx',
                        default=VachDefs.match_file_regex,
                        metavar="REGEX")

# ignore directories 
cliparser.add_argument('-d', '--ignore-dir',
                        dest='ign_dir_rgx',
                        help='ignore directories that match REGEX',
                        default=VachDefs.ignore_dir_regex,
                        metavar="REGEX")

# ignore files
cliparser.add_argument('-f', '--ignore-files',
                        dest='ign_file_rgx',
                        help='ignore files that match REGEX',
                        default=VachDefs.ignore_file_regex,
                        metavar="REGEX")
# version
cliparser.add_argument('-V', '--version', 
                        action='version',
                        version=version('vach'))

argcomplete.autocomplete(cliparser)

