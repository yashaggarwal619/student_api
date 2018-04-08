from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util

MONGODB_URI = "mongodb://test:test@ds233748.mlab.com:33748/student_record"
client = MongoClient(MONGODB_URI)
db = client.get_database("student_record")
student_record = db.student_records

app = Flask(__name__)


@app.route('/')
def index():
	return "Welcome to student records API!\nCreated by yash"


@app.route('/students/', methods=['GET', 'POST'])
def student_list():
	if request.method == 'GET':
		students = list(student_record.find())
		return json_util.dumps(students)

	elif request.method == 'POST':
		roll_no =int(request.form.get("roll_no"))

		if student_record.find_one({"roll_no":roll_no}):
			return jsonify({"error": "User already registered!"})

		student = {}
		student['roll_no'] =int(roll_no)
		student['name'] = request.form.get("name")
		student['age'] = request.form.get("age")
		student['branch'] = request.form.get("branch")

		student_record.insert_one(student)

		return jsonify({"result": "Student successfully registered!"})
#python return data,code

@app.route('/student/<int:roll_no>/', methods=['GET', 'PATCH', 'DELETE'])
def get_student(roll_no):
	student = student_record.find_one({"roll_no":roll_no})
	if not student:
		return jsonify({"error": "Student is not registered."}), 404

	if request.method == 'GET':
		return json_util.dumps(student)
	elif request.method == 'PATCH':
		student_record.update_one({'roll_no':roll_no}, {'$set':request.form})
		return jsonify({"result": "Student record successfully updated!"})
	elif request.method == 'DELETE':
		student_record.delete_one({'roll_no':roll_no})
		return jsonify({"result": "Student record successfully deleted!"})
		

if __name__ == "__main__":
	app.run(port=8000, use_reloader=True, debug=True)