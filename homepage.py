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

	self.response.out.write('''<!DOCTYPE html>
<html>
</html>''')

class Region(webapp.RequestHandler):
  def get(self):
	days = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
	coders = Coder.gql('WHERE region = :1', self.request.get('region'))
	self.response.out.write('<!DOCTYPE html>\n<html>\n')
	for coder in coders:
		wjson = fetch("http://api.wunderground.com/api/d5f91ff9e5d13cd9/forecast/q/" + coder.city + ".json", payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
		today = days[datetime.now().weekday()] + " Night"
		wjson = wjson.split("icon_url")
		for day in wjson:
			if(day.find(today) > -1):
				icon = day[ 3 : day.find('title') ]
				icon = icon[ 0 : icon.find('"') ]
				if(icon.find('rain') > -1 or icon.find('storm') > -1):
					self.response.out.write('Send a message!')
				self.response.out.write( '<img src="' + icon + '"/>' )
				break
		
	self.response.out.write('</html>')

class Coder(db.Model):
	name = db.StringProperty()
	city = db.StringProperty()
	region = db.StringProperty()
	contactmethod = db.StringProperty()
	weekendonly = db.StringProperty()

application = webapp.WSGIApplication(
                                     [('/', HomePage),
                                     ('/region.*', Region)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()