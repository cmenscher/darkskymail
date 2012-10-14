What does this do?
===========

This script checks an email inbox via IMAP for a message from IFTT that contains location and start time data for a Google Calendar event, triggered 15 minutes before it is scheduled to start. The script gathers the emails and emails a precipitation forecast for the Google Calendar event using the awesome Dark Sky API (https://developer.darkskyapp.com).  BUY THE APP! http://darkskyapp.com/


Requirements
============

A Dark Sky API key (https://developer.darkskyapp.com/)
An IMAP email inbox
A box to run darkskymail.py as a service


Directions
==========

1.  Clone the project into a directory on your box.
2.  Save this IFTTT.com Recipe and update the "to" email address to your Recipes (http://path_to_iftt_recipe)
3.  Edit the settings.py file. Use the comments to guide you.
4.  Run darkskymail.py
5.  Profit.

Once DarkSkyMail is running, be sure to include a valid address in the "location" field of the calendar event!  I am using the Google geocoding API, though, so it's quite forgiving.

TIP:  This script works great when sending an email through an SMS gateway.  (i.e. 2122222222@vtext.com for a Verizon Wireless phone.)  But you might want to add a value to the "alert_subject" setting and make it shorter than the default.  You might also want to be sure to set the 'include_day_summary' and include_map' settings to False.


FAQ
===

1.  Will this work internationally?

	I don't see why not.

2.  Receiving the message only 15 minutes before the event starts is kind of useless to me.  Can I change this?
	
	Currently, IFTT.com will only trigger the email 15 minutes before the event, and there is no way to alter this.  I would recommend complaining to them that you'd like to see at least SOME options (15 min, 30 min, 1 hr, etc.)  My original plan was to simply use a Google event's "email alert" feature, but there is seemingly no way to programmatically format the email to include a) just the data I want and b) in a format that's easily parseable.

3.  What does the email data look like?
	
	The subject of an email must have "[darkskymail]" in it or the script will skip right over it.

	The body of an event email is just the address you entered in the "location" field for the event, then a semicolon, then the start date and time of the event. Here's an example:

	1600 Amphitheatre Pkwy, Mountain View, CA 94043;October 13, 2012 at 01:21AM

4.  I have hundreds/thousands of emails in my inbox and this script iterates through each one every time.  This is useless to me.

	I created this script to be used with a single-purpose email address to which IFTT can send these messages.  I don't know how to optimize finding these emails in a huge inbox, and since GMail is free and easy I just went with that solution.  But feel free to fix this!
