track that

**Destination Unknown** is a mischievous roulette mystery trip generator that can sweep you away on a spontaneous adventure. Users can log in with their Uber accounts, compose a story for their ideal escape, and see a top-rated mystery destination unfold on a story-book map. The destination contains just enough information to pique one’s interest but not spoil the surprise. Users can request a ride from Uber directly via Destination Unknown, complete with text message confirmation. Destination Unknown also provides users with insights into their own “Inside Out”: curiosity stats, mood triggers, and celebrity alter-egos. 

As the saying goes, “*Only the curious have something to find*.” Destination Unknown will encourage you to forge a bolder path.

Destination Unknown web app and logo are created with love by **Shijie Feng** <<shijie.feng@gmail.com>>. You can connect with Shijie on [LinkedIn](https://www.linkedin.com/in/shijiefeng), [Twitter](https://twitter.com/Neon_Badger), and [Medium](https://medium.com/@ShijieF).


# Table of Contents
* [Tech stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [Deployment](#deployment)
* [Version 2.0](#future)

## <a name="technologies"></a>Technologies

**Destination Unknown** is built on a Flask server (written in Python) and uses a PostgreSQL database. The application seamlessly integrates with Uber, Yelp, Mapbox, and Twilio APIs and adopts a modernized UI that supports full-screen video background, natural language form, and JavaScript/jQuery/CSS animation effects. While using Destination Unknown, users generate live data, and the application queries the database and visualizes the information with jQuery and D3.js.

Tech Stack:
* Frontend: JavaScript, [jQuery](https://jquery.com/), [AJAX](http://api.jquery.com/jquery.ajax/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [D3.js](https://d3js.org/), [Bootstrap](http://getbootstrap.com/2.3.2/), [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)
* Backend: [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/)
* Database: [Flask - SQLAlchemy](http://flask.pocoo.org/), [PostgreSQL](http://www.postgresql.org/)
* API: [Uber](https://developer.uber.com/), [Yelp](https://www.yelp.com/developers/documentation/v2/overview), [Mapbox](https://www.mapbox.com/developers/), [Twilio](https://www.twilio.com/docs/api/rest)

(Dependencies are listed in [requirements.txt](requirements.txt).)

## <a name="features"></a>Features

####Full-Screen Video Background
![](/static/img/Landing_1.gif)

The landing page embeds HTML5 video in the background for a stunning, fluid user experience. The video background is supported in all modern browsers (>IE8). For browsers incompatible with HTML5 video, a static full-screen picture is shown instead.

I create my own video for the app's background. To make the video background work on the web, I host three formats:
* MP4 – a container for H.264 video and AAC audio
* Ogg – a container for Theora video and Vorbis audio
* WebM – a container intended primarily for use in the HTML5 video tag

####Login with Uber

When the mouse hovers to the center of the landing page, a hidden login button appears. I opt for this "hide-and-seek" button effect to augment the app's "*Be Curious, Be Bold*" message.

User login is handled through Uber's OAuth 2.0, following the client-side authorization flow. 
![](/static/img/Login_2.gif)

* _What does Destination Uknown's OAuth flow look like?_

For a user to access Destination Unknown's content and request in-app Uber services, the app needs authorization from Uber and redirects the user to Uber's Authorization server, where the user is asked to authenticate (if not already logged in) and then authorize the requested permissions. After successfully being granted access, the app is redirected from Uber to the redirect uri address, including an access token that can be used directly by the app to request information or perform operations on behalf of the user. 

The access token is then encrypted and stored on the Flask session, and the user's subsequent login will not prompt for the authorization dialog if the user is logged in and has previously approved the same permissions. For more, please see the [Uber API documentation](https://developer.uber.com/docs/authentication).

####User Profile and Avatar

Upon a user's successful login through Uber, the app accesses the user's Uber profile and greets the user with the user's name and Uber profile picture on top of the search page. With a mouseover, you can turn into a curious cat!
![](/static/img/Avatar_1.gif)

####Natural Language User Interface

Destination Unknown experiments with a novel UI concept to transform the conventional Q&A-style forms for user input. The app implements a Natural Language Form ("NLF"), embedding input fields inside sentences to make filling out a form as engaging and as writing a mini story, and as easy as talking to a friend. 

In addition to asking for the user's current location, desired activity type, and preferred destination, the form collects the user's mood information at the time of search by asking about the user's feeling, self-description, and celebrity alter-ego. For more design inspirations on NLF, please visit this [blog](http://www.jroehm.com/2014/01/ui-pattern-natural-language-form/).
![](/static/img/NLP_Form_1.gif)

####Business Discovery

Destination Unknown uses the Yelp API behind the scene to determine the list of businesses to choose from. Once the user fills out the form and clicks the "Find Destination" button, the application sends the search parameters to Yelp API's search endpoint. After Yelp returns results that fit the search criteria, the app randomly selects one of the highest-rated businesses for the user's consideration, revealing only the business's Yelp ratings, review snippet, and business categories -- just enough information to get you curious and excited!
![](/static/img/Destination_1.gif)

####Story Book Map

The background map is composed of a Mapbox (built on Leaflet) map with custom markers and popups, custom CSS, Bootstrap, and jQuery. The theme of the map is a customized [picture book atlas](https://github.com/mapbox/mapbox-studio-picture-book.tm2) designed in Mapbox Studio. 

The map has a transparent nav bar overlay on top, displaying the user's phone number, current location, and a link to view the user's stats. The map shows two custom-made markers: one for the user with a popup window greeting the user and indicating the user's current location, and the other for the mystery destination with a popup window containing the selected business information.

The user has the option of returning to the previous search page, or requesting Uber to Destination Unknown. 

####Uber Ride Request (sandbox)

A user can click "Call Uber" button and a modal window will appear. After confirming the ride request, the app sends an AJAX request to the Flask controller, sending along the geolocations of the user and the selected business. The app then uses the OAuth 2.0 credentials to instantiate a client object, makes a request to Uber's v1/requests endpoint that returns Uber products in the vincinity of the user, and picks a UberX (or UberXL if no UberX is available). The app makes a sandbox ride request to Uber, changing product status to "accepted." After Uber grants the ride request, Uber returns a successful 200 status code, and the app can access the ride details including the driver's name and rating, the vehicle's make and model, and the estimated pickup. The "Call Uber" button is disabled and turns into "Uber Called." For more, please visit [Uber API tutorial](https://developer.uber.com/docs/tutorials-rides-api).

![](/static/img/Call_Uber_2.gif)

####Twilio Text Message Confirmation

When the user's ride request is successful, the app sends the ride information to the user via the Twilio SMS API.

####Live User-Generated Data

As the user fills out the form, all the form fields -- including the user's mood, trip description, and alter-ego -- are written into the database, along with information about the destination generated by the application. When the user requests Uber, the uber_request field in the searches table is updated accordingly.

####Curiosity and Mood Stats Visualization

The app makes SQLAlchemy queries into the database and returns the following data: the number of times the user has been curious and searched for a destination (curiosity stats), the number of times the user has been bold and requested Uber (boldness stats), and how many miles the user has traveled to Destination Unknown with Uber (in sandbox). With jQuery, these stats are shown with a flipping countup animation effect.
![](/static/img/Stats_1.gif)

The user can also view a donut chart illustrating the percentage of times the user selected his or her celebrity alter-egos, made with D3.js. The user can select and deselect the alter-ego in the legend to view the relative percentages.
![](/static/img/Donut_1.gif)
 
In addition, there is a chord diagram showing how the user's mood affects the activity choice, also made with D3.js. How does feeling anxious correspond to whether you want to eat out or work out? How does practicing zen relate to how you feel? Find out the answers here!

![](/static/img/Chord_2.gif)

## <a name="install"></a>Installation

If you want to get a copy of this project up and running on your local machine for development and testing purposes, here are the steps.

####Prerequisite

Install PostgreSQL (Mac OSX)

Use Sublime to edit the file in your home directory named .bash_profile:

``` $ subl ~/.bash_profile ``` 

Then, at the bottom of this file, add the following line (exactly):

``` export PATH=/Applications/Postgres.app/Contents/Versions/9.4/bin/:$PATH ``` 


####Set up

Clone this repository.

```
$ git clone https://github.com/neonbadger/DestinationUnknown.git
```
Create a virtual environment for the project.

```
$ virtualenv env
```
Activate the virtual environment.
```
$ source env/bin/activate
```
Install dependencies.
```
$ pip install -r requirements.txt
```
To enable the Uber, Yelp, and Twilio functionality, you should set up your own developer accounts and have your own sets of API keys and tokens. Examples of the config files are provided in the folder [config_example](config_example).

Run PostgreSQL (see the elephant icon active).

Create database with the name "trips" (do it once).
```
$ psql trips

$ dropdb trips

$ createdb trips
```
To run the app from the command line of the terminal, run
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i server.py
```

## <a name="testing"></a>Testing

There is a test suite encompassing Unittest, Integration Test, and Selenium Test written for Destination Unknown. 

Currently the coverage is 67%.

![](/static/img/coverage1.png)

To run the test suite on command line:
```
$ coverage run --omit=env/* test.py
```
For report:
```
$ coverage report -m
```
For html of the the report (which will create a htmlcov folder):
```
$ coverage html

$ open htmlcov/index.html
```

## <a name="deployment"></a>Deployment

Deployment details to come!

## <a name="future"></a>Version 2.0

Future features to come:

- [ ] Drag and drop the user's geolocation
- [ ] User rate and review the Destination Unknown post Uber trip
- [ ] Multiple legs of trip
- [ ] Incorporate machine learning to predict user's preference
- [ ] More testing

## <a name="author"></a>Author

**Shijie Feng** (Github: [neonbadger](https://github.com/neonbadger)) is a software engineer and lives in the San Francisco Bay Area with her husband Blake and cat Mylo.

## <a name="license"></a>License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.

## <a name="acknowledgments"></a>Acknowledgments

* Hat tip to my wonderful husband Blake for love and support during Hackbright!
* Thanks to my mentors Terry, Sri, Monica, advisor Ally, and my Hack13right sisters for guidance and support!



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


#Task 
![Screenshot of task page](https://cloud.githubusercontent.com/assets/18127030/15828472/44675bee-2bc4-11e6-8eed-3d975848da14.png)

#Second sprint:

Day 1-2:
Cleaning up my web pages and my task list page. Also integrated with Slack using their
inoming webhook without using their OAuth. Posting notifications is successful when a task is created. Need to continue working on notification to post with the title and when the task is completed. 

![Screenshot of slack notification](https://cloud.githubusercontent.com/assets/18127030/15828427/1e266e48-2bc4-11e6-93b9-bb536fe76e07.png)

Day 3-4:
Refractored code on my server.py file and completed search engine for tasks
![Screenshot of search query](https://cloud.githubusercontent.com/assets/18127030/15828498/63c17b00-2bc4-11e6-9d48-c777ac172e59.png)









