import argparse
from easydict import EasyDict as edict
from config import cfg_from_file


# ===================================================================
# About visualization

# ===================================================================




# ===================================================================
# About configurations
# Input, Parse, Display and so on
def parse_args(description=None):
    """Parse input (currently intending for config file)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-cfg', '--config', dest='cfg_file', action='append',
                        help='an optional config file', default=None, type=str)

    args = parser.parse_args()
    if args.cfg_file is not None:
        for f in args.cfg_file:
            cfg_from_file(f)

    return args

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(indent_cnt=0)
def print_easydict(inp_dict: edict):
    """Nicely print EasyDict, for checking configurations
    """
    for key, value in inp_dict.items():
        if type(value) is edict or type(value) is dict:
            print('{}{}:'.format(' ' * 2 * print_easydict.indent_cnt, key))
            print_easydict.indent_cnt += 1
            print_easydict(value)
            print_easydict.indent_cnt -= 1
        else:
            print('{}{}: {}'.format(' ' * 2 * print_easydict.indent_cnt, key, value))

# ===================================================================