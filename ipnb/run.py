import sys
import argparse
import os.path

import utils

try:
    import pudb as debugger
except:
    import pdb as debugger

if sys.hexversion > 0x03000000:
   def run_function(source, filename):
        exec(compile(source, filename, "exec"),globals(),globals())
else:
   eval(compile("""\
def run_function(source, filename):
    exec compile(source, filename, "exec") in globals(), globals()
""", "<exec_function>", "exec"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d,--debug', dest='debug', default=False, action='store_true', help="debug")
    parser.add_argument('-s,--show-source', dest='source', default=False, action='store_true', help="print the source file (with line number) to stderr")
    parser.add_argument('command', nargs=argparse.REMAINDER)

    opts = parser.parse_args()
    args = opts.command

    nb_file = args[0]
    
    if not os.path.exists(nb_file):
        print('Error: %s does not exist' % nb_file)
        sys.exit(1)

    sys.argv = args
    sys.path[0] = os.path.dirname(nb_file)
    os.chdir(sys.path[0])

    source = utils.get_notebook_source(nb_file)
    if opts.debug:
        source = """ 
try:
    import pudb as debugger
except:
    import pdb as debugger

debugger.set_trace()
""" + source

        import tempfile
        f = tempfile.NamedTemporaryFile()
        f.write(source)
        f.seek(0)
        try:
            run_function(source, f.name)
        except SystemExit:
            pass
        except:
            debugger.pm()
    else:
        if opts.source:
            for i, line in enumerate(source.split('\n')):
                sys.stderr.write("%2d %s\n" % (i+1,line))
        run_function(source, nb_file)

if __name__ == '__main__':
    main()
