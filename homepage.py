import cgi
from datetime import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api.urlfetch import fetch,GET,POST

class HomePage(webapp.RequestHandler):
  def get(self):
	if(self.request.get('gen') == 'coder'):
		c = Coder()
		c.name = "Sam Pull"
		c.city = "94103"
		c.region = "pacific"
		c.contactmethod = "@mapmeld"
		c.weekendonly = "everyday"
		c.put()
	elif(self.request.get('gen') == 'zip'):
		c = Coder()
		c.name = "Billy " + self.request.get('zip')
		c.city = self.request.get('zip')
		c.region = "pacific"
		c.contactmethod = "@mapmeld"
		c.weekendonly = "everyday"
		c.put()

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
				<img src="http://i.imgur.com/ToJkV.png" style="float:left"/>
				<h1>Learn code</h1>
				<p>on rainy nights and weekends</p>
				<p>
					<input type="text" class="span3" placeholder="ZIPCODE"/>
					<a class="btn btn-primary" style="vertical-align:top;">
						Stay out of the rain
					</a>
				</p>
			</div>
			<div class="row">
				<div class="span4">
					<h3>Who teaches me to code?</h3>
					<p>Work on your own, or choose one of these sites:</p>
					<ul>
						<li>
							<strong><a href="http://codecademy.org" target="_blank">Codecademy</a></strong> is a free site to learn JavaScript. Backed by the White House and NYC Mayor Bloomberg.
						</li>
						<li>
							<strong><a href="http://khanacademy.org" target="_blank">Khan Academy</a></strong> uses videos to teach you about JavaScript. Taught by Jon Resig, inventor of the jQuery library. Backed by the Bill and Melinda Gates Foundation.
						</li>
						<li>
							<strong><a href="http://udacity.com" target="_blank">Udacity</a></strong> has complete Computer Science courses which are online. And free. Founded by AI pioneer and Stanford professor Sebastian Thrun.
						</li>
					</ul>
				</div>
				<div class="span4">
					<h3>When do I code?</h3>
					<img src="http://farm2.staticflickr.com/1184/1084349065_3a55f1e974_m.jpg" alt="whenever there are umbrellas out" style="width:90%;"/>
					<ul>
						<li>
							Rainy nights and weekends where you live
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
					<h3>How do you send reminders?</h3>
					<ul>
						<li>
							E-mails are probably the best way
						</li>
						<li>
							We can send you a Tweet
						</li>
						<li>
							Text messages to most cell phone carriers
						</li>
					</ul>
					<p>You can change cities or unsubscribe at any time.</p>
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

class Region(webapp.RequestHandler):
  def get(self):
	days = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
	coders = Coder.gql('WHERE region = :1', self.request.get('region'))
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
	for coder in coders:
		wjson = fetch("http://api.wunderground.com/api/d5f91ff9e5d13cd9/forecast/q/" + coder.city + ".json", payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
		if(days[datetime.now().weekday()] == "Saturday"):
			# check daytime first
			wjson = wjson.split("icon_url")
			for day in wjson:
				if(day.find("Saturday") > -1):
					icon = day[ 3 : day.find('title') ]
					icon = icon[ 0 : icon.find('"') ]
					if(icon.find('rain') > -1 or icon.find('storm') > -1):
						# need to check that rainfall isn't so small!
						if(day.find("Saturday Night") > -1):
							self.response.out.write('Rain tonight in ' + coder.city + '!')
						else:
							self.response.out.write('Rain today in ' + coder.city + '!')						
					self.response.out.write( '<img src="' + icon + '"/><br/>' )
		elif(days[datetime.now().weekday()] == "Sunday"):
			# check daytime first
			wjson = wjson.split("icon_url")
			for day in wjson:
				if(day.find("Sunday") > -1):
					icon = day[ 3 : day.find('title') ]
					icon = icon[ 0 : icon.find('"') ]
					if(icon.find('rain') > -1 or icon.find('storm') > -1):
						# need to check that rainfall isn't so small!
						if(day.find("Sunday Night") > -1):
							self.response.out.write('Rain tonight in ' + coder.city + '!')
						else:
							self.response.out.write('Rain today in ' + coder.city + '!')						
					self.response.out.write( '<img src="' + icon + '"/><br/>' )

		elif(coder.weekendonly == "everyday"):
			today = days[datetime.now().weekday()] + " Night"
			wjson = wjson.split("icon_url")
			for day in wjson:
				if(day.find(today) > -1):
					icon = day[ 3 : day.find('title') ]
					icon = icon[ 0 : icon.find('"') ]
					if(icon.find('rain') > -1 or icon.find('storm') > -1):
						# need to check that rainfall isn't so small!
						self.response.out.write('Rain tonight in ' + coder.city + '!')
					self.response.out.write( '<img src="' + icon + '"/><br/>' )
					break
		
	self.response.out.write('			</div>\n		</div>\n	</body>\n</html>')

class Why(webapp.RequestHandler):
  def get(self):
	self.response.out.write('''<!DOCTYPE html>
<html>
It's awesome.
</html>''')

class Coder(db.Model):
	name = db.StringProperty()
	city = db.StringProperty()
	region = db.StringProperty()
	contactmethod = db.StringProperty()
	weekendonly = db.StringProperty()

application = webapp.WSGIApplication(
                                     [('/region.*', Region),
                                     ('/why.*', Why),
                                     ('/.*', HomePage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()