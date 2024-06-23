import numpy as np

class Virus():
    def __init__(self, name, infect_radius, infect_intense_range):
        self.name = name
        self.infect_radius = infect_radius
        self.infect_intense_range = infect_intense_range
    
    def __str__(self):
        return f"Virus({self.name}, R={self.infect_radius}), Basic Intense Range={self.infect_intense})"

    
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

# def exposure_to_propagation(time):
#     return time


def create_becomeHidden(av):
    def becomeHidden(time):
        pro = 1 / (1 + np.exp(6 - (time/av)))
        return np.random.choice([True, False], p=[pro, 1-pro])
    return becomeHidden


class People():
    def __init__(self, identity: str, identity_id: int, lab: int, area: str, basic_infect_capacity, avg_infect_capacity,
                 hidden2infect_day, infect2recover_day, vaccation2return_day,
                  move_matrix, lab_postion=None, addition=0, immune=0):
        assert area in ['E', 'W', 'T', 'O', 'M'], "Invalid area: {}".format(area)
        assert identity.lower() in ['student', 'teacher'], "Invalid identity: {}".format(identity)

        # 人员信息
        self.identity = identity            # 人员类型
        self.identity_id = identity_id      # 人员标识符 (全局唯一)
        self.lab = lab
        self.move_matrix = move_matrix
        self.meeting_state = 0      # 记录开会剩余时间 (如果在开会的话)

        # 被传染相关
        self.exposure_time = 0
        self.immune = immune     # 强免疫 减缓暴露时间增加的速度
        self.infect_state = 0   # 0: Normal, 1: Infected, 2: Hidden, 3: Vacation, 4: Recovered
        self.state_duration = 0 # Duration of current state
        self.hidden2infect_day = np.random.randint(hidden2infect_day[0], hidden2infect_day[1])      # 在范围内随机
        self.infect2recover_day = np.random.randint(infect2recover_day[0], infect2recover_day[1])
        self.vacation2return_day = np.random.randint(vaccation2return_day[0], vaccation2return_day[1])


        # 传染别人相关
        self.basic_capacity = basic_infect_capacity    # 基础传染能力
        self.talktive_capacity = addition   # 话太多 向别人额外的传染能力
        self.becomeHidden = create_becomeHidden(avg_infect_capacity)  # Normal->Hidden 转移概率函数
        

        # 状态/位置信息
        self.current_area = AREA[area]  # 区域的首字母转换成数字
        self.experimental_position = lab_postion  # Position (If in lab)
        self.meeting_state = 0

        self.history = {
            'trajectory': [self.current_area],   # 记录行动轨迹
            'exposure': {'init': False},     # 记录这个人被另外的人传染了多少暴露时间，如n[6]=1代表6号贡献了1个时间单位，用于统计谁对其他人传染的事件最多
            'exposure_area': [0, 0, 0, 0, 0], # 记录这个人在某个区域被增加了多少暴露时间，用于统计哪个区域发生的暴露时间增加最多
            'state_change_area': [-1, -1]     # 主要记录 normal->hidden 和 hidden->infected 发生的位置
        }

    def infect(self, other):
        # 传染逻辑: 只有 Infected --> Normal 才传染
        if self.infect_state == 1 and other.infect_state == 0:
            add = self.basic_capacity + self.talktive_capacity - other.immune
            other.exposure_time += add
            other.history['exposure'][self.identity_id] = other.history['exposure'].get(self.identity_id, 0) + add
            other.history['exposure_area'][self.current_area] += add

        
    def __str__(self):
        print(f"{self.identity} at [{AREA_FULL_NAME[self.current_area]}] [State: {INFECTION_STATE_NAME[self.infect_state]}]")

    def __eq__(self, other):
        return self.identity == other.identity and self.identity_id == other.identity_id



class Student(People):
    def __init__(self, identity_id: int, lab: int, area: str, basic_infect_capacity, avg_infect_capacity,
                 hidden2infect_day, infect2recover_day, vaccation2return_day,
                 move_matrix, lab_postion=None, addition=0, immune=0):
        super().__init__('student', identity_id, lab, area, basic_infect_capacity, avg_infect_capacity,
                         hidden2infect_day, infect2recover_day, vaccation2return_day, move_matrix,
                         lab_postion=lab_postion,
                         addition=addition,
                         immune=immune)

    def update(self, clock):
        # 更新

        # 更新感染状态 ------------
        phase = INFECTION_STATE_NAME[self.infect_state]
        if phase == 'Normal':      # 变成潜伏期每个周期检查, 按照一个基于暴露时间的概率变成潜伏期
            if self.becomeHidden(self.exposure_time):
                self.infect_state = 2
                self.history['state_change_area'][0] = self.current_area    # 记录在此地转换成 Hidden
        elif (clock / 60) % 10 == 0:    # 其他状态的转换每天检查
            if phase == 'Infected':
                self.infect2recover_day -=1
                if self.infect2recover_day == 0:
                    self.infect_state = 4
                elif np.random.rand() < 0.3:    # 若student当天没好, 则 0.3 的概率去休假
                    self.infect_state = 3
            elif phase == 'Hidden':
                self.hidden2infect_day -= 1
                if self.hidden2infect_day == 0:
                    self.infect_state = 1
                    self.history['state_change_area'][1] = self.current_area    # 记录在此地转换成 Infected
            elif phase == 'Vacation':
                self.vacation2return_day -= 1
                self.infect2recover_day -= 1
                if self.vacation2return_day == 0:   # 度假恢复后 没到 infect2recover_day 就仍感染
                    self.infect_state = 1 if self.infect2recover_day > 0 else 4
            elif phase == 'Recovered':
                pass
        return


    def move(self, lab_size, call_to_meeting=0):
        # 根据自身感染产生特殊行为
        if AREA_FULL_NAME[self.current_area] == 'meeting_room':
            self.meeting_state -= 10
            if self.meeting_state != 0:     # 没开完会议则哪都不去, 开完会则正常按转移矩阵行动
                self.history['trajectory'].append(self.current_area)
                return
        
        if call_to_meeting > 0:
            self.meeting_state = call_to_meeting
            self.current_area = 4
            self.history['trajectory'].append(self.current_area)
            return
            
        # 根据移动矩阵的概率随机选择下一步
        next_area = np.random.choice(5, 1, p=self.move_matrix[self.current_area])[0]
        self.history['trajectory'].append(next_area)
        self.current_area = next_area
        if AREA_FULL_NAME[next_area] == 'experimental_areas':
            # 若整数点位, 改为 np.random.randint
            self.experimental_position = (np.random.uniform(0, lab_size[0]), np.random.uniform(0, lab_size[1]))
        else:
            self.experimental_position = None


class Teacher(People):
    def __init__(self, identity_id: int, lab: int, area: str, basic_infect_capacity, avg_infect_capacity,
                 hidden2infect_day, infect2recover_day, vaccation2return_day,
                 move_matrix, lab_postion=None, addition=0, immune=0):
        super().__init__('teacher', identity_id, lab, area, basic_infect_capacity, avg_infect_capacity,
                         hidden2infect_day, infect2recover_day, vaccation2return_day, move_matrix,
                         lab_postion=lab_postion,
                         addition=addition,
                         immune=immune)


    def update(self, clock):
        # 更新

        # 更新感染状态 ------------
        phase = INFECTION_STATE_NAME[self.infect_state]
        if phase == 'Normal':      # 变成潜伏期每个周期检查, 按照一个基于暴露时间的概率变成潜伏期    
            self.infect_state = 2 if self.becomeHidden(self.exposure_time) else 0
        elif (clock / 60) % 10 == 0:    # 其他状态的转换每天检查
            if phase == 'Infected':
                self.infect2recover_day -= 1
                if self.infect2recover_day == 0:
                    self.infect_state = 4
                elif self.vacation2return_day != 0:
                    self.infect_state = 3
            elif self.infect_state == 2:
                self.hidden2infect_day -= 1
                if self.hidden2infect_day == 0:
                    self.infect_state = 1               
            elif self.infect_state == 3:
                self.vacation2return_day -=1
                self.infect2recover_day -=1
                if self.vacation2return_day == 0:   # 度假恢复后 没到 infect2recover_day 就仍感染
                    self.infect_state = 1 if self.infect2recover_day > 0 else 4
            elif self.infect_state == 4:
                pass
        return


    def move(self, lab_size, call_to_meeting=0):
        # 根据自身感染产生特殊行为
        if AREA_FULL_NAME[self.current_area] == 'meeting_room':
            self.meeting_state -= 10
            if self.meeting_state != 0:     # 没开完会议则哪都不去, 开完会则正常按转移矩阵行动
                self.history['trajectory'].append(self.current_area)
                return
        
        if call_to_meeting > 0:
            self.meeting_state = call_to_meeting
            self.current_area = 4
            self.history['trajectory'].append(self.current_area)
            return

        # 根据移动矩阵的概率随机选择下一步
        next_area = np.random.choice(5, 1, p=self.move_matrix[self.current_area])[0]
        self.history['trajectory'].append(next_area)
        self.current_area = next_area
        if AREA_FULL_NAME[next_area] == 'experimental_areas':
            # 若整数点位, 改为 np.random.randint
            self.experimental_position = (np.random.uniform(0, lab_size[0]), np.random.uniform(0, lab_size[1]))
        else:
            self.experimental_position = None

    def vacation_check(self):
        if self.state_duration == self.student.vacation_day:
            if self.clock == 24*60: # 考虑以天为单位变化state
                self.state_duration += 1

    def work_check(self):
        return 0