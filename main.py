import re
import numpy

answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
next_report = "Y"
while next_report == "Y":
    answer_list = []
    incorrect_count = []
    skip_count = []
    for n in range(25):
        incorrect_count.append(0)
        skip_count.append(0)
    grade_dict = {}

    answer_list = re.split(r',', answer_key)

    filename = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
    try:
        with open(f'Data Files/{filename}.txt', mode='r') as file:
            class_data = file.readlines()

        print(f'Successfully open {filename}.txt')
        valid_lines = 0
        invalid_lines = 0
        total_lines = 0
        invalid_list = []

        ## Check format của từng hàng
        pattern = re.compile("^N[0-9]{8}(,[A-Z]?){25}")

        for student in class_data:
            total_lines += 1
            student_id = re.split(r",", student.strip())[0]
            student_answer = re.split(r",", student.strip())[1:]
            grade = 0
            if re.match(pattern, student):
                valid_lines += 1
                for n in range(len(answer_list)):
                    if student_answer[n] == answer_list[n]:
                        grade += 4
                    elif student_answer[n] == "":
                        grade += 0
                        skip_count[n] += 1
                    else:
                        grade -= 1
                        incorrect_count[n] += 1
                    grade_dict[student_id] = grade
            else:
                invalid_lines += 1
            with open(f'Data Files/Grades/{filename}.txt', mode='a+') as writefile:
                writefile.write(f'{student_id}: {grade} \n')
        ## Analyzing
        print('*** ANALYZING ***')
        if invalid_lines == 0:
            print("No errors found!")
        else:
            for line in class_data:
                if not re.match(pattern, line):
                    print(line)
                    if not (re.match(r"^N[0-9]{8}", line)):
                        print("Invalid line of data: N# is invalid")
                    else:
                        print("Invalid line of data: does not contain exactly 26 values")

        # Reports
        mean_score = numpy.array(list(grade_dict.values())).mean()
        max_score = numpy.array(list(grade_dict.values())).max()
        min_score = numpy.array(list(grade_dict.values())).min()
        median_score = numpy.median(list(grade_dict.values()))
        print('*** REPORT ***')
        print(f'Total line of data: {total_lines}')
        print(f'Total valid lines of data: {valid_lines}')
        print(f'Total invalid lines of data: {invalid_lines}')
        print(f'Mean (average) score: {mean_score}')
        print(f'Highest score: {max_score}')
        print(f'Lowest score: {min_score}')
        print(f'Range of scores: {max_score - min_score}')
        print(f'Median score: {median_score}')
        max_skip_indices = [f"Q.{index+1}" for index, item in enumerate(skip_count) if item == max(skip_count)]
        max_incorrect_indices = [f"Q.{index+1}" for index, item in enumerate(incorrect_count) if item == max(incorrect_count)]
        print(f'Question that most people skip: ' + ', '.join(a for a in max_skip_indices) + f' - {max(skip_count)}')
        print(f'Question that most people answer incorrectly: '
              + ', '.join(a for a in max_incorrect_indices) + f' - {max(incorrect_count)}')
    except FileNotFoundError:
        print('File cannot be found.')
    next_report = input("Restart? Y/N ")
    if next_report == "Y":
        print(">>> ================================ RESTART ================================ >>>")
