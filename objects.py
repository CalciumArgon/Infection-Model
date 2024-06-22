import numpy as np

class Virus():
    def __init__(self, name, infect_radius):
        self.name = name
        self.infect_radius = infect_radius
    
    def __str__(self):
        return f"Virus({self.name}, {self.infect_radius})"

    
INFECTION_STATE_NAME = {
    0: 'Normal',
    1: 'Infected',
    2: 'Hidden',
    3: 'Vacation',
    4: 'Recovered',
}

AREA_FULL_NAME = [
    'experimental_areas',
    'work_areas',
    'toilet',
    'office',
    'meeting_room'
]

AREA = {
    'E': 0,
    'W': 1,
    'T': 2,
    'O': 3,
    'M': 4
}

def exposure_to_prop(a):
    return a

def probability(time):
    return 1 / (1 + np.exp(-time))


class People():
    def __init__(self, identity: str, identity_id: int, lab: int, area: str, move_matrix, lab_postion=None, addition=0, weakness=0):
        assert area in ['E', 'W', 'T', 'O', 'M'], "Invalid area: {}".format(area)
        assert identity.lower() in ['student', 'teacher'], "Invalid identity: {}".format(identity)

        # 人员信息
        self.identity = identity            # 人员类型
        self.identity_id = identity_id      # 人员标识符 (全局唯一)
        self.lab = lab
        self.move_matrix = move_matrix

        # 传染别人相关
        self.propagation_capacity = exposure_to_prop(self.exposure_time)
        self.addition_capacity = addition   # 向别人额外的易传染性

        # 被传染相关
        self.exposure_time = 0
        self.weak_immune = weakness     # 被别人额外传染的弱免疫性
        self.infected_probability = probability(self.exposure_time)
        self.infect_state = 0   # 0: Normal, 1: Infected, 2: Hidden, 3: Vacation, 4: Recovered
        self.state_duration = 0 # Duration of current state

        # 状态/位置信息
        self.current_area = AREA[area]  # 区域的首字母转换成数字
        self.experimental_position = lab_postion  # Position (If in lab)
        self.meeting_state = 0


        self.history = {
            'trajectory': [],   # 记录行动轨迹
            'exposure': [],     #
        }

    def infect(self, other):
        # 传染逻辑: 只有 Infected --> Normal 才传染
        if self.infect_state == 1 and other.infect_state == 0:
            other.exposure_time += self.propagation_capacity + self.addition_capacity - other.weak_immune
        
            
    def __str__(self):
        print(f"{self.identity} at [{AREA_FULL_NAME[self.current_area]}] [State: {INFECTION_STATE_NAME[self.infect_state]}]")

    def __eq__(self, other):
        return self.identity == other.identity and self.identity_id == other.identity_id



class Student(People):
    def __init__(self, identity_id: int, lab: int, area: str, move_matrix, lab_postion=None):
        super().__init__('student', identity_id, lab, area, move_matrix, lab_postion)

    def update(self):
        if self.infect_state == 0:
            self.propagation_capacity = exposure_to_prop(self.exposure_time)
            self.infected_probability = probability(self.exposure_time)
        elif self.infect_state == 1:
            raise NotImplementedError
        elif self.infect_state == 2:
            raise NotImplementedError
        elif self.infect_state == 3:
            raise NotImplementedError
        elif self.infect_state == 4:
            raise NotImplementedError

    def move(self):
        # 根据自身感染产生特殊行为 (回家等)
        # 无
        
        # 根据移动矩阵的概率随机选择下一步
        next_area = np.random.choice(5, 1, p=self.move_matrix[self.current_area])
        self.history['trajectory'].append(next_area)
        self.current_area = next_area
        if AREA_FULL_NAME[next_area] == 'experimental_areas':
            # 若整数点位, 改为 np.random.randint
            self.experimental_position = (np.random.uniform(0, self.lab_size[0]), np.random.uniform(0, self.lab_size[1]))
        else:
            self.experimental_position = None


class Teacher(People):
    def __init__(self, identity_id: int, lab: int, area: str, move_matrix, lab_postion=None):
        super().__init__('teacher', identity_id, lab, area, move_matrix, lab_postion)


    def update(self):
        if self.infect_state == 0:
            self.propagation_capacity = exposure_to_prop(self.exposure_time)
            self.infected_probability = probability(self.exposure_time)
        elif self.infect_state == 1:
            raise NotImplementedError
        elif self.infect_state == 2:
            raise NotImplementedError
        elif self.infect_state == 3:
            raise NotImplementedError
        elif self.infect_state == 4:
            raise NotImplementedError

    def move(self):
        # 根据自身感染产生特殊行为 (回家等)
        # 无

        # 根据移动矩阵的概率随机选择下一步
        next_area = np.random.choice(5, 1, p=self.move_matrix[self.current_area])
        self.history['trajectory'].append(next_area)
        self.current_area = next_area
        if AREA_FULL_NAME[next_area] == 'experimental_areas':
            # 若整数点位, 改为 np.random.randint
            self.experimental_position = (np.random.uniform(0, self.lab_size[0]), np.random.uniform(0, self.lab_size[1]))
        else:
            self.experimental_position = None

