# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

# Custom importing
from base import BaseHandler
import banner.schema as schema
import random
import json

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class RunnerLeaseHandler(BaseHandler):
	def get(self):

		# Returns a list of leased tasks for the node to use
		q = taskqueue.Queue('banner-dots')

		# Setup 
		task_objs = q.lease_tasks(120, 5, deadline=60)

		# Loop and create proper list
		proper_task_objs = []

		for task_obj in task_objs: proper_task_objs.append( task_obj.name )

		# Returns a formatted response
		return self.response.out.write( json.dumps(proper_task_objs) )

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class RunnerStatusHandler(BaseHandler):
	def get(self):

		# get the current user
		run_str = self.request.get('run')
		x_str = self.request.get('x')
		y_str = self.request.get('y')

		# Questions to show
		run_obj = schema.Runner.get_by_id( long(run_str) )

		done_str = 'false'
		if run_obj.done != None: done_str = 'true'

		dot_objs = schema.RunnerDot.query( schema.RunnerDot.run==run_obj.key, schema.RunnerDot.done == True ).fetch()

		dotting_objs = []
		for dot_obj in dot_objs:
			dotting_objs.append( {

				'x': dot_obj.x,
				'y': dot_obj.y,
				'target': dot_obj.target

			} )

		self.response.headers['Content-Type'] ='application/json'
		self.response.out.write( json.dumps({

			'done': done_str,
			'dots': dotting_objs

		}) )
#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class RunnerUpdateHandler(BaseHandler):
	def get(self):

		# get the current user
		run_str = self.request.get('run')
		x_str = self.request.get('x')
		y_str = self.request.get('y')

		# Questions to show
		run_obj = schema.Runner.get_by_id( long(run_str) )

		if run_obj == None:
			self.response.out.write('no such run ...')
			return

		# Get all the dots !
		dot_obj = schema.RunnerDot.query( schema.RunnerDot.run==run_obj.key,schema.RunnerDot.x == int(x_str),schema.RunnerDot.y == int(y_str) ).fetch()

		if dot_obj == None or len(dot_obj) < 1:
			self.response.out.write('no such dot ...')
			return

		# Update dot !
		dot_obj = dot_obj[0]
		dot_obj.done = True
		dot_obj.put()

		# Remove task from queue
		try:
			q = taskqueue.Queue('banner-dots')
			q.delete_tasks_by_name( str(run_obj.key.id()) + '-' + str(dot_obj.x) + '-' + str(dot_obj.y) )
		except Exception, e:
			pass

		# Write out that we are done !
		self.response.out.write( 'done !' )



#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class RunnerViewHandler(BaseHandler):
	def get(self, run_id):

		# get the current user
		user_obj = users.get_current_user()

		# Questions to show
		run_obj = schema.Runner.get_by_id( long(run_id) )

		if run_obj == None or run_obj == False: self.redirect('/')

		# Get all the dots !
		dot_objs = schema.RunnerDot.query( schema.RunnerDot.run==run_obj.key ).fetch()

		# Create dict
		mapping_dict = {}
		for dot_obj in dot_objs:
			target_str = dot_obj.target

			if dot_obj.done == False: target_str = 'white'

			mapping_dict[ str(dot_obj.x) + '-' + str(dot_obj.y) ] = target_str

		# Locales
		locales = {
			
			'user_obj': user_obj,
			'run_obj': run_obj,
			'mapping_dict': mapping_dict,
			'height': range(0, run_obj.height),
			'width': range(0, run_obj.width)

		}

		# Render the template
		self.render('view.html', locales)

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class RunnerStartHandler(BaseHandler):
	def get(self):

		# Add to the queue
		q = taskqueue.Queue('banner-dots')

		winning_member_str = ''

		# Go get a swag winner
		with open('members.csv') as f:
			content = f.readlines()

			winning_member_str = random.choice( content ).strip()

		# Image we are going to create
		banner_img = [

			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#'],
			['#','#','#','#','#','#','#','#','#','#','#']
		]

		width_count = len(banner_img[0])
		height_count = len(banner_img)

		# Create the schema obj
		run_obj = schema.Runner()
		run_obj.winner = winning_member_str
		run_obj.instance_count = False
		run_obj.width = width_count
		run_obj.height = height_count
		run_obj.put()

		# Create all of the dots
		dot_objs = []
		x = 0
		y = 0

		# Loop our image to create
		for row in banner_img:

			for column in row:

				# Add it !
				dot_obj = schema.RunnerDot()
				dot_obj.run = run_obj.key
				dot_obj.x = x
				dot_obj.y = y
				dot_obj.done = False

				if column == '#':
					dot_obj.target = 'green'
				else:
					dot_obj.target = 'red'

				dot_objs.append( dot_obj )
				
				x = x + 1

			x = 0
			y = y + 1

		# Save all the dots
		ndb.put_multi( dot_objs )

		# Then start a task in the queue for each
		for dot_obj in dot_objs: 
			payload_str = str( run_obj.key.id() ) + "-" + str( dot_obj.x ) + "-" + str( dot_obj.y )
			q.add( taskqueue.Task(name=payload_str, payload=payload_str, method='PULL') )

		# Redirect to this run
		self.redirect('/view/' + str(run_obj.key.id()))
