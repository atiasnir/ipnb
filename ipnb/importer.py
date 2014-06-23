import sys
import os.path
import imp
import glob

import utils

_folders = {}

if sys.hexversion > 0x03000000:
    def exec_function(source, filename, global_map):
        exec(compile(source, filename, "exec"), global_map)
else:
    eval(compile("""\
def exec_function(source, filename, global_map):
    exec compile(source, filename, "exec") in global_map
""", "<exec_function>", "exec"))

class IPythonNotebookImporter(object):
    def __init__(self):
        for f in sys.path:
            if f in _folders:
                continue
            self._cache_folder(f)

    @staticmethod
    def _cache_folder(f):
        s = set(os.path.basename(x) for x in glob.glob(os.path.join(f,"*.ipynb")))
        if len(s)>0:
            _folders[f] = s

    @staticmethod
    def _extract_notebook_source(name, path):
        filename = os.path.join(path, name + ".ipynb")

        try:
            return utils.get_notebook_source(filename)
        except:
            raise ImportError("Something is wrong")

    def find_module(self, fullname, path=None):
        if path is None:
            for key, notebooks in _folders.viewitems():
                if fullname + ".ipynb" in notebooks:
                    self.path = key
                    return self
              
        if isinstance(path, list):
            for p in path:
                if (p in _folders) and (fullname in _folders[p]):
                    self.path = p
                    return self
        else:
            if (path in _folders) and (fullname in _folders[path]):
                self.path = path
                return self

        return None


    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        source = self._extract_notebook_source(fullname, self.path)
        module = imp.new_module(fullname)
        exec_function(source, fullname, module.__dict__)

        sys.modules[fullname] = module
        self.path = None

        return module

sys.meta_path = [IPythonNotebookImporter()]
