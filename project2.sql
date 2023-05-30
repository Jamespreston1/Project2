-- Project 2 - Calendar Application 


CREATE TABLE if not exists meetings (
   meeting_id SERIAL PRIMARY KEY,
   owner_name TEXT NOT NULL,
   meeting_subject TEXT NOT NULL,
   meeting_time TEXT NOT NULL,
   location TEXT NOT NULL CHECK (location IN ('Meeting Room 1', 'Meeting Room 2', 'Meeting Room 3', 'Meeting Room 4', 'Meeting Room 5')),
   attendees TEXT[]
);

-- adding in the second table 

CREATE TABLE if not exists users (
    id serial PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    password TEXT
);