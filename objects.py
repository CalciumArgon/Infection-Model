class Virus():
    def __init__(self, name, infect_radius):
        self.name = name
        self.infect_radius = infect_radius
    
    def __str__(self):
        return f"Virus({self.name}, {self.infect_radius})"

    
InfectionState = {
    0: 'Normal',
    1: 'Infected',
    2: 'Hidden',
    3: 'Vacation',
    4: 'Recovered',
}

Area = {
    'E': 'experimental_areas',
    'W': 'work_areas',
    'T': 'toilet',
    'O': 'office',
    'M': 'meeting_room'
}

class People():
    def __init__(self, identity, lab, area, move_matrix, lab_postion=None):
        assert area in ['E', 'W', 'T', 'O', 'M'], "Invalid area: {}".format(area)
        assert identity.lower() in ['student', 'teacher'], "Invalid identity: {}".format(identity)

        self.identity = identity
        self.lab = lab
        self.exposure_time = 0
        self.infect_state = 0   # 0: Normal, 1: Infected, 2: Hidden, 3: Vacation, 4: Recovered
        self.state_duration = 0 # Duration of current state
        self.current_area = area

        self.experimental_position = lab_postion  # Position (If in lab)
        self.meeting_state = 0

        self.move_matrix = move_matrix

        self.history = {
            'trajectory': [],
            'exposure': [],
        }

    def __str__(self):
        print(f"{self.identity} at [{Area[self.current_area]}] [State: {InfectionState[self.infect_state]}]")


class Student(People):
    def __init__(self, lab, area, move_matrix, lab_postion=None):
        super().__init__('student', lab, area, move_matrix, lab_postion)

    def move(self):
        pass


class Teacher(People):
    def __init__(self, lab, area, move_matrix, lab_postion=None):
        super().__init__('teacher', lab, area, move_matrix, lab_postion)

    def move(self):
        pass

