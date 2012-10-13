import util
from util import log as log
import os, shutil
import datetime
import settings
import json

class Dark_Sky_Alert:
	def __init__(self):
		self.settings = settings.Dark_Sky_Mail_Settings()

	def get_data(self):
		"""
			This will fetch an email with that contains a [darksky] in the subject line and parse it.
			The location will be searched, and if a lat/lon is returned the forecast will be retrieved
			The result will be a dictionary:
				{"address": ADDRESS, "lat": LAT, "lon": LONG, "darksky": DARKSKY_FORECAST_OBJECT }
			If the list is None a venue was not found an not email will be sent.
		"""
		forecast_data = None
		geo_data = None
		email_data = None

		fetch = util.IMAP_Fetch()
		message_content = fetch.get_mail(self.settings.imap_server, self.settings.imap_user, self.settings.imap_password, self.settings.remove_messages_after_processed)

		if message_content:
			#turn the message content into actionable data
			message_data = message_content.split(';') #10/12/2003;257 Central Park West
			if len(message_data) == 2:
				start = message_data[0]
				address = message_data[1]
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

				email_data = {"address": address, "formatted_address": geo_data["results"][0]["formatted_address"], "lat": lat, "lon": lon, "darksky": forecast_data}
		else:
			log("No Google event email found.")

		return email_data

	def package_alert(self, email_data):
		""" This will create the alert text based on the captured venue and forecast data """
		alert = None
		subject = "Forecast at %s..." % email_data["address"] #add the venue name when we have it
		body = "It is currently %sF and " % email_data["darksky"]["currentTemp"]

		if not email_data["darksky"]["isPrecipitating"]:
			body = body + "not "

		body = body + "raining at your upcoming appointment's address '%s'. It will be %s, and %s in the the next hour." % (email_data["address"], email_data["darksky"]["hourSummary"], email_data["darksky"]["daySummary"])

		alert = {"subject": subject, "body": body}
		return alert

	def send_alert(self, alert):
		""" This will take the alert and mail it """

		send_alert_result = util.send_mail(self.settings.smtp_server, self.settings.smtp_user, self.settings.smtp_password, self.settings.smtp_port, [self.settings.alert_to], self.settings.alert_from, alert["subject"], alert["body"], [])
		return send_alert_result

	def execute(self):
		email_data = self.get_data()
		
		alert = None
		if(email_data):
			alert = self.package_alert(email_data)

		send_alert_result = None
		if(alert):
			send_alert_result = self.send_alert(alert)
		return send_alert_result

def main():
	log("\n" + str(datetime.datetime.now()) + "\nStarting alert!")
	alert = Dark_Sky_Alert()
	alert.execute()
	log("DarkSkyMail complete!\n")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass

