class Dark_Sky_Mail_Settings:
	def __init__(self):
		# ENTER YOUR SMTP SERVER INFORMATION HERE
		self.smtp_server = "smtp.gmail.com"
		self.smtp_user = ""
		self.smtp_password = ""
		self.smtp_port = 587

		# ENTER YOUR IMAP SERVER INFORMATION HERE
		self.imap_server = "imap.gmail.com"
		self.imap_user = ""
		self.imap_password = ""

		# ENTER YOUR FROM AND TO ADDRESSES HERE
		self.alert_from = ""
		self.alert_to = ""

		# ENTER YOUR DARK SKY API KEY HERE
		self.dark_sky_API_key = ""

		# SET THIS TO TRUE TO DELETE THE IFTT MESSAGE FROM YOUR INBOX
		self.remove_messages_after_processed = True

		# THE IMAP INBOX WILL BE CHECKED AT THIS INTERVAL
		self.fetch_interval = 60000 #in seconds

		# SET THIS TO TRUE TO SEE SOME DEBUG OUTPUT
		self.show_log = True #outputs some messages to stderr if True
