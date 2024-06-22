from easydict import EasyDict as edict
import yaml

__C = edict({
    'virus': edict(),
    'student': edict(),
    'teacher': edict(),
    'environment': edict(),
})
cfg = __C   # Consumers get this

# 病毒类型 -----------------------------------------------------
__C.virus.name = 'COVID-19'     # 病毒名称
__C.virus.infect_radius = 2.0   # 传染半径
# -------------------------------------------------------------

# 学生 -----------------------------------------------------
__C.student.e_number = 6        # 在 experimental area 学生数量
__C.student.w_number = 12       # 在 work area 学生数量
__C.student.move_matrix = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]     # 学生移动矩阵
# ---------------------------------------------------------


# 教师 --------------------------------------------------------
__C.teacher.number = 1        # 教师数量, 初始默认在 office
__C.teacher.move_matrix = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]     # 教师移动矩阵
# ------------------------------------------------------------

# 地图设置 -----------------------------------------------------
__C.environment.lab_number = 3      # 实验室数量
__C.environment.lab_length = 40.0     # 实验室尺寸--长
__C.environment.lab_width = 20.0      # 实验室尺寸--宽
# ------------------------------------------------------------


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

