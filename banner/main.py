#!/usr/bin/env python

# Python Libs
import webapp2
from webapp2_extras import routes
import jinja2
import os
import urllib

# Setup the Handlers
from banner.handlers.home import HomepageHandler
from banner.handlers.run import *

# General Config for our web application
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'secret_key_for_session_here',
}

# Startup our app with the routes we are
# going to configure now
app = webapp2.WSGIApplication([

	('/', HomepageHandler),
	('/start', RunnerStartHandler),
	webapp2.Route(r'/view/<run_id:\d+>', handler=RunnerViewHandler),
	('/update', RunnerUpdateHandler),
	('/status', RunnerStatusHandler),
	('/lease', RunnerLeaseHandler)

], debug=True, config=config)