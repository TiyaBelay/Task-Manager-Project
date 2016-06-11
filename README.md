track that

TrackThat is an application built to manage your emails and improve collaboration between teams without the need to use multiple external trackers. Users can view their email after logging in with Gmail and start creating tasks for important emails. Users have the ability to share it with teams on their slack channels notifying their teams when tasks are created, completed as well time of completion. TrackThat will maintain and display all tasks that have been created with the ability to easily search through tasks. 


# Table of Contents
* [Tech stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [Deployment](#deployment)
* [Version 2.0](#future)

## <a name="technologies"></a>Technologies
Backend: Python, Flask
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3
Database: PostgreSQL, SQLAlchemy
API: Gmail
Other: Slack Incoming Webhook

## <a name="features"></a>Features

![](https://cloud.githubusercontent.com/assets/18127030/15987140/bd1543be-2fd2-11e6-9258-138393a326b1.png)

Sign in with Gmail, where user authenticates and authorizes TrackThat to access their inbox. This is handled through Gmail's OAuth 2.0. This is done by first obtaining the OAuth credentials from [Google's developer's console](https://console.developers.google.com). TrackThat additionally obtains an access token from Google's Authorization server, sending the acces to Gmail API's in regards to the readonly scope. For more information, please see [Google's API documentation](https://developers.google.com/api-client-library/python/start/get_started).

####Inbox
Upon access, user is directed to the inbox page where they can view and read all of their emails as well as view the status of a tracked or untracked email.

![](https://cloud.githubusercontent.com/assets/18127030/15987223/19cdf562-2fd6-11e6-9d71-b705c9f98465.png)

####Email Message
Users can then click on an important email which displays the body of the message on the same page as the inbox using Javascript, jquery, and AJAX to maintain the integrity of the html.

![](https://cloud.githubusercontent.com/assets/18127030/15987243/a0a205e2-2fd6-11e6-8b8d-a14e54c899b4.png)

####Create Tasks
Users can then create tasks for important emails by filling in the task-related information in the modal. If the task needs to be shared with your team on Slack, just check the box and submit for automated notification to your team.

![](https://cloud.githubusercontent.com/assets/18127030/15987277/ac188102-2fd7-11e6-8832-e8396bc3acc0.png)

Immediate notification to team when task is shared and modal is submitted. This is done by sending a post ajax request to Slack using their incoming webhook.
![](https://cloud.githubusercontent.com/assets/18127030/15987289/299a86de-2fd8-11e6-8503-1d6e80251ba6.png)

####Task List & Search Engine
User is then redirected to the task list page where all tasks that were created are displayed by querying my postgres database.
![](https://cloud.githubusercontent.com/assets/18127030/15987340/da359384-2fd9-11e6-9d0a-2b0352e93fd4.png)

The search engine uses a SQLAlchemy-searchable library to do a full-text search on the task name in my flask server.
![](https://cloud.githubusercontent.com/assets/18127030/15987379/073e0fea-2fdb-11e6-81e2-c0f8b64c0839.png)

