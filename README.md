What does this do?
===========

This script checks an email inbox via IMAP for a message from IFTT that triggers a precipitation forecast for an upcoming Google Calendar event's location and mails the result.



Requirements
============

A Dark Sky API key (https://developer.darkskyapp.com/)
An IMAP email inbox
A box to run darkskymail.py as a service
An IFTT.com account



Directions
==========

1.  Clone the project into a directory on your box.
2.  Save this IFTTT.com Recipe and update the "to" email address to your Recipes (http://path_to_iftt_recipe)
3.  Edit the settings.py file. Use the comments to guide you.
4.  Run darkskymail.py
5.  Profit.

Once DarkSkyMail is running, be sure to include a valid address in the "location" field of the calendar event!


To Do
=====

1.  Add looping to darkskymail.py and adhere to the fetch_interval in settings.py
2.  Gracefully handle missing/bad addresses in the email.



FAQ
===

1.  Will this work internationally?

	I don't see why not.

2.  Receiving the message only 15 minutes before the event starts is kind of useless to me.  Can I change this?
	
	Currently, IFTT.com will only trigger the email 15 minutes before the event, and there is no way to alter this.  I would recommend complaining to them that you'd like to see at least SOME options (15 min, 30 min, 1 hr, etc.)  My original plan was to simply use a Google event's "email alert" feature, but there is seemingly no way to programmatically format the email to include a) just the data I want and b) in a format that's easily parseable.

3.  What does the email data look like?
	
	The body of an event email is literally just the start date and time of the event, then a semicolon, and then the address you entered in the "location" field for the event. Here's an example:

	October 13, 2012 at 01:21AM;1600 Amphitheatre Pkwy, Mountain View, CA 94043