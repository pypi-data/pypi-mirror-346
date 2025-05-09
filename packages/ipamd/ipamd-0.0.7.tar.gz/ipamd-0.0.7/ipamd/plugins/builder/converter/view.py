configure = {
    'type': 'function',
    "schema": 'full',
    "apply": ['persistency_dir']
}
def func(slf, persistency_dir, target_frame=''):
    print('working_dir:', persistency_dir)