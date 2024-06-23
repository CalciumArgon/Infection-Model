import numpy as np

from config import cfg
from objects import *
from utils import *


class Simulation():
    def __init__(self, cfg):
        self.config = cfg
        self.virus = Virus(cfg.virus.name, cfg.virus.infect_radius, cfg.virus.infect_intense_range)
        self.avg_infect_capacity = 0.5 * (cfg.virus.infect_intense_range[0] + cfg.virus.infect_intense_range[1])

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

        # 学生性质
        self.talktive_rate = cfg.student.talktive_rate
        self.immune_rate = cfg.student.immune_rate
        self.stu_init_infect = cfg.student.init_infect

        # 老师性质
        self.tea_talktive_rate = cfg.teacher.talktive_rate
        self.tea_immune_rate = cfg.teacher.immune_rate
        self.tea_init_infect = cfg.teacher.init_infect

        # 实验室信息
        self.lab_num = cfg.environment.lab_number
        self.lab_size = (cfg.environment.lab_length, cfg.environment.lab_width)

        # 事件信息 -- 各个实验室分开
        self.meeting_rate = cfg.event.meeting_rate
        self.meeting_scale = cfg.event.meeting_scale
        self.meeting_duration = cfg.event.meeting_duration
        assert len(self.meeting_rate) == len(self.meeting_scale) == len(self.meeting_duration) == self.lab_num, "Meeting config length has to be same as lab-number"


        for lab in range(self.lab_num):
            # 对于每个lab的学生, 全局标识号的前部分为初始在实验室的, 后部分为初始在工作区的
            for i in range(cfg.student.e_number):
                # 添加实验室学生, 坐标随机, 全局标识号为: lab * stu_num + i
                is_talktive = np.random.choice([cfg.student.talktive_addition, 0], p=[self.talktive_rate, 1-self.talktive_rate])
                is_immune = np.random.choice([cfg.student.immune_defence, 0], p=[self.immune_rate, 1-self.immune_rate])
                basic_capacity = np.random.randint(self.virus.infect_intense_range[0], self.virus.infect_intense_range[1]+1)
                self.students.append(Student(
                                            lab * self.stu_num + i, 
                                            lab, 'E', basic_capacity, self.avg_infect_capacity,
                                            cfg.student.hidden2infect_day, cfg.student.infect2recover_day, cfg.student.vacation2return_day,
                                            cfg.student.move_matrix,
                                            # 如果整点随机改为 np.random.randint
                                            lab_postion=(np.random.uniform(0,self.lab_size[0]), np.random.uniform(0, self.lab_size[1])),
                                            addition=is_talktive, immune=is_immune
                                        )
                                    )
            for i in range(cfg.student.w_number):
                # 添加工作区学生, 工位号固定为其全局标识号: lab * stu_num + e_number + i
                is_talktive = np.random.choice([cfg.student.talktive_addition, 0], p=[self.talktive_rate, 1-self.talktive_rate])
                is_immune = np.random.choice([cfg.student.immune_defence, 0], p=[self.immune_rate, 1-self.immune_rate])
                basic_capacity = np.random.randint(self.virus.infect_intense_range[0], self.virus.infect_intense_range[1]+1)
                self.students.append(Student(lab * self.stu_num + cfg.student.e_number + i,
                                             lab, 'W', basic_capacity, self.avg_infect_capacity,
                                             cfg.student.hidden2infect_day, cfg.student.infect2recover_day, cfg.student.vacation2return_day,
                                             cfg.student.move_matrix,
                                             addition=is_talktive, immune=is_immune
                                        )
                                    )
                
        for lab in range(cfg.environment.lab_number):
            for i in range(cfg.teacher.number):
                # 老师初始都在 Office, 全局标识符: 学生总数 + lab * cfg.teacher.number + i
                is_talktive = np.random.choice([cfg.teacher.talktive_addition, 0], p=[self.tea_talktive_rate, 1-self.tea_talktive_rate])
                is_immune = np.random.choice([cfg.teacher.immune_defence, 0], p=[self.tea_immune_rate, 1-self.tea_immune_rate])
                basic_capacity = np.random.randint(self.virus.infect_intense_range[0], self.virus.infect_intense_range[1]+1)
                self.teachers.append(Teacher(lab * cfg.teacher.number + i,
                                              lab, 'O', basic_capacity, self.avg_infect_capacity,
                                              cfg.teacher.hidden2infect_day, cfg.teacher.infect2recover_day, cfg.teacher.vacation2return_day,
                                              cfg.teacher.move_matrix,
                                              addition=is_talktive, immune=is_immune
                                        )
                                    )
                
        # 设置初始感染者
        for lab in range(self.lab_num):
            this_lab_student = [s for s in self.students if s.lab == lab]
            init_infect_stu = np.random.choice(this_lab_student, self.stu_init_infect[lab], replace=False)
            for s in init_infect_stu:
                s.infect_state = 1
                s.history['exposure']['init'] = True
            this_lab_teacher = [t for t in self.teachers if t.lab == lab]
            init_infect_tea = np.random.choice(this_lab_teacher, self.tea_init_infect, replace=False)
            for t in init_infect_tea:
                t.infect_state = 1
                t.history['exposure']['init'] = True
                
    def action(self):
        # 每个状态先相互传染
        for p in (self.students + self.teachers):
            for other_p in (self.students + self.teachers):
                if other_p == p:  # 重载了 ==, 比较 identity 和 identity_id
                    continue    # 不考虑自己
                if (p.current_area == other_p.current_area):
                    # 在同一区域传染; 若在实验室还需小于传染半径; 若在工位认为工号在其正负4的人传染(可能跨Lab)
                    if (p.current_area not in [0,1]) \
                            or (p.current_area == 0 and dist(p, other_p) <= self.virus.infect_radius) \
                            or (p.current_area == 1 and abs(p.identity_id - other_p.identity_id) <= 4):
                        p.infect(other_p)

        # 每个实验室按照自己的概率决定开会
        for lab in range(self.lab_num):
            if np.random.rand() < self.meeting_rate[lab]:   # 该实验室决定开会
                this_lab_student = [s for s in self.students if s.lab == lab]
                unlucky = np.random.choice(this_lab_student,
                                           int(self.meeting_scale[lab] * self.stu_num), replace=False)
                lucky = [x for x in self.students if x not in unlucky]
                for s in unlucky:     # 学生按比例参会
                    s.update(self.clock)
                    s.move(self.lab_size, call_to_meeting=self.meeting_duration[lab])
                for s in lucky:     # 不参会的学生
                    s.update(self.clock)
                    s.move(self.lab_size)
                this_lab_teacher = [t for t in self.teachers if t.lab == lab]
                unlucky_tea = np.random.choice(this_lab_teacher,
                                               int(self.meeting_scale[lab] * self.tea_num), replace=False)
                lucky_tea = [x for x in self.teachers if x not in unlucky_tea]
                for t in unlucky_tea:     # 老师按比例参会
                    t.update(self.clock)
                    t.move(self.lab_size, call_to_meeting=self.meeting_duration[lab])
                for t in lucky_tea:     # 不参会的老师
                    t.update(self.clock)
                    t.move(self.lab_size)
        
        self.clock += 10
        return

    @staticmethod
    def day(self):
        return self.clock // (10 * 60)
    
    @staticmethod
    def hour(self):
        return (self.clock // 60) % 10
    
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
        does_all_recover = [False for _ in range(self.lab_num)]
        for lab in range(self.lab_num):
            infected_stu = len([s for s in self.students if s.lab == lab and s.infect_state == 1])
            infected_tea = len([t for t in self.teachers if t.lab == lab and t.infect_state == 1])
            print('  Lab {}: student: {} ({}%), teacher: {} ({}%)'.format(lab, infected_stu, round(100*infected_stu / self.stu_num, 2)
                                                                          , infected_tea, round(100*infected_tea / self.tea_num, 2))
            )
            if infected_stu == 0 and infected_tea == 0:
                does_all_recover[lab] = True
        if all(does_all_recover):
            assert False, 'All people in all labs are recovered!'
        print('People postions:')
        stu_dis, tea_dis = self.posi_distribution(self)
        print('(corresponding [E W T O M])')
        for lab in range(self.lab_num):
            print('  Lab {}:'.format(lab))
            print('    Student:', stu_dis[lab])
            print('    Teacher:', tea_dis[lab])
        print('==========================================')
        return ''
    
    
    def infection_situation(self):
        # 返回一些更具体的信息, 比如暴露时间分布, 状态分布
        students_situation = []


if __name__ == '__main__':
    _ = parse_args()
    print_easydict(cfg)
    np.random.seed(cfg.seed)

    simulation = Simulation(cfg)
    
    for ii in range(3000):
        if ii % 10 == 0:
            print('Round:', ii)
            print(simulation)
            
        simulation.action()