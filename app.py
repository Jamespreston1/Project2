from flask import Flask, render_template, request, redirect
import psycopg2
import os
# psycopg 
connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
cursor = connection.cursor()

# Flask app
app = Flask(__name__)

# Homepage 
@app.route('/')
def homepage():
    return render_template("home.html")

# New Meeting Add
@app.route('/meetings/new', methods=["GET", "POST"])
def meeting_form():
    connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
    cursor = connection.cursor()
    if request.method == "POST":
        owner_name = request.form["owner_name"]
        meeting_subject = request.form["meeting_subject"]
        meeting_time = request.form["meeting_time"]
        location = request.form["location"]
        attendees = request.form["attendees"].split(',')
        
        try:
            cursor.execute("INSERT INTO meetings (owner_name, meeting_subject, meeting_time, location, attendees) VALUES (%s, %s, %s, %s, %s)", (owner_name, meeting_subject, meeting_time, location, attendees))
            connection.commit()
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            error_detail = f"{error_type}: {error_msg}"
            connection.rollback()
            return f"Error inserting data into database: {error_detail}"
        
        return redirect('/')
    else:
        return render_template("meeting_form.html", meeting=None)
    

# Appointment View Page
@app.route('/meetings')
def test():
    connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
    cursor = connection.cursor()

    # get data from database
    cursor.execute('SELECT * FROM meetings')
    results = cursor.fetchall()
    print(results)
    sorted_results = []
    for result in results:
        sorted_results.append({
            "meeting_id":result[0],
            "Meeting_time": result[3], 
            "Owner_name" :result[1],
            "Meeting_subject":result[2],
            "Location":result[4],
            "Attendees":', '.join(result[5])
        })
    return render_template("appointment_view.html",meetings=sorted_results)    

# Edit Meeting View 
@app.route('/meetings/edit/<int:id>', methods=['GET', 'POST'])
def edit_meeting(id):
    connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
    cursor = connection.cursor()
    if request.method == 'POST':
        new_data = request.form
        print("new_data",new_data)  
        # update data in the database
        try:
            cursor.execute('''
            UPDATE meetings SET 
            meeting_time = %s,
            owner_name = %s,
            meeting_subject = %s,
            location = %s,
            attendees = %s
            WHERE meeting_id = %s
        ''', (new_data['meeting_time'], new_data['owner_name'], new_data['meeting_subject'], new_data['location'], new_data['attendees'].split(', '), id))
            connection.commit()
            return redirect('/meetings')
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            error_detail = f"{error_type}: {error_msg}"
            connection.rollback()
            return f"Error inserting data into database: {error_detail}"
       
    else:
        # get data from database
        cursor.execute('SELECT * FROM meetings WHERE meeting_id = %s', (id,))
        result = cursor.fetchone()
        meeting = {
            "meeting_id":result[0],
            "Meeting_time": result[3], 
            "Owner_name" :result[1],
            "Meeting_subject":result[2],
            "Location":result[4],
            "Attendees":', '.join(result[5])
        }
        return render_template("edit_meeting.html", meeting=meeting)    


# Delete Meeting View 
@app.route('/meetings/delete/<int:id>', methods=['GET'])
def delete_meeting(id):
    connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
    cursor = connection.cursor() 
    # delete data from database
    
    try:
        cursor.execute('DELETE FROM meetings WHERE meeting_id = %s', (id,))
        connection.commit()
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        error_detail = f"{error_type}: {error_msg}"
        connection.rollback()
        return f"Error inserting data into database: {error_detail}"
    return redirect('/meetings')


if __name__ == '__main__':
    app.run(debug=True)

