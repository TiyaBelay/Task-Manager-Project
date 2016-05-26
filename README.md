Task Manager - Hackbright porject
--------------------------------------------------------------------------------
Registered application with Google Developers Console and received my OAuth 2.0 
credentials.

Virtual environment created for this project with the following installed:
    Google api libraries for python using pip 

Implementing Gmail RESTful API:
    Used Google Sign-in to provide the user secure login and to avoid the user from
    having to remember an additional username and passwords. User signs in and chooses 
    their account, they would have to allow authorization for the task manager in order 
    to access their inbox.

Day 3 of Project:
Command_line based application:
My command_line py file currently authenticates user and runs through the authentication flow
providing access permission to modify inbox. When running file, it will also pull messages
based on the labelid which is currently set to 'INBOX'. It currently outputs header information
as a dictionary. Next step is to filter through the inbox to have it return a list of the information
based on my data model, which will be seeded into my db and outputted onto the inbox page.

I came across a blocker:

redirect_uri was set in my console to render my inbox web page. After coming across the error that
my redirect uri was incorrect after running my command_line file and making sure that all my redirect_uri's
were following what was reflected in my dev console, it turned out that the redirect_uri should be set to
google's standard redirect_uri: http://localhost:8080/ which wasn't documented accurately


Day 4-6 of project:
Completed functioning of OAuth
Parsed through API dictionaries to grab headers which are being displayed on the inbox page. Currently just 
working on receiving 1 message to avoid delay with my pages running.
Linked message to the body and built a page to handle the message body. Thinking of using Angular to have 
the messages run on the same page as inbox. Will do this in my second sprint if I have the time
I still need to refractor my code and clean it up but won't do this till the end of the week when I have a 
functioning app.

I came across a couple of blockers:
Parsing through the dictionary received from the message. It took most of my time and a lot of trial and error
Since the dictionary for the headers were set up with non unique keys, I had to create my own dictionary where
I assigned the values of the keys from gmail's dictionary to be keys in my own dictionary for cleaner data.

Parsing through the message body was also a bit challenging. After much research I decided to continue testing
in the command-line application that I had set up previously to make sure to decode the body of my message and
have it display on my web page.

Day 7-8:
Completed working on linking the subject to the message body and storing some of my messages in my db. I've linked the Subject to 
message body. The message body is currently in a plain text format since it requires multi text parsing that I will be looking at
later this week. When clicking on an email, the 'create task button' is available on the top right side of the page. Currently
I've been rendering a page for the inbox, the body of the message, and the tasks. This will be changing into a 1-page browser
during my second sprint where I will be using Angular. Currently, I'm just concentrating on the functionalities. Next when submitting
the task, it routes to a page where the list of tasks will be living. I will be working on populating the list of tasks next.

#My inbox Page - 
![Screenshot of my inbox](https://cloud.githubusercontent.com/assets/18127030/15580939/5bbdd24e-231f-11e6-8aac-eb412027254f.png)

#Task 
![Screenshot of task page](https://cloud.githubusercontent.com/assets/18127030/15580988/8c6b6d70-231f-11e6-829f-1ea2b8d4bb8d.png)

#Second sprint:

Day 1-2:
Cleaning up my web pages and my task list page. Also integrated with Slack using their
inoming webhook without using their OAuth. Posting notifications is successful when a task is created. Need to continue working on notification to post with the title and when the task is completed. 

![Screenshot of slack notification](https://cloud.githubusercontent.com/assets/18127030/15520759/c70c27ee-21bc-11e6-9358-ef18171c15f8.png)

Day 3-4:
Refractored code on my server.py file and worked on search engine for task
![Screenshot of list of tasks](https://cloud.githubusercontent.com/assets/18127030/15579175/5769455e-2318-11e6-87f4-f84d7635d639.png)









