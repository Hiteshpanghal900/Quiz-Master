from application.sec import datastore
from application.models import *
from werkzeug.security import generate_password_hash
from datetime import date

def upload_initial_data():
    from flask import current_app
    with current_app.app_context():
        db.create_all()
        datastore.find_or_create_role(name="admin", description="User is an admin")
        datastore.find_or_create_role(name="student", description="User is a student")
        if not datastore.find_user(email = "admin@gmail.com"):
            datastore.create_user(email="admin@gmail.com", password=generate_password_hash("admin"), roles=["admin"], qualification = "None", full_name="Admin")
        if not datastore.find_user(email="stud1@gmail.com"):
            datastore.create_user(email="stud1@gmail.com", password=generate_password_hash("stud1"), roles=["student"], qualification = "Graduate", full_name="Student 1")

        madsubject = Subjects(name = "MAD-I", description="This is the MAD-I subject containing of chapters like HTML, CSS & Python Flask.")
        mathsSubject = Subjects(name = 'Mathematics', description = 'Contains chapters like Linear Algebra & Simplification etc.')
        db.session.add_all([madsubject, mathsSubject])

        htmlMadSubject = Chapters(name = 'HTML', description = 'This teaches various html tags, inline as well as block.', subject_id = 1)
        cssMadSubject = Chapters(name = 'CSS', description = 'Filled with various techniques of designing and styling.', subject_id = 1)
        simplifyMathSubject = Chapters(name = 'Simplification', description = 'It contains various simplification arithmetic problems including complex as well as easy.', subject_id = 2)
        db.session.add_all([htmlMadSubject, cssMadSubject, simplifyMathSubject])

        htmlQuiz = Quiz(quiz_name='HTML Tags', chapter_id=1, start_date=date.today(), end_date=date(2025, 4, 2), time_duration=time(0, 30), total_score = 5)
        db.session.add(htmlQuiz)

        questions = ["Which tag is used to create a hyperlink in HTML?", "Which HTML tag is used to define a table row?", 
                    "Which tag is used for inserting a line break in HTML?", "Which tag is used to define the largest heading in HTML?",
                    "Which HTML tag is used to insert an image?"]

        options = [
            ["<link>", "<a>", "<href>", "<hyper>"],["<th>", "<tr>", "<td>", "<table>"],["<br>", "<lb>", "<break>", "<newline>"],
            ["<heading>", "<h6>", "<h1>", "<head>"],["<img>", "<picture>", "<image>", "<src>"]]

        answers = ["<a>", "<tr>", "<br>", "<h1>", "<img>"]

        for i in range(len(questions)):
            new_question = Questions(
                quiz_id = 1,
                question_statement=questions[i],
                option1=options[i][0],
                option2=options[i][1],
                option3=options[i][2],
                option4=options[i][3],
                correct_option=answers[i],
                question_score = 1
            )
            db.session.add(new_question)

        db.session.commit()