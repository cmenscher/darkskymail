What does this do?
===========

This script checks an email inbox via IMAP for a message that contains location and start time data for a Google Calendar event, triggered 15 minutes before it is scheduled to start. The script gathers the event's location info and emails a precipitation forecast for it using the awesome Dark Sky API (https://developer.darkskyapp.com).  BUY THE APP! http://darkskyapp.com/


Requirements
============

* A Dark Sky API key (https://developer.darkskyapp.com/)
* An IMAP email inbox
* A box to run darkskymail.py as a service


Directions
==========

1.  Clone the project into a directory on your box.
2.  Edit the settings.py file. Use the comments to guide you.
3.  Run darkskymail.py

After it's running, you'll need to create email reminders for your events sent to the email address in settings.py ("alert_to") for no earlier than one hour prior to the event.  (DarkSky will only give you a forecast for the next hour.)

![Sample Email](https://dl.dropbox.com/s/jsoj0a4klcz9hcs/screenshot_mailapp.png?dl=1)

***IMPORTANT***
Once DarkSkyMail is running, be sure to include a valid address in the "location" field of the calendar event!  I am using the Google geocoding API, so it's quite forgiving if you don't use an exact/full address with postal codes, etc.  You can even use place names in some cases. ("Union Square New York" works, "721 Broadway New York" works, etc.)  But I recommend using an exact address whenever possible.

TIP:  This script works great when sending an email through an SMS gateway.  (i.e. 2122222222@vtext.com for a Verizon Wireless phone.)  But you might want to add a value to the "alert_subject" setting and make it shorter than the default.  You might also want to be sure to set the 'include_day_summary' and include_map' settings to False.


![Sample SMS](https://dl.dropbox.com/s/7ky4ej5d90r17pd/screenshot_sms.png?dl=1)
