import schoolopy
from datetime import datetime, timedelta
import webbrowser as wb
import json

key = ''
secret = ''
user_id = ''

auth = schoolopy.Auth(key, secret, three_legged=True, domain='https://schoology.harker.org')
url = auth.request_authorization()

print(url)

while not auth.authorize():
    continue

sc = schoolopy.Schoology(auth)



# SECTIONS

section_ids = []

sections = sc.get_sections(user_id)

for section in sections:
    section_ids.append(section['id'])



# ASSIGNMENTS

assignments_raw = []
upcoming_raw = []

for section_id in section_ids:
    assignments_raw.append(sc.get_assignments(section_id))

assignments = json.loads(json.dumps(assignments_raw))

# gets raw assignments
for section in assignments:
    for assignment in section:
        due_date_str = assignment.get('due', '')
        if due_date_str:
            due_date = datetime.strptime(due_date_str.split(" ")[0], "%Y-%m-%d").date()
            yesterday = (datetime.now() - timedelta(days=4)).date()
            if due_date > yesterday:
                upcoming_raw.append({
                    'id': assignment['id'],
                    'title': assignment['title'],
                    'description': assignment['description'],
                    'due': assignment['due'],
                    'grading_category': assignment['grading_category']
                })

# with open("output.json", "w") as q:
#     json.dump(upcoming, q)

# sorts to final upcoming list
upcoming = sorted(upcoming_raw, key=lambda x: x['due'])

# for assignment in upcoming:
#     print(f"Title: {assignment['title']}, Due Date: {assignment['due']}")



# GRADES

grades_raw = []

for section_id in section_ids:
    grades_raw.append(sc.get_user_grades_by_section(user_id, section_id))


grades = json.loads(json.dumps(grades_raw))

# for section in grades:
#     for index, grade in enumerate(section):
        # print(grade)
        # print(f"{grade['section_id']} | {grade['final_grade'][0]['grade']}")
        # for index, grade_category in enumerate(grade):
            # print(index)
        #print(f"{grade['grading_category'][index]['title']} ({grade['grading_category'][index]['weight']})")
        # print(f"{grade['final_grade'][0]['grading_category'][index]['grade']}")


for section in grades:
    for grade in section:
        print(grade['section_id'])
        period_grade = grade['final_grade'][0]['grade']

    for period in grade['period']:
        print(f"{period['period_title']} ({period['period_id']}) | {period_grade}")
        
    for category in grade['grading_category']:
#        for category_grade_temp in grade['final_grade'][0]['grading_category']:
            category_title = category['title']
            category_weight = category['weight']
#            category_grade = category_grade_temp['grade']
            print(f"{category_title} ({category_weight})")
            for category_grade_temp in grade['final_grade'][0]['grading_category']:
                category_grade = category_grade_temp['grade']
                print(f"{category_title} ({category_grade})")

#

'''
Class [section_id]
    Semester (Weight) [period_title (period_id)] | Overall Grade
        Category (Weight) | Overall Grade
            Assignments (Due) | Grade | Comment
'''

# with open("output.json", "w") as q:
#     json.dump(grades, q)

# for section in grades



'''
for each section
    get section id and print
    for period[0]
        get period_title; period_id and print
        get final_grade['grade'] and print
        for each grading_category
            print title (weight) | final_grade of grading_category of grade
            search through all assignments
                if same id
                    print assignment (due) | grade | comment if any
'''