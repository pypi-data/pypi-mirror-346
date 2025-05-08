# modul with exceptions

class VaultError(Exception):
  """ used for decode/encode 
  vault errors
  """

class NoYamlError(Exception):
  """ used if file is no 
  yaml with dict,list or single
  vault values
  """
