class Dark_Sky_Mail_Settings:
	def __init__(self):
		# ENTER YOUR SMTP SERVER INFORMATION HERE
		self.smtp_server = "smtp.gmail.com"
		self.smtp_user = ""
		self.smtp_password = ""
		self.smtp_port = 587

		# ENTER YOUR IMAP SERVER INFORMATION HERE
		self.imap_server = "imap.gmail.com"
		self.imap_port = 993
		self.imap_use_ssl = True
		self.imap_user = ""
		self.imap_password = ""
		# If self.imap_folder is set to None, DarkSkyMail will look in "Inbox"
		# Otherwise it will use this value.  If the mailbox name entered does
		# not exist, it will be created.  But this is kind of foolish because you'll probably
		# need a filter to move messages into the desired folder anyway.
		self.imap_folder = None

		# ENTER YOUR FROM AND TO ADDRESSES HERE
		self.alert_from = ""
		self.alert_to = ""
		self.alert_subject = None #If None defaults to "Current weather at your appointment on [START_DATE]"

		# SET THIS TO TRUE TO INCLUDE ADDITIONAL SUMMARY INFO FOR THE NEXT 24HRS
		self.include_day_summary = True

		# SET THIS TO TRUE TO INCLUDE A STATIC GOOGLE MAP IMAGE (OR LINK TO IT IN TEXT EMAIL)
		self.include_map = True

		# SET THIS TO FALSE TO ONLY SEND ALERTS IF IT'S RAINING OR WILL RAIN WITHIN THE HOUR
		self.send_even_when_clear = True

		# ENTER YOUR DARK SKY API KEY HERE
		self.dark_sky_API_key = ""

		# SET THIS TO TRUE TO DELETE THE REMINDER MESSAGE FROM YOUR INBOX
		# If you set this to False, you run the risk of getting stuck in a loop.
		# But, it's useful for debugging.
		self.remove_messages_after_processed = True

		# THE IMAP INBOX WILL BE CHECKED AT THIS INTERVAL
		self.fetch_interval = 60 #in seconds

		# ENTER THE FROM ADDRESS FOR IDENTIFYING GOOGLE CALENDAR EMAILS
		self.fetch_from_address = "calendar-notification@google.com"

		# SET THIS TO TRUE TO SEE SOME DEBUG OUTPUT
		self.show_log = True #outputs some messages to stderr if True
		self.send_no_location_error_email = False #sends an error email if no location found via Google
