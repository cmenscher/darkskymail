import util
from util import log as log
import os, shutil
import datetime
import settings
import json
from time import sleep
from imap_fetch import IMAP_Fetch

class Dark_Sky_Alert:
	def __init__(self):
		self.settings = settings.Dark_Sky_Mail_Settings()

	def get_data(self):
		"""
			This will fetch an email with that contains a [darkskymail] in the subject line and parse it.
			The location will be searched, and if a lat/lon is returned the forecast will be retrieved
			The result will be a dictionary:
				{"address": ADDRESS, "lat": LAT, "lon": LONG, "darksky": DARKSKY_FORECAST_OBJECT }
			If the list is None a venue was not found an not email will be sent.
		"""
		forecast_data = None
		geo_data = None
		email_data = None

		kwargs = {
			"imap_server": self.settings.imap_server,
			"imap_port": self.settings.imap_port,
			"imap_user": self.settings.imap_user,
			"imap_password": self.settings.imap_password,
			"use_ssl": self.settings.imap_use_ssl,
			"delete_messages": self.settings.remove_messages_after_processed,
			"imap_folder": self.settings.imap_folder
		}
		fetch = IMAP_Fetch(**kwargs)
		#message_content = fetch.get_mail(self.settings.imap_server, self.settings.imap_port, self.settings.imap_user, self.settings.imap_password, **kwargs)
		message_content = fetch.get_mail()

		if message_content:
			#turn the message content into actionable data
			message_data = message_content.split(';') #10/12/2003;257 Central Park West
			if len(message_data) == 2:
				start = message_data[1]
				address = message_data[0]
			else:
				log("No message found with event content.")
			
			#TODO: handle non-address or bad-address values
			geo_data_val = None
			geo_data_val = util.search_for_venue(address)
			if geo_data_val:
				geo_data = json.loads(geo_data_val)

			if geo_data:
				if len(geo_data["results"]) > 0:
					loc =  geo_data["results"][0]["geometry"]["location"]
					lat = loc["lat"]
					lon = loc["lng"]
				else:
					log("No location found for '%s'." % address)

				forecast_data_val = util.get_forecast(self.settings.dark_sky_API_key, lat, lon)
				forecast_data = json.loads(forecast_data_val)

				email_data = {"address": address, "formatted_address": geo_data["results"][0]["formatted_address"], "start": start, "lat": lat, "lon": lon, "darksky": forecast_data}
		else:
			log("No Google event email found.")

		return email_data

	def package_alert(self, email_data):
		""" This will create the alert text based on the captured venue and forecast data """
		alert = None
		subject = "Current weather at your appointment on %s" % email_data["start"]

		#This will override the default subject with the custom subject in settings.py
		#This is particularly useful if you send the text as an SMS (to shorten it)
		if self.settings.alert_subject:
			subject = self.settings.alert_subject

		static_map_url = "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=16&size=300x200&maptype=roadmap&markers=color:blue|label:Event|%s,%s&sensor=false" % (email_data["address"], email_data["lat"], email_data["lon"])

		body_text = "It is currently %sF and " % email_data["darksky"]["currentTemp"]

		if not email_data["darksky"]["isPrecipitating"]:
			body_text = body_text + "not"

		body_text = "%s raining at your next appointment ('%s'). It will be %s in the next hour" % (body_text, email_data["address"], email_data["darksky"]["hourSummary"])

		if self.settings.include_day_summary:
			body_text = "%s, with %s through tomorrow." % (body_text, email_data["darksky"]["daySummary"])
		else:
			body_text = "%s." % body_text

		#now add the static map URL to the body
		if self.settings.include_map:
			html = "<html><head></head><body>%s<p><img src='%s' /></p><p><a href='http://darkskyapp.com'>Powered by Dark Sky</a></p></body></html>" % (body_text, static_map_url)
			body_text = "%s\n\n%s" % (body_text, static_map_url)
		else:
			html = "<html><head></head><body>%s<p><a href='http://darkskyapp.com'>Powered by Dark Sky</a></p></body></html>" % (body_text)

		alert = {"subject": subject, "body_text": body_text, "body_html": html}
		return alert

	def send_alert(self, alert):
		""" This will take the alert and mail it """

		send_alert_result = util.send_mail(self.settings.smtp_server, self.settings.smtp_user, self.settings.smtp_password, self.settings.smtp_port, [self.settings.alert_to], self.settings.alert_from, alert["subject"], alert["body_text"], alert["body_html"], [])
		return send_alert_result

	def execute(self):
		alert = None
		send_alert_result = None

		email_data = self.get_data()

		if(email_data):
			#only proceed if it's going to rain or the settings say to always send
			if self.settings.send_even_when_clear or email_data["darksky"]["minutesUntilChange"] > 0:
				alert = self.package_alert(email_data)

				if(alert):
					send_alert_result = self.send_alert(alert)
			else:
				log("NO ALERT EMAIL: It's not raining, nor will it in the next hour. (Change 'send_even_when_clear' setting to send anyway.)")
		
		return send_alert_result

def main():
	log("Dark Sky Mail initiated!")
	log("\n" + str(datetime.datetime.now()) + "\nGetting messages...")
	app = Dark_Sky_Alert()
	
	app.execute() #run once

	if app.settings.fetch_interval > 0:
		while 1:
			log("Sleeping for %s seconds...\n" % app.settings.fetch_interval)
			sleep(app.settings.fetch_interval)
			log("\n" + str(datetime.datetime.now()) + "\nGetting messages...")
			app.execute()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass

