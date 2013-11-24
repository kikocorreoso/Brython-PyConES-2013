__stdout__=getattr(doc,"$stdout")
__stderr__=getattr(doc,"$stderr")

stdout = getattr(doc,"$stdout")
stderr = getattr(doc,"$stderr")

modules=__BRYTHON__.modules

has_local_storage=__BRYTHON__.has_local_storage
has_json=__BRYTHON__.has_json
version_info=__BRYTHON__.version_info
path=__BRYTHON__.path
builtin_module_names=['posix']

byteorder='little'
maxsize=9007199254740992   #largest integer..
maxunicode=1114111

platform="brython"
warnoptions=[]

class flag_class:
  def __init__(self):
      self.debug=0
      self.inspect=0
      self.interactive=0
      self.optimize=0
      self.dont_write_bytecode=0
      self.no_user_site=0
      self.no_site=0
      self.ignore_environment=0
      self.verbose=0
      self.bytes_warning=0
      self.quiet=0
      self.hash_randomization=1

flags=flag_class()

