# General
Project for automatic changing ansible vault passwords in yaml files with ansible vault strings. Use *vach* script wchich will be automatic installed by:
```
pip install vach
```
*vach* requieres some python packages:
- *ansible-vault*
- *yaml*
- *argcomplete*

*vach* don't overwrite files with vaults on default. only with *-n* option files with vault strings will be modified.
*vach* uses python logging to write messages to stdout

# Usage

```
vach [-h] [-i VID] [-g [LENGTH]] [-n] [--no-sum-file] [--tb] [-m REGEX] [-d REGEX] [-f REGEX] [-V] [PATH ...]
```
positional arguments:
- search in  *PATH* for ansible vault strings and change vault passsword. 
  - Default: *.*. 
  - python `os.walk` used for recursively file search in direct

options:
```
  -h, --help            show this help message and exit
  -i VID, --vault-id VID
                        vault ids which password should be changed (default:
                        ['vid'])
  -g [LENGTH], --gen-passwd [LENGTH]
                        generate passwords for new vault ids. if no LENGTH is
                        provided use default length (default: None)
                        default password length: 20
  -n, --no-dry          no dry mode. files will be really written (default:
                        False)
  --no-sum-file         don't write summary json file in $HOME (default:
                        False)
  --tb                  show traceback on exceptions (default: False)
  -m REGEX, --match-file REGEX
                        handle only files that match REGEX (default: .+)
                        REGEX is case sensitive
  -d REGEX, --ignore-dir REGEX
                        ignore directories that match REGEX (default:
                        /?\.git/?)
                        REGEX is case sensitive
  -f REGEX, --ignore-files REGEX
                        ignore files that match REGEX (default: None)
                        REGEX is case sensitive
  -V, --version         show program's version number and exit
```

## Usage examples
- show only changes in *test_dir* directory recursively and in files *file_1*, *file_2*. use *vid_1* vault-id
```
vach -i vid_1 test_dir file_1 file_2
```
- overwrite files with vaults (no-dry mode)
```
vach -i vid_1 test_dir file_1 file_2 --no-dry
```
- handle only filenames that match some regex
```
vach -i vid_1 test_dir file_1 file_2 -m "\.ya?ml"
```
- ignore directories that match some regex
```
vach -i vid_1 test_dir file_1 file_2 -d "dist|build"
```
- ignore filenames that match some regex
```
vach -i vid_1 test_dir file_1 file_2 -f "\.json$"
```

# Default values/Konfiguration
Konfig files in ini format can be used to set some default values for *vach* script. Konfig files can be placed in:
- ./vach.cfg
- $HOME/vach.cfg
- $HOME/.vach/vach.cfg 

*vach.cfg* example:
```
[main]

passwd_length = 23
wpath = ~/vach_dir,/opt/test_dir,file_1
vault_id = vid1,vid2
match_file_regex=my?.regex
ignore_dir_regex=some_dir_regex
ignore_file_regex=ign_file_rg[Xx]
```
*main* section in *vach.cfg* is required

# summary file
*vach* writes on default json summary file in the same directory. Example for a summary file (*vach_summary_20250424213256.json*):
```
{
  "general": {
    "all": 36,
    "success": 3,
    "vault": 2,
    "written": 0,
    "ignored": 30,
    "len_bad_srcs": 0,
    "bad_srcs": [],
    "error": 3
  },
  "files": [
    {
      "path": "/home/firusik/vach_dir/myobject.yaml",
      "succeeded": true,
      "written": false,
      "ignored": false,
      "errors": [],
      "vault_vars": []
    },
    {
      "path": "/home/firusik/vach_dir/vach_test_file_2.yml",
      "succeeded": true,
      "written": false,
      "ignored": false,
      "errors": [],
      "vault_vars": [
        ":oxak[1]:p",
        ":she:lost:control[2]",
        ":she:lost:begun",
        ":passwd"
      ]
    },
    {
      "path": "/home/firusik/vach_dir/vach_error_file.yml",
      "succeeded": false,
      "written": false,
      "ignored": false,
      "errors": [
        "('VaultError', VaultError('decryption of vault failed. exceptions derived from ansible: {Decryption failed (no vault secrets were found that could decrypt)}'))"
      ],
      "vault_vars": []
    },
    {
      "path": "/home/firusik/vach_dir/.git/description",
      "succeeded": false,
      "written": false,
      "ignored": true,
      "errors": [],
      "vault_vars": []
    },
    ...
  ]
}
```
