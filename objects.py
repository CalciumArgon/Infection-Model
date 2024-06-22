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

AREA_FULL_NAME = {
    'E': 'experimental_areas',
    'W': 'work_areas',
    'T': 'toilet',
    'O': 'office',
    'M': 'meeting_room'
}

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
    def __init__(self, identity: str, identity_id: int, lab: int, area: str, move_matrix, lab_postion=None):
        assert area in ['E', 'W', 'T', 'O', 'M'], "Invalid area: {}".format(area)
        assert identity.lower() in ['student', 'teacher'], "Invalid identity: {}".format(identity)

        self.identity = identity            # 人员类型
        self.identity_id = identity_id      # 人员标识符 (全局唯一)
        self.lab = lab
        self.exposure_time = 0
        self.propagation_capacity = exposure_to_prop(self.exposure_time)
        self.infected_probability = probability(self.exposure_time)
        self.infect_state = 0   # 0: Normal, 1: Infected, 2: Hidden, 3: Vacation, 4: Recovered
        self.state_duration = 0 # Duration of current state
        self.current_area = AREA[area]  # 区域的首字母转换成数字

        self.experimental_position = lab_postion  # Position (If in lab)
        self.meeting_state = 0

        self.move_matrix = move_matrix

        self.history = {
            'trajectory': [],
            'exposure': [],
        }

    def __str__(self):
        print(f"{self.identity} at [{AREA_FULL_NAME[self.current_area]}] [State: {INFECTION_STATE_NAME[self.infect_state]}]")


class Student(People):
    def __init__(self, identity_id: int, lab: int, area: str, move_matrix, lab_postion=None):
        super().__init__('student', identity_id, lab, area, move_matrix, lab_postion)

    def move(self):
        pass


class Teacher(People):
    def __init__(self, identity_id: int, lab: int, area: str, move_matrix, lab_postion=None):
        super().__init__('teacher', identity_id, lab, area, move_matrix, lab_postion)

    def move(self):
        pass

