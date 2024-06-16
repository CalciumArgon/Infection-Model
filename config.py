from easydict import EasyDict as edict
import yaml

__C = edict({
    'virus': edict(),
    'people': edict(),
    'student': edict(),
})
cfg = __C   # Consumers get this

__C.virus.name = 'COVID-19'
__C.virus.infection_radius = 0.3
__C.virus.infection_rate = 0.8

__C.student.num = 100



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

