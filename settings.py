class Dark_Sky_Mail_Settings:
	def __init__(self):
		# ENTER YOUR SMTP SERVER INFORMATION HERE
		self.smtp_server = ""
		self.smtp_user = ""
		self.smtp_password = ""
		self.smtp_port = 587

		# ENTER YOUR IMAP SERVER INFORMATION HERE
		self.imap_server = ""
		self.imap_user = ""
		self.imap_password = ""

		# ENTER YOUR FROM AND TO ADDRESSES HERE
		self.alert_from = ""
		self.alert_to = ""
		self.alert_subject = None

		#SET THIS TO TRUE TO INCLUDE ADDITIONAL SUMMARY INFO FOR THE NEXT 24HRS
		self.include_day_summary = False

		#SET THIS TO TRUE TO INCLUDE A STATIC GOOGLE MAP IMAGE (OR LINK TO IT IN TEXT EMAIL)
		self.include_map = True

		#SET THIS TO FALSE TO ONLY SEND ALERTS IF IT'S RAINING OR WILL RAIN WITHIN THE HOUR
		self.send_even_when_clear = False

		# ENTER YOUR DARK SKY API KEY HERE
		self.dark_sky_API_key = ""

		# SET THIS TO TRUE TO DELETE THE IFTT MESSAGE FROM YOUR INBOX
		self.remove_messages_after_processed = True

		# THE IMAP INBOX WILL BE CHECKED AT THIS INTERVAL
		self.fetch_interval = 60 #in seconds

		# SET THIS TO TRUE TO SEE SOME DEBUG OUTPUT
		self.show_log = True #outputs some messages to stderr if True
