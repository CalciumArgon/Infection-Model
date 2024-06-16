import numpy as np

from config import cfg
from objects import *
from utils import *



class Simulation():
    def __init__(self, cfg):
        self.config = cfg
        self.virus = Virus(cfg.virus.name, cfg.virus.infect_radius)
        self.students = []
        self.teachers = []
        self.labs = []

        for i in range(cfg.student.number / 3):
            self.students.append(Student(0, 'E', cfg.student.move_matrix, [0, 0]))
            self.students.append(Student(1, 'W', cfg.student.move_matrix))


if __name__ == '__main__':
    _ = parse_args()
    print_easydict(cfg)
    simulation = Simulation(cfg)