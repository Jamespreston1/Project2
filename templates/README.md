<!-- Project 2 README file  -->


Project 2 - Calendar Application 

For Project 2, I decided to contruct a Calendar Application that lets people create, modify and delete appointments. 

It also allows you to view all appointments that have been created in a calendar like format. 

My approach was relatively simple, composed of only 5 key routes on my application to fulfil the CRUD requirements. 

They were to: 
1: Build a homepage which rendered a HTML for basic navigation
2: Add in a new meeting using a GET + POST method
3: View all the meetings that have been build through the appointment scheduling page 
4: Edit the meetings that have been made on the HTML interface for appointment scheduling 
5:  Delete the meetings on the HTML interface

Challenges: 
 ~ Getting my routes to work! I learned a lot in this section as I fought capitalisation issues between files holding me back. I eventually found a way to handle the erros using a Try & Except system which lead me to find my way out of this hole. 

 ~ Integrating with Render dashboards - With the help of VIshal, I was able to get this to work. Right up until my final commit, I didn't have the right Github account linked, didn't have my database pushed onto Render, and wasn't using the web service appropriately.  

 ~ Setting up a CSS with different classes to be able to let it apply to different tags across the various HTML documents that I was using linked via the {% extends "base.html" %} method for example. I was only able to set this up for the homepage with the body colour. 

Technologies Used: 
~ HTML, CSS were used to be able to integrate with the Jinga template method and render the files through my python routes in my application 
~ Render was used as the hosted service to be able to publish my database and my front end product on the web 
~  Python + flask were used as the key element here to build my application in the virtual environment  

Link to the hosted application: https://project2-zj8q.onrender.com/ 