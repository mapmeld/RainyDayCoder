import cgi, logging
from datetime import datetime, timedelta

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api.urlfetch import fetch,GET,POST
from google.appengine.api import mail
import botconfig, twitteroauth
import phoneconfig, twilio

class HomePage(webapp.RequestHandler):
  def get(self):
  	cityname = ""
	try:
		cityname = self.request.headers["X-AppEngine-City"].split(" ")
		index = 0
		for word in cityname:
			cityname[index] = word[0].upper() + word[ 1: len(word) ]
			index = index + 1
		cityname = ' '.join(cityname) + ", " + self.request.headers["X-AppEngine-Region"].upper()
	except:
		cityname = ""

	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>Rainy Day Coder</title>
		<link href="/bootstrap.min.css" rel="stylesheet" type="text/css"/>
		<style type="text/css">
.hero-unit{
	padding: 40px;
}
		</style>
	</head>
	<body>
		<div class="navbar">
			<div class="navbar-inner">
				<div class="container">
					<ul class="nav">
						<li>
							<a class="brand" href="/">
								Rainy Day Coder
							</a>
						</li>
						<li>
							<a class="active" href="/">
								Home
							</a>
						</li>
						<li>
							<a href="/why">
								Why code?
							</a>
						</li>
						<li>
							<a href="#">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
		<div class="container">
			<div class="hero-unit" style="text-align:center;">
				<img src="logo1.jpg" style="float:left;width:140px;"/>
				<h1>Learn code</h1>
				<p>on rainy nights and weekends</p>
				<form action="/subscribe" method="GET">
					<span style="font-weight:bold;vertical-align:center;font-size:12pt;">''' + cityname + '''</span> or <input id="zip" name="zip" type="text" class="span2" placeholder="ZIPCODE"/>
					<input type="submit" value="Stay out of the rain" class="btn btn-primary" style="vertical-align:top;"/>
				</form>
			</div>
			<div class="row">
				<div class="span4">
					<h3>Who teaches me to code?</h3>
					<p>Work on your own, or choose one of these sites:</p>
					<ul>
						<li>
							<strong><a href="http://codecademy.org" target="_blank">Codecademy</a></strong> introduces JavaScript in a series of lessons. Affiliated with Y-Combinator, the White House, and NYC Mayor Bloomberg.
						</li>
						<li style="color:#ccc;">
							<strong><a href="http://khanacademy.org" target="_blank">Khan Academy</a></strong> uses videos to teach you JavaScript. Taught by John Resig, inventor of jQuery. Backed by the Bill and Melinda Gates Foundation.
						</li>
						<li style="color:#ccc;">
							<strong><a href="http://udacity.com" target="_blank">Udacity</a></strong> has complete Computer Science courses which are online. And free. Founded by AI pioneer and Stanford professor Sebastian Thrun.
						</li>
					</ul>
				</div>
				<div class="span4">
					<h3>When do I code?</h3>
					<img src="http://farm2.staticflickr.com/1184/1084349065_3a55f1e974_m.jpg" alt="whenever there are umbrellas out" style="width:90%;"/>
					<ul>
						<li>
							Rainy nights and weekends (1 or 2 per week)
						</li>
						<li>
							When you're home sick
						</li>
						<li>
							Whenever you feel like it
						</li>
					</ul>
				</div>
				<div class="span4">
					<h3>How do you contact me?</h3>
					<ul>
						<li>
							Get e-mail
						</li>
						<li>
							We can send Tweets
						</li>
						<li>
							Text messages to most cell phones
						</li>
					</ul>
					<p>You can <a href="/citychange">change cities</a> or <a href="/unsubscribe">unsubscribe</a> at any time.</p>
					<iframe src="//www.facebook.com/plugins/like.php?href=http%3A%2F%2Frainydaycoder.appspot.com&amp;send=false&amp;layout=standard&amp;width=450&amp;show_faces=false&amp;action=like&amp;colorscheme=light&amp;font&amp;height=35&amp;appId=123994207657251" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:35px;" allowTransparency="true"></iframe>
				</div>
			</div>
			<div class="row">
				<div class="span12" style="text-align:center;">
					<img src="http://b.vimeocdn.com/ps/702/702568_300.jpg" width="200"/>
					<br/><br/>
					<small>Umbrella photo CC-BY-NC-SA <a href="http://flickr.com/photos/solidether">solidether</a></small>
				</div>
			</div>
		</div>
	</body>
</html>''')

class Unsubscribe(webapp.RequestHandler):
  def post(self):
	coders = None
  	if(self.request.get('contactname').find('@') == 0):
		coders = Coder.gql('WHERE contactmethod = :1', "tweet|" + self.request.get('contactname')[ 1 : len( self.request.get('contactname') ) ])
		for c in coders:
			contactname = c.contactmethod
			cityname = c.city
			c.delete()
			self.confirm_change(contactname, cityname)
		self.response.out.write('Your request has been made, and a confirmation message will be sent.')

	elif(self.request.get('contactname').find('@') > 0):
		coders = Coder.gql('WHERE contactmethod = :1', "mail|" + self.request.get('contactname') )
		for c in coders:
			contactname = c.contactmethod
			cityname = c.city
			c.delete()
			self.confirm_change(contactname, cityname)
		self.response.out.write('Your request has been made, and a confirmation message will be sent.')

	else:
		coders = Coder.gql('WHERE contactmethod = :1', "tweet|" + self.request.get('contactname') )
		if (coders.count() > 0):
			for c in coders:
				contactname = c.contactmethod
				cityname = c.city
				c.delete()
				self.confirm_change(contactname, cityname)
			self.response.out.write('Your request has been made, and a confirmation message will be sent.')

		coders = Coder.gql('WHERE contactmethod = :1', "mail|" + self.request.get('contactname') )
		if (coders.count() > 0):
			for c in coders:
				contactname = c.contactmethod
				cityname = c.city
				c.delete()
				self.confirm_change(contactname, cityname)
			self.response.out.write('Your request has been made, and a confirmation message will be sent.')

		coders = Coder.gql('WHERE contactmethod = :1', "txt|" + self.request.get('contactname') )
		if (coders.count() > 0):
			for c in coders:
				contactname = c.contactmethod
				cityname = c.city
				c.delete()
				self.confirm_change(contactname, cityname)
			self.response.out.write('Your request has been made, and a confirmation message will be sent.')

  def get(self):
	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>Rainy Day Coder: Unsubscribe</title>
		<link href="/bootstrap.min.css" rel="stylesheet" type="text/css"/>
	</head>
	<body>
		<div class="navbar">
			<div class="navbar-inner">
				<div class="container">
					<ul class="nav">
						<li>
							<a class="brand" href="/">
								Rainy Day Coder
							</a>
						</li>
						<li>
							<a href="/">
								Home
							</a>
						</li>
						<li>
							<a href="/why" class="active">
								Why code?
							</a>
						</li>
						<li>
							<a href="#">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
	<div class="container">
		<h1>Unsubscribing</h1>
		<hr/>
		<div class="well">
			<form action="/unsubscribe" method="POST">
				<label>E-mail, Twitter handle, or Phone Number we used to contact you:</label>
				<input id="contactname" name="contactname" type="text" class="span2" placeholder="Contact"/>
				<br/>
				<input type="submit" value="Unsubscribe" class="btn btn-primary" style="vertical-align:top;"/>
			</form>
		</div>
		<div class="well">
			We hope you code with us again sometime!
		</div>
	</div>
</body>
</html>''')

  def confirm_change(self, contactmethod, city):
	contactby = contactmethod.split('|')[0]
	contactname = contactmethod.split('|')[1]
	city = city.split(" ")
	index = 0
	for word in city:
		if(index == len(city) - 1):
			city[index] = word.upper()
		else:
			city[index] = word[0].upper() + word[ 1: len(word) ]
		index = index + 1
	city = ' '.join(city)

	if(contactby == 'tweet'):
		logging.info("Sending unsubscribe Tweet to " + contactname)
		finished_format = "@" + contactname.replace('@','').replace(' ','') + ": You are now unsubscribed from #RainyDayCoder."
		client = twitteroauth.TwitterClient(botconfig.consumer_key, botconfig.consumer_secret, botconfig.callback_url)
		additional_params = {
			"status": finished_format
		}
		result = client.make_request(
			"http://twitter.com/statuses/update.json",
		token=botconfig.access_token,
			secret=botconfig.access_token_secret,
			additional_params=additional_params,
			method=POST)

	elif(contactby == "mail"):
		logging.info("Sending unsubscribe e-mail to " + contactname)
		if mail.is_email_valid(contactname):
			sender_address = "korolev415@gmail.com"
			subject = "RainyDayCoder: Unsubscribed"
			mail.send_mail(sender_address, contactname, subject, "You are now unsubscribed from Rainy Day Coder.")

	elif(contactby == "txt"):
		outbody = "You are now unsubscribed from RainyDayCoder.appspot.com"
		account = twilio.Account(phoneconfig.account, phoneconfig.token)
		d = {
			'From' : phoneconfig.number,
			'To' : contactname,
			'Body' : outbody,
		}
		gotdata = account.request('/%s/Accounts/%s/SMS/Messages' % ('2008-08-01', phoneconfig.account), 'POST', d)
		logging.info("Sent unsubscribe text to " + contactname)

class CityChange(webapp.RequestHandler):
  def post(self):
	coders = None
  	if(self.request.get('contactname').find('@') == 0):
		coders = Coder.gql('WHERE contactmethod = :1', "tweet|" + self.request.get('contactname')[ 1 : len( self.request.get('contactname') ) ])
		for c in coders:
			state = ''
			c.city = self.request.get('zip')
			if(self.request.get('zip') == ''):
				c.city = self.request.headers["X-AppEngine-City"] + ", " + self.request.headers["X-AppEngine-Region"]
				state = self.request.headers["X-AppEngine-Region"]

			if(state in [ "CA", "OR", "WA" ] ):
				c.region = 'pacific'
			elif(state in [ "AZ", "CO", "ID", "MT", "NV", "NM", "ND", "SD", "TX", "UT", "WY" ] ):
				c.region = 'mountain'
			elif(state in [ "AL", "AR", "IL", "IN", "IA", "KS", "LA", "MI", "MN", "MS", "MO", "NE", "OH", "OK", "WI" ] ):
				c.region = 'central'
			elif(state in [ "CT", "DE", "DC", "FL", "GA", "KY", "ME", "MD", "MA", "NH", "NJ", "NY", "NC", "PA", "RI", "SC", "TN", "VT", "VA", "WV" ] ):
				c.region = 'eastern'
			elif(state in [ "AK" ] ):
				c.region = 'alaska'
			elif(state in [ "HI" ] ):
				c.region = 'hawaii'
			c.put()
			self.confirm_change(c, c.city)
		self.response.out.write('Your request has been made, and a confirmation message will be sent.')

	elif(self.request.get('contactname').find('@') > 0):
		
		coders = Coder.gql('WHERE contactmethod = :1', "mail|" + self.request.get('contactname') )
		for c in coders:
			state = ''
			c.city = self.request.get('zip')
			if(self.request.get('zip') == ''):
				c.city = self.request.headers["X-AppEngine-City"] + ", " + self.request.headers["X-AppEngine-Region"]
				state = self.request.headers["X-AppEngine-Region"]

			if(state in [ "CA", "OR", "WA" ] ):
				c.region = 'pacific'
			elif(state in [ "AZ", "CO", "ID", "MT", "NV", "NM", "ND", "SD", "TX", "UT", "WY" ] ):
				c.region = 'mountain'
			elif(state in [ "AL", "AR", "IL", "IN", "IA", "KS", "LA", "MI", "MN", "MS", "MO", "NE", "OH", "OK", "WI" ] ):
				c.region = 'central'
			elif(state in [ "CT", "DE", "DC", "FL", "GA", "KY", "ME", "MD", "MA", "NH", "NJ", "NY", "NC", "PA", "RI", "SC", "TN", "VT", "VA", "WV" ] ):
				c.region = 'eastern'
			elif(state in [ "AK" ] ):
				c.region = 'alaska'
			elif(state in [ "HI" ] ):
				c.region = 'hawaii'
			c.put()
			self.confirm_change(c, c.city)
		self.response.out.write('Your request has been made, and a confirmation message will be sent.')

	else:
		coders = Coder.gql('WHERE contactmethod = :1', "tweet|" + self.request.get('contactname') )
		if (coders.count() > 0):
			for c in coders:
				state = ''
				c.city = self.request.get('zip')
				if(self.request.get('zip') == ''):
					c.city = self.request.headers["X-AppEngine-City"] + ", " + self.request.headers["X-AppEngine-Region"]
					state = self.request.headers["X-AppEngine-Region"]

				if(state in [ "CA", "OR", "WA" ] ):
					c.region = 'pacific'
				elif(state in [ "AZ", "CO", "ID", "MT", "NV", "NM", "ND", "SD", "TX", "UT", "WY" ] ):
					c.region = 'mountain'
				elif(state in [ "AL", "AR", "IL", "IN", "IA", "KS", "LA", "MI", "MN", "MS", "MO", "NE", "OH", "OK", "WI" ] ):
					c.region = 'central'
				elif(state in [ "CT", "DE", "DC", "FL", "GA", "KY", "ME", "MD", "MA", "NH", "NJ", "NY", "NC", "PA", "RI", "SC", "TN", "VT", "VA", "WV" ] ):
					c.region = 'eastern'
				elif(state in [ "AK" ] ):
					c.region = 'alaska'
				elif(state in [ "HI" ] ):
					c.region = 'hawaii'
				c.put()
				self.confirm_change(c, c.city)
			self.response.out.write('Your request has been made, and a confirmation message will be sent.')

		coders = Coder.gql('WHERE contactmethod = :1', "mail|" + self.request.get('contactname') )
		if (coders.count() > 0):
			for c in coders:
				state = ''
				c.city = self.request.get('zip')
				if(self.request.get('zip') == ''):
					c.city = self.request.headers["X-AppEngine-City"] + ", " + self.request.headers["X-AppEngine-Region"]
					state = self.request.headers["X-AppEngine-Region"]

				if(state in [ "CA", "OR", "WA" ] ):
					c.region = 'pacific'
				elif(state in [ "AZ", "CO", "ID", "MT", "NV", "NM", "ND", "SD", "TX", "UT", "WY" ] ):
					c.region = 'mountain'
				elif(state in [ "AL", "AR", "IL", "IN", "IA", "KS", "LA", "MI", "MN", "MS", "MO", "NE", "OH", "OK", "WI" ] ):
					c.region = 'central'
				elif(state in [ "CT", "DE", "DC", "FL", "GA", "KY", "ME", "MD", "MA", "NH", "NJ", "NY", "NC", "PA", "RI", "SC", "TN", "VT", "VA", "WV" ] ):
					c.region = 'eastern'
				elif(state in [ "AK" ] ):
					c.region = 'alaska'
				elif(state in [ "HI" ] ):
					c.region = 'hawaii'
				c.put()
				self.confirm_change(c, c.city)
			self.response.out.write('Your request has been made, and a confirmation message will be sent.')

		coders = Coder.gql('WHERE contactmethod = :1', "txt|" + self.request.get('contactname') )
		if (coders.count() > 0):
			for c in coders:
				state = ''
				c.city = self.request.get('zip')
				if(self.request.get('zip') == ''):
					c.city = self.request.headers["X-AppEngine-City"] + ", " + self.request.headers["X-AppEngine-Region"]
					state = self.request.headers["X-AppEngine-Region"]

				if(state in [ "CA", "OR", "WA" ] ):
					c.region = 'pacific'
				elif(state in [ "AZ", "CO", "ID", "MT", "NV", "NM", "ND", "SD", "TX", "UT", "WY" ] ):
					c.region = 'mountain'
				elif(state in [ "AL", "AR", "IL", "IN", "IA", "KS", "LA", "MI", "MN", "MS", "MO", "NE", "OH", "OK", "WI" ] ):
					c.region = 'central'
				elif(state in [ "CT", "DE", "DC", "FL", "GA", "KY", "ME", "MD", "MA", "NH", "NJ", "NY", "NC", "PA", "RI", "SC", "TN", "VT", "VA", "WV" ] ):
					c.region = 'eastern'
				elif(state in [ "AK" ] ):
					c.region = 'alaska'
				elif(state in [ "HI" ] ):
					c.region = 'hawaii'
				c.put()
				self.confirm_change(c, c.city)
			self.response.out.write('Your request has been made, and a confirmation message will be sent.')

  def get(self):
  	cityname = ""
	try:
		cityname = self.request.headers["X-AppEngine-City"].split(" ")
		index = 0
		for word in cityname:
			cityname[index] = word[0].upper() + word[ 1: len(word) ]
			index = index + 1
		cityname = ' '.join(cityname) + ", " + self.request.headers["X-AppEngine-Region"].upper()
	except:
		cityname = ""
	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>Rainy Day Coder: Change Cities</title>
		<link href="/bootstrap.min.css" rel="stylesheet" type="text/css"/>
	</head>
	<body>
		<div class="navbar">
			<div class="navbar-inner">
				<div class="container">
					<ul class="nav">
						<li>
							<a class="brand" href="/">
								Rainy Day Coder
							</a>
						</li>
						<li>
							<a href="/">
								Home
							</a>
						</li>
						<li>
							<a href="/why" class="active">
								Why code?
							</a>
						</li>
						<li>
							<a href="#">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
	<div class="container">
		<h1>Changing Cities</h1>
		<hr/>
		<div class="well">
			<form action="/citychange" method="POST">
				<label>E-mail, Twitter handle, or Phone Number we used to contact you:</label>
				<input id="contactname" name="contactname" type="text" class="span2" placeholder="Contact"/>
				<br/>
				<label>New city or zipcode:</label>
				<span style="font-weight:bold;vertical-align:center;font-size:12pt;">''' + cityname + '''</span> or <input id="zip" name="zip" type="text" class="span2" placeholder="ZIPCODE"/>
				<br/>
				<input type="submit" value="Change City" class="btn btn-primary" style="vertical-align:top;"/>
			</form>
		</div>
	</div>
</body>
</html>''')

  def confirm_change(self, c, city):
	contactby = c.contactmethod.split('|')[0]
	contactname = c.contactmethod.split('|')[1]
	city = city.split(" ")
	index = 0
	for word in city:
		if(index == len(city) - 1):
			city[index] = word.upper()
		else:
			city[index] = word[0].upper() + word[ 1: len(word) ]
		index = index + 1
	city = ' '.join(city)

	if(contactby == 'tweet'):
		logging.info("Sending city change Tweet to " + contactname)
		finished_format = "@" + contactname.replace('@','').replace(' ','') + ": Your #RainyDayCoder city has been changed."
		client = twitteroauth.TwitterClient(botconfig.consumer_key, botconfig.consumer_secret, botconfig.callback_url)
		additional_params = {
			"status": finished_format
		}
		result = client.make_request(
			"http://twitter.com/statuses/update.json",
		token=botconfig.access_token,
			secret=botconfig.access_token_secret,
			additional_params=additional_params,
			method=POST)

	elif(contactby == "mail"):
		logging.info("Sending city change e-mail to " + contactname)
		if mail.is_email_valid(contactname):
			sender_address = "korolev415@gmail.com"
			subject = "RainyDayCoder: City Changed"
			mail.send_mail(sender_address, contactname, subject, "You are now signed up for Rainy Day Coder in " + city + "!")

	elif(contactby == "txt"):
		outbody = "You changed your coding city to " + city + ". RainyDayCoder.appspot.com"
		account = twilio.Account(phoneconfig.account, phoneconfig.token)
		d = {
			'From' : phoneconfig.number,
			'To' : contactname,
			'Body' : outbody,
		}
		gotdata = account.request('/%s/Accounts/%s/SMS/Messages' % ('2008-08-01', phoneconfig.account), 'POST', d)
		logging.info("Sent city change text to " + contactname)

class Subscribe(webapp.RequestHandler):
  def post(self):
	c = Coder()
	c.name = self.request.get('name')
	c.city = self.request.get('zip')
	c.codecademyname = self.request.get('codecademyname')
	if(self.request.get('zip') == ''):
		c.city = self.request.headers["X-AppEngine-City"] + ", " + self.request.headers["X-AppEngine-Region"]
		state = self.request.headers["X-AppEngine-Region"]
	else:
		cityjson = fetch("http://zip.elevenbasetwo.com/?zip=" + self.request.get('zip'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
		state = cityjson[ cityjson.find("state")  + 9 : cityjson.find("state") + 11 ]

	if(state in [ "CA", "OR", "WA" ] ):
		c.region = 'pacific'
	elif(state in [ "AZ", "CO", "ID", "MT", "NV", "NM", "ND", "SD", "TX", "UT", "WY" ] ):
			c.region = 'mountain'
	elif(state in [ "AL", "AR", "IL", "IN", "IA", "KS", "LA", "MI", "MN", "MS", "MO", "NE", "OH", "OK", "WI" ] ):
		c.region = 'central'
	elif(state in [ "CT", "DE", "DC", "FL", "GA", "KY", "ME", "MD", "MA", "NH", "NJ", "NY", "NC", "PA", "RI", "SC", "TN", "VT", "VA", "WV" ] ):
		c.region = 'eastern'
	elif(state in [ "AK" ] ):
		c.region = 'alaska'
	elif(state in [ "HI" ] ):
		c.region = 'hawaii'
	c.contactmethod = self.request.get('contact') + "|" + self.request.get('contactname')
	c.weekendonly = self.request.get('wkendonly')
	c.contactlast = datetime.now() - timedelta(days=31)
	c.contactsecond = datetime.now() - timedelta(days=31)
	c.put()
	
	self.response.out.write('''<!DOCTYPE html>
<html>
<body>
Sign-up confirmed.
<br/><br/>
You will receive a confirmation message.
</body>
</html>''')

	contactby = c.contactmethod.split('|')[0]
	contactname = c.contactmethod.split('|')[1]

	if(contactby == 'tweet'):
		logging.info("Sending confirmation Tweet to " + contactname)
		finished_format = "@" + contactname.replace('@','').replace(' ','') + ": Thanks for signing up with #RainyDayCoder!"
		client = twitteroauth.TwitterClient(botconfig.consumer_key, botconfig.consumer_secret, botconfig.callback_url)
		additional_params = {
			"status": finished_format
		}
		result = client.make_request(
			"http://twitter.com/statuses/update.json",
		token=botconfig.access_token,
			secret=botconfig.access_token_secret,
			additional_params=additional_params,
			method=POST)

	elif(contactby == "mail"):
		logging.info("Sending confirmation e-mail to " + contactname)
		if mail.is_email_valid(contactname):
			sender_address = "korolev415@gmail.com"
			subject = "Rainy Day Coder Confirmation"
			mail.send_mail(sender_address, contactname, subject, "You are now signed up for Rainy Day Coder!")

	elif(contactby == "txt"):
		outbody = "You're now signed up to learn JavaScript on rainy days. RainyDayCoder.appspot.com"
		account = twilio.Account(phoneconfig.account, phoneconfig.token)
		d = {
			'From' : phoneconfig.number,
			'To' : contactname,
			'Body' : outbody,
		}
		gotdata = account.request('/%s/Accounts/%s/SMS/Messages' % ('2008-08-01', phoneconfig.account), 'POST', d)
		logging.info("Sent confirmation text to " + contactname)

  def get(self):
  	cityname = ""
	if(self.request.get('zip') == ''):
		try:
			cityname = self.request.headers["X-AppEngine-City"].split(" ")
			index = 0
			for word in cityname:
				cityname[index] = word[0].upper() + word[ 1: len(word) ]
				index = index + 1
			cityname = ' '.join(cityname) + ", " + self.request.headers["X-AppEngine-Region"].upper()
		except:
			cityname = ""
	else:
		cityjson = fetch("http://zip.elevenbasetwo.com/?zip=" + self.request.get('zip'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
		cityname = cityjson[ cityjson.find('city') + 8: len(cityjson) - 2 ]
		cityname = cityname.split(' ')
		index = 0
		for word in cityname:
			cityname[index] = word[0] + word[ 1 : len(word) ].lower()
			index = index + 1
		cityname = ' '.join(cityname) + ", " + cityjson[ cityjson.find("state")  + 9 : cityjson.find("state") + 11 ]

	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>Rainy Day Coder</title>
		<link href="/bootstrap.min.css" rel="stylesheet" type="text/css"/>
		<style type="text/css">
.hero-unit{
	padding: 40px;
}
		</style>
	</head>
	<body>
		<div class="navbar">
			<div class="navbar-inner">
				<div class="container">
					<ul class="nav">
						<li>
							<a class="brand" href="/">
								Rainy Day Coder
							</a>
						</li>
						<li>
							<a href="/">
								Home
							</a>
						</li>
						<li>
							<a href="/why">
								Why code?
							</a>
						</li>
						<li>
							<a href="#">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
		<div class="container">
			<div class="row">
				<div class="hero-unit" style="text-align:center;">
					<img src="logo1.jpg" style="float:left;width:115px;"/>
					<h1>Coding in ''' + cityname + '''</h1>
					<p>on rainy nights and weekends</p>
				</div>
			</div>
			<div class="row">
				<form action="/subscriber" method="POST">
					<input type="hidden" name="zip" value="''' + cgi.escape(self.request.get('zip')) + '''"/>
					<div class="well">
						<h3>How do we contact you?</h3>
						We'll contact you at most twice in a week.<br/>
						<label class="radio"><input type="radio" name="contact" value="mail" checked="checked"/>E-mail</label>
						<label class="radio"><input type="radio" name="contact" value="tweet"/>Twitter</label>
						<label class="radio"><input type="radio" name="contact" value="txt"/>Text</label>
						<h3>Enter e-mail, Twitter handle, or number here:</h3>
						<input name="contactname" class="x-large"/>
					</div>
					<div class="well">
						<h3>Weekends only?</h3>
						<label class="checkbox"><input type="checkbox" name="wkendonly"/>Weekends only</label>
					</div>
					<div class="well">
						<h3>Track your progress?</h3>
						If you'd like us to track your progress on <a href="http://codecademy.com" target="_blank">Codecademy</a>, create an account there and paste your profile link here.
						<br/>
						On your <a href="http://www.codecademy.com/edit_account/basic_info" target="_blank">Account page</a>, you must set <i>Who can view my profile</i> to Everyone.
						<br/>
						<input name="codecademyname" class="x-large" placeholder="http://www.codecademy.com/profiles/yourname" style="width:300pt;"/>
					</div>
					<input type="submit" class="btn btn-info" value="Sign Up for Rainy Day Coder"/>
				</form>
			</div>
			<div class="row">
				<div class="span12" style="text-align:center;">
					<img src="http://b.vimeocdn.com/ps/702/702568_300.jpg" width="200"/>
				</div>
			</div>
		</div>
	</body>
</html>''')

class Region(webapp.RequestHandler):

  def get(self):
	days = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
	coders = Coder.gql('WHERE region = :1 ORDER BY city', self.request.get('region'))
	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>Rainy Day Coder</title>
		<link href="/bootstrap.min.css" rel="stylesheet" type="text/css"/>
	</head>
	<body>
		<div class="navbar">
			<div class="navbar-inner">
				<div class="container">
					<ul class="nav">
						<li>
							<a class="brand" href="/">
								Rainy Day Coder
							</a>
						</li>
						<li>
							<a class="active" href="/">
								Home
							</a>
						</li>
						<li>
							<a href="#">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="span10">\n''')
	lastcity = " | "
	for coder in coders:
		wjson = ""
		if(lastcity.split("|")[0] == coder.city):
			if(lastcity.split("|")[1] == "NO"):
				# already tried this city, and it wasn't raining
				continue
			else:
				# already tried this city, and it was raining
				wjson = lastcity[ lastcity.find('|') + 1 : len(lastcity) ]
		else:
			# new zipcode, check for rain
			wjson = fetch("http://api.wunderground.com/api/d5f91ff9e5d13cd9/forecast/q/" + coder.city + ".json", payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
			
		dayAdjust = datetime.now().weekday()

		# AppEngine has UTC time; let cron add or subtract a day to read the right forecast
		if(self.request.get('dayAdjust') == "minus1"):
			dayAdjust = (dayAdjust + 6) % 7
		elif(self.request.get('dayAdjust') == "plus1"):
			dayAdjust = (dayAdjust + 8) % 7

		if(days[dayAdjust] == "Saturday" or days[dayAdjust] == "Sunday"):
			# check daytime first
			wjson = wjson.split("icon_url")
			for day in wjson:
				if(day.find(days[dayAdjust]) > -1):
					icon = day[ 3 : day.find('title') ]
					icon = icon[ 0 : icon.find('"') ]
					if(icon.find('rain') > -1 or icon.find('storm') > -1):
						# TODO: need to check that rainfall isn't so small!
						lastcity = coder.city + "|" + 'icon_url'.join(wjson)
						if(day.find(days[dayAdjust] + " Night") > -1):
							self.response.out.write('Rain tonight in ' + coder.city + '!')
							self.tweetTo(coder, "tonight")
						else:
							self.response.out.write('Rain today in ' + coder.city + '!')						
							self.tweetTo(coder, "today")
					else:
						lastcity = coder.city + "|NO"					
					self.response.out.write( '<img src="' + icon + '"/><br/>' )

		elif(coder.weekendonly != "on"): # will code any night
			today = days[dayAdjust] + " Night"
			wjson = wjson.split("icon_url")
			for day in wjson:
				if(day.find(today) > -1):
					icon = day[ 3 : day.find('title') ]
					icon = icon[ 0 : icon.find('"') ]
					if(icon.find('rain') > -1 or icon.find('storm') > -1):
						lastcity = coder.city + "|" + 'icon_url'.join(wjson)
						self.response.out.write('Rain tonight in ' + coder.city + '!')
						self.tweetTo(coder, "tonight")
					else:
						lastcity = coder.city + "|NO"
						
					self.response.out.write( '<img src="' + icon + '"/><br/>' )
					break
		
	self.response.out.write('			</div>\n		</div>\n	</body>\n</html>')

  def badgeStatus(self, coder):
	# badges sourced from CSS on http://cdn.codecademy.com/assets/application-ltr-75dbc02d22023f50a85125d4f34c3102.css
	badgeOrder = [ "first-lesson", "exercises-10", "exercises-25", "exercises-50", "exercises-100", "exercises-200", "exercises-500", "exercises-1000", "exercises-10000", "course-programming-intro", "course-fizzbuzz", "course-functions_in_javascript", "course-hello_new_york", "course-functions-in-javascript-2-0", "course-conditionals-in-javascript", "course-calculating-the-costs-of-running-a-business", "course-conditionals-application", "course-primitives-development-course", "course-blackjack-part-1", "course-spencer-sandbox", "course-building-an-address-book", "course-olympic-trials", "course-objects-ii", "default-cash-register", "default-loops", "course-dice-game-part-2-getting-dicey", "course-blackjack-part-2", "course-fizzbuzz-return-of-the-modulus", "course-intro-to-object-oriented-programming", "course-cash-register-mark-ii", "default-more-arrays", "default-rock-paper-scissors", "default-recursion", "default-recursive-functions", "course-blackjack-part-3", "course-html-one-o-one", "course-week-3-html-project"  ]
	
	# "course-javascript-intro" not yet placed

	if(coder.codecademyname is not None):
		if(coder.codecademyname.find('codecademy.com/profiles/') == -1):
			# not a valid Codecademy profile URL
			return "not-valid"
	else:
		return "not-valid"

	badgescrape = fetch("http://www.codecademy.com/profiles/" + coder.codecademyname.split('codecademy.com/profiles/')[1], payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content.split("span class='badge ")
	if(len(badgescrape) == 1):
		# first lesson
		return "first-lesson"
	index = -1
	hasbadges = [ ]
	for badge in badgescrape:
		index = index + 1
		if(index == 0):
			# first segment has nothing
			continue
		badgename = badge[ 0: badge.find("'>") ]
		hasbadges.append(badgename)

	for badgename in badgeOrder:
		if(badgename not in hasbadges):
			if(badgename.find('exercises-') > -1 and (badgename.find('-50') > -1 or badgename.find('-100') > -1 or badgename.find('-200') > -1 or badgename.find('-500') > -1 or badgename.find('-1000') > -1or badgename.find('-10000') > -1 )):
				# lots of exercises not needed to continue
				continue
			return badgename

  def tweetTo(self, coder, timeframe):
	if(datetime.now() - coder.contactsecond < timedelta(days=7) ):
		# no spam rule: this coder was contacted twice in the past 7 days
		return
	else:
		# OK to contact! update coder days
		coder.contactsecond = coder.contactlast
		coder.contactlast = datetime.now()
		coder.put()
	contactby = coder.contactmethod.split('|')[0]
	contactname = coder.contactmethod.split('|')[1]
	
	nextBadge = self.badgeStatus( coder )
	if(nextBadge != "not-valid"):
		if(nextBadge.find('course-') > -1):
			nextBadge = "http://www.codecademy.com/courses/" + nextBadge[ 7 : len(nextBadge) ]
		else:
			nextBadge = "http://www.codecademy.com/courses/programming-intro"

	if(contactby == 'tweet'):
		logging.info("Sending Tweet to " + contactname + " in " + coder.city)
		finished_format = "@" + contactname.replace('@','').replace(' ','') + ": #RainyDayCoder says it's going to rain " + timeframe + ". Time to code?"
		if(nextBadge != "not-valid"):
			finished_format = finishedFormat + " " + nextBadge		
		client = twitteroauth.TwitterClient(botconfig.consumer_key, botconfig.consumer_secret, botconfig.callback_url)
		additional_params = {
			"status": finished_format
		}
		result = client.make_request(
			"http://twitter.com/statuses/update.json",
		token=botconfig.access_token,
			secret=botconfig.access_token_secret,
			additional_params=additional_params,
			method=POST)
		#logging.info(result.content)

	elif(contactby == "mail"):
		logging.info("Sending e-mail to " + contactname + " in " + coder.city)
		if mail.is_email_valid(contactname):
			sender_address = "korolev415@gmail.com"
			subject = "Code on this Rainy Day"
			if(timeframe == "tonight"):
				subject = "Code on this Rainy Night"
			placename = coder.city
			try:
				# attempt zipcode decode
				cityjson = fetch("http://zip.elevenbasetwo.com/?zip=" + str( int( placename) ), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
				cityname = cityjson[ cityjson.find('city') + 8: len(cityjson) - 2 ]
				cityname = cityname.split(' ')
				index = 0
				for word in cityname:
					cityname[index] = word[0] + word[ 1 : len(word) ].lower()
					index = index + 1
				placename = ' '.join(cityname) + ", " + cityjson[ cityjson.find("state")  + 9 : cityjson.find("state") + 11 ]
			except:
				# just keep coder.city
				fullnamealready = 1
			body = ""
			if(nextBadge == "not-valid"):
				body = '''
It's raining in ''' + cgi.escape(placename) + ' ' + timeframe + '''! Time to go to Codecademy and start coding!

-- Nick
Rainy Day Coder ( http://rainydaycoder.appspot.com )'''
			else:
				body = '''
It's raining in ''' + cgi.escape(placename) + ' ' + timeframe + '''! Time to go to Codecademy and start coding!

Pick up where you left off, at ''' + nextBadge + '''

-- Nick
Rainy Day Coder ( http://rainydaycoder.appspot.com )'''
			mail.send_mail(sender_address, contactname, subject, body)
	elif(contactby == "txt"):
		outbody = "It's raining " + timeframe + "! Time to go to Codecademy and learn to code! -RainyDayCoder.appspot.com"
		account = twilio.Account(phoneconfig.account, phoneconfig.token)
		d = {
			'From' : phoneconfig.number,
			'To' : contactname,
			'Body' : outbody,
		}
		gotdata = account.request('/%s/Accounts/%s/SMS/Messages' % ('2008-08-01', phoneconfig.account), 'POST', d)
		logging.info("Sent text to " + contactname + " in " + coder.city)

class Map(webapp.RequestHandler):
  def get(self):
  	ll = self.request.get('ll').split(',')
	mapimg = fetch("http://pafciu17.dev.openstreetmap.org/?module=map&center=" + ll[1] + "," + ll[0] + "&zoom=16&type=mapnik&width=500&height=250", payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
  	self.response.out.write(mapimg)

class Why(webapp.RequestHandler):
  def get(self):
  	cityname = ""
	try:
		cityname = self.request.headers["X-AppEngine-City"].split(" ")
		index = 0
		for word in cityname:
			cityname[index] = word[0].upper() + word[ 1: len(word) ]
			index = index + 1
		cityname = ' '.join(cityname) + ", " + self.request.headers["X-AppEngine-Region"].upper()
	except:
		cityname = ""
	self.response.out.write('''<!DOCTYPE html>
<html>
<head>
	<title>Rainy Day Coder: Why Learn to Code?</title>
	<link href="/bootstrap.min.css" rel="stylesheet" type="text/css"/>
</head>
<body>
		<div class="navbar">
			<div class="navbar-inner">
				<div class="container">
					<ul class="nav">
						<li>
							<a class="brand" href="/">
								Rainy Day Coder
							</a>
						</li>
						<li>
							<a href="/">
								Home
							</a>
						</li>
						<li>
							<a href="/why" class="active">
								Why code?
							</a>
						</li>
						<li>
							<a href="#">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
	<div class="container">
		<h1>Why learn to code?</h1>
		<hr/>
		<div class="well">
			<p>You, yes <strong>you</strong>, can make websites, games, and time-saving scripts.</p>
			<p>Tell the world about stuff you care about.</p>
			<p>Help a movement reach more people through interactive videos and maps.</p>
			<p>Understand how technology works.</p>
		</div>
		<div class="well">
			<h3>You are going to make awesome things</h3>
			<h3>It's free</h3>
		</div>
		<div class="well" style="text-align:center;">
			<img src="logo1.jpg" style="float:left;width:115px;"/>
			<h2>Learn code</h2>
			<p>on rainy nights and weekends</p>
			<form action="/subscribe" method="GET">
				<span style="font-weight:bold;vertical-align:center;font-size:12pt;">''' + cityname + '''</span> or <input id="zip" name="zip" type="text" class="span2" placeholder="ZIPCODE"/>
				<br/>
				<input type="submit" value="Stay out of the rain" class="btn btn-primary" style="vertical-align:top;"/>
			</form>
		</div>
	</div>
</body>
</html>''')

class Coder(db.Model):
	name = db.StringProperty()
	city = db.StringProperty()
	region = db.StringProperty()
	contactmethod = db.StringProperty()
	weekendonly = db.StringProperty()
	contactlast = db.DateTimeProperty()
	contactsecond = db.DateTimeProperty()
	codecademyname = db.StringProperty()

application = webapp.WSGIApplication(
                                     [('/region.*', Region),
                                     ('/why.*', Why),
                                     ('/subscribe.*', Subscribe),
                                     ('/map.*', Map),
                                     ('/citychange.*', CityChange),
                                     ('/unsubscribe.*', Unsubscribe),
                                     ('/.*', HomePage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()