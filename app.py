from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

# Flask app
app = Flask(__name__)

# setting secret key used to 'sign' session values
app.config["SECRET_KEY"] = "Your Secret Key Here"

# Homepage 
@app.route('/')
def homepage():
    user_id = session.get("user_id", "")
    if user_id:
        # now you have user_id, you know who is logged in and can display customized content 
        return render_template("home.html")
    else:
        # no session so need to login
        return redirect("/login")

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    print(session)
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # check for existence of user in DB and handle appropriately
        # if user exists, set the session variable and go back to "/";
        # otherwise, display error page or refresh "/login"
        connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"))
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users where email='{email}' and password='{password}'")
        logincheck = cursor.fetchall()
        connection.commit()
        print(logincheck)
        print(request.form)
        if not len(logincheck):
            return redirect("/login?error=Invalid Credentials")
        # Dummy check - replace with actual database query check
        if email == logincheck[0][3] and password == logincheck[0][4]:
            session["user_id"] = email
            return redirect('/')
        else:
            return "Invalid credentials. Please try again."
        
        
    else:
        if request.args.get("error"):
            return render_template("login.html", error=request.args.get("error"))
        return render_template("login.html")
    



# Second Attempt at signup route 

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get form data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Here you can add data to your database.
        # Make sure to securely hash the password before storing it!

        # Dummy check - replace with actual database query check
        if password == confirm_password:
            connection = None
            try:
                connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), port=os.getenv("DB_PORT"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"))
                cursor = connection.cursor()
                cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, password))
                connection.commit()
                session["user_id"] = email
                return redirect('/')
            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)
                error_detail = f"{error_type}: {error_msg}"
                if connection is not None:
                    connection.rollback()
                return f"Error inserting data into database: {error_detail}"
            finally:
                if connection is not None:
                    connection.close()
        else:
            return "Passwords do not match. Please try again."
    else:
        return render_template("signup.html")
    

# Signout route 
@app.route('/logout')
def logout():
    print(session)
    if "user_id" in session:
        del session["user_id"]
        return redirect('/login')
    else:
        return redirect('/login')
    

# New Meeting Add
@app.route('/meetings/new', methods=["GET", "POST"])
def meeting_form():
    connection = psycopg2.connect(dbname='calendar',user = 'postgres',port=5433, password = 'Flugenhimen10!' )
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
    connection = psycopg2.connect(dbname='calendar',user = 'postgres',port=5433, password = 'Flugenhimen10!' )
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
    connection = psycopg2.connect(dbname='calendar',user = 'postgres',port=5433, password = 'Flugenhimen10!' )
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
    connection = psycopg2.connect(dbname='calendar',user = 'postgres',port=5433, password = 'Flugenhimen10!' )
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

