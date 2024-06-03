from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import sqlite3 as m
import smtplib

my_email="nigaa3400@gmail.com"
password="fbmq tzcv cvpx dymg"

connection=smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email,password=password)

con=m.connect("students.db")
cur=con.cursor()
cur.execute("Create table if not exists users(id integer primary key, username text, password text)")
con.commit()
cur.execute("Create table if not exists students(id INTEGER Primary key, name text, father text, mother text, email text, address text, phone text, dob datetime, gender char(1))")
con.commit()
cur.execute("Create table if not exists announcements(id integer primary key, title TEXT, desc TEXT)")
con.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///BTech23.db"
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

class Student(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(1), nullable=False)

    def __repr__(self) -> str:
        return f"{self.usn} - {self.name} - {self.section}"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usn = db.Column(db.Integer, db.ForeignKey('student.usn'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    present = db.Column(db.Boolean)

    student = db.relationship('Student', backref='attendances')

    def __repr__(self) -> str:
        return f"Attendance({self.usn} - {self.name} - {self.date} - {self.subject})"

batches = {
    'BTech 22': ['A', 'B', 'C'],
    'BSc 22': ['A', 'B', 'C'],
    'BTech 23': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'BSc 23': ['A', 'B', 'C']
}

ttBTech23 = {
    'A': {'Monday': ['BAP', 'LA', 'DSA', 'BAP'],
          'Tuesday': ['ESM', 'DSA', 'BAP', 'EEx'],
          'Wednesday': ['DSA', 'LA', 'Elective'],
          'Thursday': ['ES2', 'ESM', 'ESM', 'EEx'],
          'Friday': ['LA', 'BAP', 'DSA']},

    'B': {'Monday': ['ES2', 'DSA', 'BAP', 'ESM', 'BAP'],
          'Tuesday': ['DSA', 'BAP', 'ESM', 'EEx'],
          'Wednesday': ['ESM', 'DSA', 'BAP', 'Elective'],
          'Thursday': ['LA', 'ESM', 'LA', 'EEx'],
          'Friday': ['DSA', 'LA']},

    'C': {'Monday': ['BAP', 'ES2', 'DSA', 'LA'],
          'Tuesday': ['DSA', 'LA', 'DSA', 'EEx'],
          'Wednesday': ['ESM', 'BAP', 'Elective'],
          'Thursday': ['ESM', 'BAP', 'EEx'],
          'Friday': ['DSA', 'ESM', 'LA']}
}

@app.route("/", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        if request.form['submit'] == 'Sign In':
            username = request.form['username']
            password = request.form['pswd']
            con = m.connect("students.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cur.fetchone()
            cur.close()
            if user:
                return redirect("/index")  
            else:
                return render_template("sign-in.html",notfound=True)
        elif request.form['submit']=='Create':
            username = request.form['username']
            password = request.form['pswd']
            con = m.connect("students.db")
            cur = con.cursor()
            cur.execute("INSERT INTO USERS(username,password) values (?,?)", (username, password))
            con.commit()
            cur.close()
            return render_template("sign-in.html")
    return render_template("sign-in.html")

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/students",methods=['POST','GET'])
def students():
    if request.method=="POST":
        if request.form['submit']=='ADD':
            id=request.form["id"]
            name = request.form["name"]
            father = request.form["name_f"]
            mother = request.form["name_m"]
            email = request.form["email"]
            address = request.form["address"]
            phone = request.form["phone"]
            date = request.form["date"]
            gender=request.form["gender"]
            con=m.connect("students.db")
            cur=con.cursor()
            cur.execute("Insert into students values(?,?,?,?,?,?,?,?,?)",(id,name,father,mother,email,address,phone,date,gender))
            con.commit()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            return render_template("students.html", students=students)
        elif request.form["submit"] == "DELETE":
            id = request.form["id"]
            con=m.connect("students.db")
            cur=con.cursor()
            cur.execute("DELETE FROM students WHERE id=?", (id,))
            con.commit()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            return render_template("students.html", students=students)
        elif request.form["submit"] == "UPDATE":
            id=request.form["id"]
            name = request.form["name"]
            father = request.form["name_f"]
            mother = request.form["name_m"]
            email = request.form["email"]
            address = request.form["address"]
            phone = request.form["phone"]
            date = request.form["date"]
            gender=request.form["gender"]
            con=m.connect("students.db")
            cur=con.cursor()
            cur.execute("UPDATE students SET name=?, father=?, mother=?, email=?, address=?, phone=?, dob=?, gender=? WHERE id=?",
                        (name,father,mother,email,address,phone,date,gender,id))
            con.commit()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            return render_template("students.html", students=students)
        elif request.form["submit"]=="DISPLAY":
            con=m.connect("students.db")
            cur=con.cursor()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            return render_template("students.html", students=students)
        elif request.form["submit"]=="SEARCH":
            name = request.form["name"]
            con=m.connect("students.db")
            cur=con.cursor()
            cur.execute("SELECT * FROM students where name=?",(name,))
            students = cur.fetchall()
            return render_template("students.html", students=students)
    
    return render_template("students.html")

@app.route("/announcements",methods=['POST','GET'])
def announcements():
    con=m.connect("students.db")
    cur=con.cursor()
    cur.execute("Select * from announcements")
    q=cur.fetchall()
    if request.method=='POST':
        if request.form['submit']=='OK': 
            title=request.form['title'] 
            desc=request.form['desc']  
            s=cur.execute("Select * from students")
            for i in s:
                connection.sendmail(from_addr=my_email,
                    to_addrs=f"{i[4]}",
                    msg=f"Subject:{title}\n\n{desc}")
            cur.execute("INSERT INTO announcements(title, desc) values (?,?)",(title,desc))
            con.commit()
            q=cur.execute("Select * from announcements")
                
            return render_template("announcements.html",announcements=q)
    return render_template("announcements.html",announcements=q)

@app.route("/delete/<int:id>",methods=['GET','POST'])
def delete(id):
    con=m.connect("students.db")
    cur=con.cursor()
    cur.execute("DELETE FROM announcements WHERE id=?", (id,))
    con.commit()
    return redirect("/announcements")

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    con = m.connect("students.db")
    cur = con.cursor()
    
    if request.method == 'POST':
        if request.form['submit'] == 'OK':
            title = request.form['title']
            desc = request.form['desc']
            cur.execute("UPDATE announcements SET title = ?, desc = ? WHERE id = ?", (title, desc, id))
            con.commit()
            return redirect("/announcements")
    
    cur.execute("SELECT title, desc FROM announcements WHERE id = ?", (id,))
    announcement = cur.fetchone()
    con.close()
    
    return render_template('update.html', announcement=announcement, id=id)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    selected_batch = None
    selected_section = None
    students = None
    timetable = None
    selected_date = None
    selected_subject = None

    if request.method == 'POST':
        selected_batch = request.form.get('batch')
        selected_section = request.form.get('section')
        selected_date = request.form.get('date')
        selected_subject = request.form.get('subject')
        
        students = Student.query.filter_by(section=selected_section).all()
        
        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            day_of_week = date_obj.strftime('%A')
            timetable = ttBTech23.get(selected_section, {}).get(day_of_week, [])

        if 'mark_attendance' in request.form:
            return redirect(url_for('subject_attendance', subject=selected_subject, section=selected_section, date=selected_date))

    return render_template('attendance.html', 
                           batches=batches, 
                           selected_batch=selected_batch, 
                           selected_section=selected_section, 
                           students=students, 
                           timetable=timetable,
                           selected_date=selected_date,
                           selected_subject=selected_subject)

@app.route('/attendance/<string:subject>', methods=['GET', 'POST'])
def subject_attendance(subject):
    selected_section = request.args.get('section')
    selected_date = request.args.get('date')

    if request.method == 'POST':
        return redirect(url_for('attendance', batch='BTech 23', section=selected_section, date=selected_date))

    attendance_records = Attendance.query.filter_by(date=selected_date, subject=subject).all()
    return render_template('subject_attendance.html', 
                           subject=subject, 
                           attendance_records=attendance_records, 
                           selected_date=selected_date,
                           selected_section=selected_section)

@app.route('/insert_attendance', methods=['POST'])
def insert_attendance():
    date = request.form.get('date')
    subject = request.form.get('subject')
    selected_section = request.form.get('section')
    attendance_records = []

    for student_id in request.form.getlist('student_id'):
        student = Student.query.get(student_id)
        present = request.form.get(f'present_{student_id}') == 'on'
        
        attendance_record = Attendance(
            usn=student.usn,
            name=student.name,
            date=datetime.strptime(date, '%Y-%m-%d'),
            subject=subject,
            present=present
        )
        attendance_records.append(attendance_record)
        db.session.add(attendance_record)
    
    db.session.commit()
    return redirect(url_for('subject_attendance', subject=subject, section=selected_section, date=date))

@app.route('/insert_data')
def insert_data():
    with open('BTech23_USN.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            section, usn, name = row
            student = Student(usn=int(usn), section=section, name=name)
            db.session.add(student)
        db.session.commit()
    return 'Data inserted successfully'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
