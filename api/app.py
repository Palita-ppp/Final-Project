from flask import Flask, jsonify
from flask_cors import CORS
import requests

server_ip = "http://localhost:3000"

app = Flask(__name__)
CORS(app)

# ปิดการใช้งาน core เพื่อให้รองรับการเชื่อมต่อจากภายนอกได้
app.config['CORE_ENABLED'] = False

# สร้าง route สำหรับดูลิสต์ของพนักงานทั้งหมด
@app.route("/employees")
def employees():
    employees = {"83db35f": "lambo", "839af2e": "tesla", "e3c52f": "tesla", "139cfc10": "lambo"}
    return jsonify("employees", employees)

# สร้าง route สำหรับดูข้อมูลของพนักงานแต่ละคน
@app.route("/employee/<employee_id>")
def employee(employee_id):
    url = server_ip + "/" + employee_id
    response = requests.get(url)
    if employee_id == "83db35f":
        response = {"employee": employee_id, "car_name": "lambo", "noted": response.json()}
    elif employee_id == "839af2e":
        response = {"employee": employee_id, "car_name": "tesla", "noted": response.json()}
    elif employee_id == "e3c52f":
        response = {"employee": employee_id, "car_name": "tesla", "noted": response.json()}
    elif employee_id == "139cfc10":
        response = {"employee": employee_id, "car_name": "lambo", "noted": response.json()}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)