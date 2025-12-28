import csv

def read_csv(fname):
    try:
        with open(fname, 'r') as file:
            data = list(csv.reader(file))

            print(data)

            if not data:
                return None

            student_data = []
            for element in data:
                name = element[0].strip()
                section = element[1].strip()

                try:
                    scores = [float(score) for score in element[2:12]]
                except ValueError:
                    continue 

                average = round(sum(scores) / len(scores), 3)
                student = {
                    'name': name,
                    'section': section,
                    'scores': scores,
                    'average': average
                }
                student_data.append(student)
            
            return student_data

    except (FileNotFoundError, IsADirectoryError):
        print(f"Error occurred when opening {fname} to read")
        return None

def write_csv(fname, student_data):
    try:
        with open(fname, 'w', newline='') as file:
            writer = csv.writer(file)

            for student in student_data:
                name = student['name']
                section = student['section']
                scores = student['scores']  
                row = [name, section] + scores
                writer.writerow(row)

    except Exception:
        print(f"Error occurred when opening {fname} to write")
        return

def filter_section(student_data, section_name):
    return [student for student in student_data if student['section'] == section_name]

def filter_average(student_data, min_inc, max_exc):
    return [student for student in student_data if min_inc <= student['average'] < max_exc]


import os

def split_section(fname):
    student_data = read_csv(fname)
    
    if student_data is None:
        return 
    
    sections = {student['section'] for student in student_data}
    
    base_name = os.path.splitext(fname)[0]

    for section in sections:
        section_data = filter_section(student_data, section)
        section_file = (f"{base_name}_section_{section}.csv")
        write_csv(section_file, section_data)


import math

def get_stats(nums):
    mean = sum(nums) / len(nums)
    minimum = min(nums)
    maximum = max(nums)
    range_value = maximum - minimum
    std_dev = math.sqrt(sum([(n - mean)**2 for n in nums]) / len(nums))
    
    return {'mean': mean, 'std_dev': std_dev, 'min': minimum, 'max': maximum, 'range': range_value}

def get_assignment_stats(student_data):
    return_list = []
    
    avg_scores = [student['average'] for student in student_data]
    return_list.append(get_stats(avg_scores))
    
    for i in range(10):
        scores = [student['scores'][i] for student in student_data]
        return_list.append(get_stats(scores))
    
    return return_list
