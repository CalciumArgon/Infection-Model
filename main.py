import numpy as np

from config import cfg
from objects import *
from utils import *



class Simulation():
    def __init__(self, cfg):
        self.config = cfg
        self.virus = Virus(cfg.virus.name, cfg.virus.infect_radius)

        # 时钟信息 -------------------------------------
        self.clock = 0  # 按分钟计, 但可以每次+60模拟小时
        # --------------------------------------------

        # 记录所有人
        self.students = []
        self.teachers = []
        # self.labs = []

        # 单个实验室中的人数
        self.w_number = cfg.student.w_number
        self.e_number = cfg.student.e_number
        self.stu_num = cfg.student.e_number + cfg.student.w_number
        self.tea_num = cfg.teacher.number

        self.lab_num = cfg.environment.lab_number
        self.lab_size = (cfg.environment.lab_length, cfg.environment.lab_width)
        for lab in range(self.lab_num):
            # 对于每个lab的学生, 全局标识号的前部分为初始在实验室的, 后部分为初始在工作区的
            for i in range(cfg.student.e_number):
                # 添加实验室学生, 坐标随机, 全局标识号为: lab * stu_num + i
                self.students.append(Student(
                                            lab * self.stu_num + i, 
                                            lab, 'E', cfg.student.move_matrix,
                                            # 如果整点随机改为 np.random.randint
                                            lab_postion=(np.random.uniform(0,self.lab_size[0]), np.random.uniform(0, self.lab_size[1]))
                                        )
                                    )
            for i in range(cfg.student.w_number):
                # 添加工作区学生, 工位号固定为其全局标识号: lab * stu_num + e_number + i
                self.students.append(Student(lab * self.stu_num + cfg.student.e_number + i, 
                                             lab, 'W', cfg.student.move_matrix
                                        )
                                    )
                
        for lab in range(cfg.environment.lab_number):
            for i in range(cfg.teacher.number):
                # 老师初始都在 Office, 全局标识符: lab * cfg.teacher.number + i
                self.teachers.append(Teacher(lab * cfg.teacher.number + i,
                                              lab, 'O', cfg.teacher.move_matrix
                                        )
                                    )
                
    def action(self):
        for s in self.students:
            for other_s in self.students:
                if other_s == s:  # 重载了 ==, 比较 identity_id
                    continue    # 不考虑自己
                if (s.current_area == other_s.current_area):
                    # 在同一区域传染; 若在实验室还需小于传染半径
                    if (s.current_area != 0) or (s.current_area == 0 and dist(s, other_s) <= self.virus.infect_radius):
                        s.infect(other_s)

        # 最后所有人移动
        for s in self.students:
            s.update()
            s.move()
        for t in self.teachers:
            t.update()
            t.move()
        
        self.clock += 60
        return

    @staticmethod
    def day(self):
        return self.clock // (24 * 60)
    
    @staticmethod
    def hour(self):
        return (self.clock // 60) % 24
    
    @staticmethod
    def posi_distribution(self):
        # 分布按 'E W T O M' 的顺序记录各区域人数
        stu_distribution = np.zeros((self.lab_num, 5), dtype=int)
        tea_distribution = np.zeros((self.lab_num, 5), dtype=int)
        for s in self.students:
            stu_distribution[s.lab][s.current_area] += 1
        for t in self.teachers:
            tea_distribution[t.lab][t.current_area] += 1
        return (stu_distribution, tea_distribution)


    def __str__(self):
        print('=============== Simulation ===============')
        print('[Config]')
        print('Lab number: {}'.format(self.config.environment.lab_number))
        print('#Student in each lab: {}'.format(self.stu_num))
        print('#Teacher in each lab: {}'.format(self.tea_num))
        print('Lab size: {} x {}'.format(self.lab_size[0], self.lab_size[1]))
        print('[Virus]')
        print('Name: {}, Infection R={}'.format(self.virus.name, self.virus.infect_radius))

        print('[State]')
        print('{} days, {} hours'.format(self.day(self), self.hour(self)))
        print('Infected people number:')
        for lab in range(self.lab_num):
            infected_stu = len([s for s in self.students if s.lab == lab and s.infect_state == 1])
            infected_tea = len([t for t in self.teachers if t.lab == lab and t.infect_state == 1])
            print('  Lab {}: student: {} ({}%), teacher: {} ({}%)'.format(lab, infected_stu, round(100*infected_stu / self.stu_num, 2)
                                                                          , infected_tea, round(100*infected_tea / self.tea_num, 2))
            )
        print('People postions:')
        stu_dis, tea_dis = self.posi_distribution(self)
        print('(corresponding [E W T O M])')
        for lab in range(self.lab_num):
            print('  Lab {}:'.format(lab))
            print('    Student:', stu_dis[lab])
            print('    Teacher:', tea_dis[lab])
        print('==========================================')
        return ''


if __name__ == '__main__':
    _ = parse_args()
    print_easydict(cfg)
    simulation = Simulation(cfg)
    print(simulation)