import string
import random
import file_writer
import csv_reader

freshmanclass = int(input("What graduating year is the freshman class?"))


class Student:
    def __init__(self, year, name, isMale):
        self.name = name
        self.isMale = isMale
        self.year = int(year)

    def isMale(self):
        return self.isMale

    def __str__(self):
        self.gender = ""
        if self.isMale:
            self.gender = "Male"
        else:
            self.gender = "Female"
        return self.name + " " + self.gender + " " + str(freshmanclass - self.year)

class Table:
    def __init__(self, id, teacher, spots=10):
        self.id = id
        self.list = []
        self.teacher = teacher
        self.spots_left = int(spots)  # changes with different tables

    def add_student(self, student):
        if isinstance(student, Student):
            self.list.append(student)
            self.spots_left -= 1

    def add_teacher(self, teacher):
        if isinstance(teacher, Teacher):
            self.teacher = teacher
            self.spots_left -= teacher.total

    def __str__(self):
        string = "id: " + str(self.id) + " \n"
        string += "teacher: " + str(self.teacher) + " \n"
        string += "students:\n"
        for student in self.list:
            string += str(student) + '\n'
        string += "\n"
        return string

class Teacher:
    def __init__(self, name, isMale, guest):
        self.name = name
        self.isMale = isMale
        self.guest = guest
        self.total = guest + 1

    def __str__(self):
        self.gender = ""
        if self.isMale:
            self.gender = "Male"
        else:
            self.gender = "Female"
        return self.name + " " + str(self.gender)


def randomStudent(stringLength=6):
    """Generate a random Student """
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(stringLength))
    year = random.randint(0, 3)
    gender = random.choice([True, False])
    return Student(year, name, gender)


def randomTeacher(stringLength=6):
    """Generate a random Teacher """
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(stringLength))
    gender = random.choice([True, False])
    guest = 0
    return Teacher(name, gender, guest)


def reorder_student_list(organized_student_list):
    for iter_num in range(len(organized_student_list) - 1, 0, -1):
        for idx in range(iter_num):
            if len(organized_student_list[idx]) < len(organized_student_list[idx + 1]):
                temp = organized_student_list[idx]
                organized_student_list[idx] = organized_student_list[idx + 1]
                organized_student_list[idx + 1] = temp


excel_data = csv_reader.array_to_dataframe()
student_dataframe = excel_data[0]
table_dataframe = excel_data[1]

""" Fill complete student list """
complete_student_list = []
for i in range(1, student_dataframe.shape[0]):
    """last_name, preferred, sex_code, board_day, YOG"""
    single_student = student_dataframe.iloc[i, [1, 2, 3, 4, 5]]

    sex = str(single_student[3])
    if sex == "M":
        isMale = True
    else:
        isMale = False

    if single_student[4] == "B":
        student = Student(freshmanclass - int(float(single_student[5])), single_student[1] + ", " + single_student[2],
                          isMale)
        complete_student_list.append(student)

fresh_boy = []
fresh_girl = []
soph_boy = []
soph_girl = []
jun_boy = []
jun_girl = []
sen_boy = []
sen_girl = []

organized_student_list = [fresh_boy, fresh_girl, soph_boy, soph_girl, jun_boy, jun_girl, sen_boy, sen_girl]
tables = []

teachers = []

for x in range(len(complete_student_list)):
    student = complete_student_list[x]
    if student.year == 0:
        if student.isMale:
            fresh_boy.append(student)
        else:
            fresh_girl.append(student)
    elif student.year == 1:
        if student.isMale:
            soph_boy.append(student)
        else:
            soph_girl.append(student)
    elif student.year == 2:
        if student.isMale:
            jun_boy.append(student)
        else:
            jun_girl.append(student)
    elif student.year == 3:
        if student.isMale:
            sen_boy.append(student)
        else:
            sen_girl.append(student)

""" Fill table list """
for i in range(1, table_dataframe.shape[0]):
    """faculty, table_index, seats_assignable"""
    single_table = table_dataframe.iloc[i, [1, 2, 6]]
    if int(float(single_table[6])) > 0:
        table = Table(single_table[2], single_table[1], int(float(single_table[6])))
        tables.append(table)

random.shuffle(fresh_boy)
random.shuffle(fresh_girl)
random.shuffle(soph_boy)
random.shuffle(soph_girl)
random.shuffle(jun_boy)
random.shuffle(jun_girl)
random.shuffle(sen_boy)
random.shuffle(sen_girl)
# print(len(fresh_boy), len(fresh_girl), len(soph_boy), len(soph_girl), len(jun_boy), len(jun_girl), len(sen_boy),
#       len(sen_girl))


def num_non_zero_list(list):
    cnt = 0
    for l in list:
        if len(l) > 0:
            cnt += 1
    return cnt


def fill_table(index, f_b, f_g, so_b, so_g, j_b, j_g, se_b, se_g):
    """ add teacher (already added in filling table list) """
    # tables[index].add_teacher(teachers.pop())

    """ preparing for students """
    spots = tables[index].spots_left
    organized_student_list = [f_b, f_g, so_b, so_g, j_b, j_g, se_b, se_g]
    reorder_student_list(organized_student_list)

    non_zero_count = num_non_zero_list(organized_student_list)
    if (non_zero_count == 0):
        print("Divide by zero error")
        return

    upper_bound = int(spots / non_zero_count) + 1
    lower_bound = upper_bound - 1
    num_upper_bound = int(spots % non_zero_count)

    if (lower_bound != 0):
        num_lower_bound = int((spots - upper_bound * num_upper_bound) / lower_bound)
    else:
        num_lower_bound = 0

    # print("table: ", index, "spots_left:", spots, "upper_bound:", upper_bound, "lower_bound:", lower_bound, "num_up:",
    #       num_upper_bound, "num_low:", num_lower_bound)

    """ add student"""
    for i in range(num_upper_bound):
        for n in range(upper_bound):
            if (len(organized_student_list[i]) != 0):
                tables[index].add_student(organized_student_list[i].pop())
    for i in range(num_upper_bound, num_upper_bound + num_lower_bound):
        for n in range(lower_bound):
            if (len(organized_student_list[i]) != 0):
                tables[index].add_student(organized_student_list[i].pop())


for i in range(len(tables)):
    fill_table(i, fresh_boy, fresh_girl, soph_boy, soph_girl, jun_boy, jun_girl, sen_boy, sen_girl)

""" checking students left """
total_assigned = 0
for i in range(len(tables)):
    # print(tables[i])
    total_assigned += len(tables[i].list)
# print("total assigned: ", total_assigned)

cnt_f_b, cnt_f_g, cnt_so_b, cnt_so_g, cnt_j_b, cnt_j_g, cnt_se_b, cnt_se_g = 0, 0, 0, 0, 0, 0, 0, 0

for i in range(len(tables)):
    for student in tables[i].list:
        if student.year == 0 and student.isMale:
            cnt_f_b += 1
        elif student.year == 0 and not student.isMale:
            cnt_f_g += 1
        elif student.year == 1 and student.isMale:
            cnt_so_b += 1
        elif student.year == 1 and not student.isMale:
            cnt_so_g += 1
        elif student.year == 2 and student.isMale:
            cnt_j_b += 1
        elif student.year == 2 and not student.isMale:
            cnt_j_g += 1
        elif student.year == 3 and student.isMale:
            cnt_se_b += 1
        elif student.year == 3 and not student.isMale:
            cnt_se_g += 1

# print(cnt_f_b, cnt_f_g, cnt_so_b, cnt_so_g, cnt_j_b, cnt_j_g, cnt_se_b, cnt_se_g)

""" write table lists """
table_str = ""
for i in range(len(tables)):
    table_str += str(tables[i])
    table_str += "\n"
table_str += "Total number of assigned students: " + str(total_assigned) + "\n"
table_str += "Students left unassigned:\n"
for student_list in organized_student_list:
    for student in student_list:
        table_str += str(student) + "\n"

file_writer.write_output_file(table_str)
print("Students are assigned! Look for a file called 'table assignments.txt'")
