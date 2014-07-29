# Google Libraries
from google.appengine.ext import ndb

#
# Event Details
# @author Johann du Toit
#
class Runner(ndb.Model):
	instance_count = ndb.IntegerProperty()
	winner = ndb.StringProperty()
	created = ndb.DateTimeProperty(auto_now_add=True)
	width = ndb.IntegerProperty()
	height = ndb.IntegerProperty()
	done = ndb.DateTimeProperty(default=None)
	lastupdated = ndb.DateTimeProperty(auto_now_add=True,auto_now=True)

#
# Event Details
# @author Johann du Toit
#
class RunnerDot(ndb.Model):
	run = ndb.KeyProperty(kind=Runner)
	x = ndb.IntegerProperty()
	y = ndb.IntegerProperty()

	target = ndb.StringProperty()

	done = ndb.BooleanProperty(default=False)
	created = ndb.DateTimeProperty(auto_now_add=True)
	lastupdated = ndb.DateTimeProperty(auto_now_add=True,auto_now=True)
