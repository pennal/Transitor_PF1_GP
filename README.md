Transitor
==============

Before you begin, make sure that you have all of the required packages installed, see below for details.

In order to run the program, cd to the Transitor folder, and run main.py using 

    python3 main.py

This will start the server and allow you to visit the page at the address [127.0.0.1:5000](127.0.0.1:5000)
Hosted Version
--------------
A hosted version can be found at <a href="http://transitor.herokuapp.com/">http://transitor.herokuapp.com/</a>

Requirements
--------------
The program was designed to run on Python 3.4.1, so that is needed. In order to run properly, you also need the following modules:

| Module           | Command to install          |
|------------------|-----------------------------|
| Flask            | pip3 install Flask          |
| Beautiful Soup 4 | pip3 install beautifulsoup4 |
| Requests         | pip3 install requests       |
| iCalendar        | pip3 install icalendar      |


sudo is recommended when installing packages, but not required. 

How does it work?
-----------------
When you run the main.py file, a local server gets created for you and the first page is loaded. Everytime you ask for information (departure times, weather, ...) the information gets processed by the server code (Python) and the results are then displayed to you, with pages generated on the spot. This allows every user to have their customized results. 

Authors
-------
This project was created by the following people:
* [@pennal](http://github.com/pennal)
* [@Dcamma](http://github.com/DCamma)
* [@alexandernorth](http://github.com/alexandernorth)
* [@VictorMion](http://github.com/VictorMion)
