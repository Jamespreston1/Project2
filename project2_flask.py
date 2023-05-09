from flask import Flask, render_template, request, redirect
import psycopg2

# psycopg 
connection = psycopg2.connect(dbname='calendar', user='postgres', port=5433, password='Flugenhimen10!')
cursor = connection.cursor()

# Flask app
app = Flask(__name__)

# Homepage 
@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/meeting_form', methods=["GET", "POST"])
def meeting_form():
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

if __name__ == '__main__':
    app.run(debug=True)
