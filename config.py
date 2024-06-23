from easydict import EasyDict as edict
import yaml

__C = edict({
    'virus': edict(),
    'student': edict(),
    'teacher': edict(),
    'environment': edict(),
    'event': edict(),
})
cfg = __C   # Consumers get this

# 病毒类型 -----------------------------------------------------
__C.virus.name = 'COVID-19'     # 病毒名称
__C.virus.infect_radius = 2.0   # 传染半径
# -------------------------------------------------------------

# 学生 -----------------------------------------------------
__C.student.e_number = 10        # 在 experimental area 学生数量
__C.student.w_number = 20        # 在 work area 学生数量
__C.student.init_infect = [1, 2, 4]        # 初始感染人数
__C.student.move_matrix = [ [0.847,0.1,0.05,0.003,0],[0.1,0.847,0.05,0.003,0],[0.6,0.4,0,0,0],[0.24,0.16,0,0.6,0],[0.6,0.4,0,0,0]]    # 学生移动矩阵
__C.student.hidden2infect_day = (2, 4)      # 从 hidden 到 infected 天数范围
__C.student.infect2recover_day = (7, 14)    # 从 infected 到 recovered 天数范围
__C.student.vacation2return_day = (1, 2)    # 从 vacation 到 回实验室天数范围
__C.student.talktive_rate = 0.5    # e人 / 总人数
__C.student.talktive_addition = 20    # 额外的传染能力值
__C.student.immune_rate = 0.5        # 强免疫 / 总人数
__C.student.immune_defence = 20    # 防御能力值
# ---------------------------------------------------------


# 教师 --------------------------------------------------------
__C.teacher.number = 1        # 教师数量, 初始默认在 office
__C.teacher.init_infect = [0, 0, 0]        # 初始感染人数
__C.teacher.move_matrix = [[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0],[0.1,0.1,0.05,0.75,0],[0,0,0,1,0]]    # 教师移动矩阵
__C.teacher.hidden2infect_day = (2, 4)      # 从 hidden 到 infected 天数范围
__C.teacher.infect2recover_day = (7, 14)    # 从 infected 到 recovered 天数范围
__C.teacher.vacation2return_day = (1, 3)    # 从 vacation 到 回实验室天数范围
__C.teacher.talktive_rate = 0.8    # e人 / 总人数
__C.teacher.talktive_addition = 20    # 额外的传染能力值
__C.teacher.immune_rate = 0.8        # 强免疫 / 总人数
__C.teacher.immune_defence = 20    # 防御能力值
# ------------------------------------------------------------


# 地图设置 -----------------------------------------------------
__C.environment.lab_number = 3      # 实验室数量
__C.environment.lab_length = 40.0     # 实验室尺寸--长
__C.environment.lab_width = 20.0      # 实验室尺寸--宽
# ------------------------------------------------------------


# 事件设置 -----------------------------------------------------
__C.event.meeting_rate = [0.01, 0.1, 0.4]   # 每个非会议周期 开会概率 (长度必须与实验室数量相同)
__C.event.meeting_scale = [0.7, 0.3, 0.1]   # 开会人数比例
__C.event.meeting_duration = [90, 60, 20]   # 开会
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

