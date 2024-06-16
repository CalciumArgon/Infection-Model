from easydict import EasyDict as edict
import yaml

__C = edict({
    'virus': edict(),
    'student': edict(),
    'teacher': edict(),
    'environment': edict(),
})
cfg = __C   # Consumers get this

__C.virus.name = 'COVID-19'
__C.virus.infect_radius = -1.0

__C.student.number = 6
__C.student.move_matrix = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]

__C.teacher.number = 1
__C.teacher.move_matrix = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]

__C.environment.lab_number = 3



#---------------------------------------------------------+
# Helping functions for loading configurations from file  |
# Do Not Touch                                            |
#---------------------------------------------------------+
def _merge_a_into_b(a, b):
    """Merge a into b, covering duplicated elements in b with a."""
    if type(a) is not edict:
        return

    for k, v in a.items():
        if k not in b:
            raise KeyError('{} is not a valid config key'.format(k))
        if type(b[k]) is not type(v):
            print("[Warning] Type mismatch ({} vs. {}) with key: {}".format(type(b[k]), type(v), k))
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except Exception as e:
                print('Error under config key: {}'.format(k))
                print("Error:", e)
                raise
        else:
            b[k] = v

def cfg_from_file(filename):
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.full_load(f))
    _merge_a_into_b(yaml_cfg, __C)

