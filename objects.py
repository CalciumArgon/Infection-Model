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

def exposure_to_prop(time):
    return 1 / (1 + np.exp(-time))

def probability(pro):
    if np.random.ranint(1) <= pro:
        return 2
    else:
        return 0

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
        self.infect_state = 0   # 0: Normal, 1: Infected, 2: Hidden, 3: Vacation, 4: Recovered
        self.state_duration = 0 # Duration of current state
        self.hidden2infect_day = np.random.randint(hidden2infect_day[0], hidden2infect_day[1]) #在范围内随机的 hidden 天数
        self.infect2recover_day = np.random.randint(infect2recover_day[0], infect2recover_day[1]) #在范围内随机的 infect 天数
        self.vaccation2return_day = np.random.randint(vaccation2return_day[0], vaccation2return_day[1]) #在范围内随机的 vaccation 天数

        # 状态/位置信息
        self.current_area = AREA[area]  # 区域的首字母转换成数字
        self.experimental_position = lab_postion  # Position (If in lab)
        self.meeting_state = 0

        self.history = {
            'trajectory': [],   # 记录行动轨迹
            'exposure': [],     # 应该是记录这个人被另外的人传染了多少暴露时间，例如我们想的是可以用数组实现，n[6]=1代表被6号传染了1个时间单位，用于统计谁对其他人传染的事件最多
            'exposure_area':[], # 记录这个人在某个区域被增加了多少暴露时间，用于统计哪个区域发生的暴露时间增加最多
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

    def update(self, clock):
        if self.infect_state == 0:        
            self.infect_state = probability(exposure_to_prop(self.exposure_time))
        elif clock %(10*60)==0:
            if self.infect_state == 1:
                self.infect2recover_day -=1
                if self.infect2recover_day == 0:
                    self.infect_state = 4
                elif self.infect2recover_day> infect2recover_day[1] - vaccation2return_day[1] & self.vaccation2return_day !=0 & np.random.randint(1) < 0.5:
                    self.infect_state = 3               
            elif self.infect_state == 2:
                self.hidden2infect_day -=1
                if self.hidden2infect_day == 0:
                    self.infect_state = 1               
            elif self.infect_state == 3:
                self.vaccation2return_day -=1
                self.infect2recover_day -=1
                if self.vaccation2return_day == 0:
                    self.infect_state = 1
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


    def update(self, clock):
        if self.infect_state == 0:        
            self.infect_state = probability(exposure_to_prop(self.exposure_time))
        elif clock %(10*60)==0:
            if self.infect_state == 1:
                self.infect2recover_day -=1
                if self.infect2recover_day == 0:
                    self.infect_state = 4
                elif self.vaccation2return_day !=0
                    self.infect_state = 3               
            elif self.infect_state == 2:
                self.hidden2infect_day -=1
                if self.hidden2infect_day == 0:
                    self.infect_state = 1               
            elif self.infect_state == 3:
                self.vaccation2return_day -=1
                self.infect2recover_day -=1
                if self.vaccation2return_day == 0:
                    self.infect_state = 1
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

def vacation_check():
    if self.state_duration == self.student.vacation_day:
        if self.clock == 24*60: # 考虑以天为单位变化state
            self.state_duration += 1

def work_check():

    return 0