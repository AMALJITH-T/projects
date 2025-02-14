from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the path for the folder where uploaded images will be stored
app.config['UPLOAD_FOLDER'] = 'static/images/'

# Define allowed file extensions (adjust as needed)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class Employee:
    def __init__(self, id, name, age, salary, experience, department, image_filename=None):
        self.id = id
        self.name = name
        self.age = age
        self.salary = salary
        self.experience = experience
        self.department = department
        self.image_filename = image_filename

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

employees = [] 
count = 0   

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None


@app.route('/')
def index():
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        global count
        image = request.files['image']
        image_filename = None

        if image and allowed_file(image.filename):
            # Save the image file to the specified folder
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        employee = Employee(
            int(request.form['id']),
            request.form['name'],
            int(request.form['age']),
            float(request.form['salary']),
            int(request.form['experience']),
            request.form['department'],
            image_filename=image_filename
        )
        employees.append(employee)
        count += 1
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/index')
def go_to_index():
    return redirect(url_for('index'))

@app.route('/edit_employee_form/<int:id>', methods=['GET', 'POST'])
def edit_employee_form(id):
    for employee in employees:
        if employee.id == id:
            if request.method == 'POST':
                employee.name = request.form['name']
                employee.age = int(request.form['age'])
                employee.salary = float(request.form['salary'])
                employee.experience = int(request.form['experience'])
                employee.department = request.form['department']
                return redirect(url_for('index'))
            return render_template('edit.html', employee=employee)
    return 'Employee not found', 404

@app.route('/search', methods=['GET', 'POST'])
def search_employee():
    if request.method == 'POST':
        search_term = request.form['search_term'].lower()
        results = [employee for employee in employees if search_term in employee.name.lower()]
        return render_template('search_results.html', results=results)

    return render_template('search.html')

@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    for employee in employees:
        if employee.id == id:
            employees.remove(employee)
            break
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
