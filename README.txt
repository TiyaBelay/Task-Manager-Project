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

I came across a blockage:
    - redirect_uri was set in my console to render my inbox web page. After coming across the error that
    my redirect uri was incorrect after running my command_line file and making sure that all my redirect_uri's
    were following what was reflected in my dev console, it turned out that the redirect_uri should be set to
    google's standard redirect_uri: http://localhost:8080/ which wasn't documented accurately










