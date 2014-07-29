# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

# Custom importing
from base import BaseHandler
import banner.schema as schema

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class HomepageHandler(BaseHandler):
	def get(self):

		# get the current user
		user_obj = users.get_current_user()

		# Questions to show
		run_objs = schema.Runner.query().order(-schema.Runner.created).fetch()

		# Locales
		locales = {
			
			'user_obj': user_obj,
			'run_objs': run_objs

		}

		# Render the template
		self.render('main.html', locales)