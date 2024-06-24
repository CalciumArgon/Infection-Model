import argparse
from easydict import EasyDict as edict
from config import cfg_from_file
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# ===================================================================
# About visualization
rect_coords = [ # 顺序 E W T O M Vacation
    [(11, 11), (11, 31), (51, 31), (51, 11)],   # Experiment
    [(11, 0), (11, 10), (51, 10), (51, 0)],   # Work
    [(52, 11), (52, 20), (62, 20), (62, 11)],   # Toilet
    [(0, 0), (0, 10), (10, 10), (10, 0)],   # Office
    [(0, 11), (0, 31), (10, 31), (10, 11)],   # Meeting
    [(52, 21), (52, 31), (62, 31), (62, 21)],   #  Vacation
]
area_names = ['Experiment', 'Work', 'Toilet', 'Office', 'Meeting', 'Vacation']

def draw_rectangles(total_num, color_values):
    fig, axs = plt.subplots(total_num//2 + (total_num%2), 2, figsize=(10, 5*total_num//2))

    # Normalize the color_values to range between 0 and 1
    # norms = [mcolors.Normalize(vmin=min(color_values[i]), vmax=max(color_values[i])) for i in range(len(color_values))]
    norm = mcolors.Normalize(vmin=min([min(sublist) for sublist in color_values]), vmax=max([max(sublist) for sublist in color_values]))
    cmap = cm.Reds

    for i, ax in enumerate(axs.flat):
        ax.set_title(f'Day {i*10}')
        if i >= total_num: 
            break
        for j, (coords, text) in enumerate(zip(rect_coords, area_names)):
            rect = patches.Rectangle((coords[0][0], coords[0][1]), 
                                     coords[2][0] - coords[0][0], 
                                     coords[2][1] - coords[0][1], 
                                     linewidth=1, 
                                     edgecolor='r', 
                                     facecolor=cmap(norm(color_values[i][j])))
            ax.add_patch(rect)
            center_x = (coords[0][0] + coords[2][0]) / 2
            center_y = (coords[0][1] + coords[2][1]) / 2
            ax.text(center_x, center_y, text, fontsize=12, ha='center', va='center')

        ax.set_xlim(0, 65)
        ax.set_ylim(0, 35)
        # 颜色对应数值
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, orientation='vertical')

    return fig, axs
# ===================================================================



# ===================================================================
# About simulation
def dist(stu1, stu2):
    x1, y1 = stu1.experimental_position
    x2, y2 = stu2.experimental_position
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
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
            

if __name__ == '__main__':
    color_value = [0,10, 30, 2, 5, 10]
    mcolors.Normalize(vmin=min(color_value), vmax=max(color_value))
    print(cm.Reds(mcolors.Normalize(vmin=min(color_value), vmax=max(color_value))(color_value)))