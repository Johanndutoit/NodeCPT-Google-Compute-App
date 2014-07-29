# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

# Python Apis
import webapp2
import os
import jinja2
import os
import time
import logging
import uuid

# Setup our Jinja Runner
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('views'))

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class BaseHandler(webapp2.RequestHandler):

	# Do some general checks
	# here we mostly just check users
	def dispatch(self):

		# Right carry on
		super(BaseHandler, self).dispatch()

	# Our global key to check for if
	# a site comes in
	viewing_site_key = None

	# Our defaults
	defaults = {

		'user_obj': users.get_current_user()

	}

	#
	# Merges and returns the template vars.
	# Just a quick util method
	#
	def get_default_template_vars(self, current_vars):

		if current_vars != None:

			return dict(self.defaults.items() + current_vars.items())

		else:

			return self.defaults

	#
	# Custom helping method
	#
	def render(self, template_str, template_vars=None):
		template_vars = self.get_default_template_vars(template_vars)
		template = jinja_environment.get_template(template_str)
		self.response.out.write(template.render(template_vars))


