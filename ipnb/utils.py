import json

def get_notebook_source(filename):
    with open(filename, 'r') as f:
        nb = json.load(f)
        code = ''.join(''.join(c['input']) + '\n' for w in nb['worksheets'] for c in w['cells'] \
                       if c['cell_type'] == 'code' and c['language'] == 'python')

        lines = code.split('\n')
        lines = [l for l in lines if not l.startswith('%')]

        return '\n'.join(lines)
