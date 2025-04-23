from flask import Flask,request,jsonify
from app.database import db_connection


# call methods of app.database
student_collection = db_connection()

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1> This is student home page</h1>'


# Add all student data
@app.route('/add_student', methods=["POST"])
def add_student():

    # Data in JSON format
    data    = request.get_json()

    stud_id     = data.get('stud_id','')
    name        = data.get('name','')
    roll_no     = int(data.get('roll_no',''))
    email_id    = data.get('email_id','')
 
    if not all([stud_id, name, roll_no,email_id]):
        return jsonify({'message': 'misssing students details.'})

    # list of courses added 
    courses     = data.get('courses',[])
    
    # VALIDATE COURSES
    course_data = []
    for course in courses:
        if all(key in course for key in ('course_name', 'marks', 'grade')):
            course_data.append({
            'course_name': course['course_name'],
            'marks': course['marks'],
            'grade': course['grade']
        })
        else:
            return jsonify({'Message':'update course fileds not found'})
    

    student = {
        'stud_id': stud_id,
        'name': name,
        'roll_no': roll_no, 
        'email_id': email_id,
        'courses': courses
    }

    # Add single studen data to DB
    student_collection.insert_one(student)

    return jsonify({'Message': f'Student {name} added to database Successfully..!'})

# update student
@app.route('/update_student/<stud_id>', methods=['PUT'])
def update_student(stud_id):

    data = request.get_json()
    student = student_collection.find_one({'stud_id':stud_id})

    if not student:
        return jsonify({'Message': 'Student not Found'})
    
    update_data = {}
    # update student fileds
    for field in ['name','roll_no','email_id']:
        if field in data:
            update_data[field] = data[field]


    # update courses filed
    if 'courses' in data:
        updated_courses = []
        for course in data['courses']:
            if all(key in course for key in ('course_name', 'marks', 'grade')):
                updated_courses.append({
                'course_name': course['course_name'],
                'marks': course['marks'],
                'grade': course['grade']
            })
            # else: 
            #     return jsonify({'Message':'update course fileds not found'})

        # update course data        
        update_data["courses"] = updated_courses
    
    if not update_data:
        return jsonify({{'Message':'update data not validated'}})
    
    # update specific student data
    student_collection.update_one({'stud_id': stud_id}, {'$set':update_data})

    return jsonify({'Message': 'Student Data updated Sucessfully..!!'})


# display all student
@app.route('/display_students', methods=['GET'])
def display_students():
    res = list(student_collection.find({}, {'_id': 0}))
    if not res:
        return jsonify({'Message': 'Student data not found'})
    else:
        return jsonify({'Student_Data': res})

# display particular student
@app.route('/get_student/<stud_id>', methods=['GET'])
def get_student(stud_id):
    res = student_collection.find_one({'stud_id': stud_id}, {'_id': 0})
    if not res:
        return jsonify({'Message': f'Student with {stud_id} not found'})
    else:
        return jsonify({f'Student {stud_id}': res})

# Delete specific student
@app.route('/delete_student/<stud_id>', methods=['DELETE'])
def delete_student(stud_id):

    res = student_collection.delete_one({'stud_id': stud_id})
    if not res:
        return jsonify({'Message': f'{stud_id} not found'})
    else:
        return jsonify(f'{stud_id} successfully deleted..!!')
    


if __name__ == '__main__':
    app.run(debug=True)

