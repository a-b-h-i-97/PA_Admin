import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import auth

import sys
import traceback
import json
from datetime import datetime
import csv

# cred = credentials.Certificate('admin-PA.json')

# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://project-allocator.firebaseio.com/',
#     'storageBucket': 'project-allocator.appspot.com'       
# })

def network_error():
	print "\nUnable to read/write data  Check your internet connection and try again. If connection is alright modify source to view stacktrace.\n"
	print "\n The traceback for the error occurred\n"
	traceback.print_exc()
	print "\n\n"
	sys.exit()

def archiveAll():
	db_ref_string='RequestQueue'
	try:
		# db_ref = db.reference(db_ref_string)
		Projects = db.reference('AcceptProject').get()
	except:
		network_error()
	try:
		db_ref = db.reference("AreaExpertise")
		Expertises = db_ref.get()
	except:
		network_error()
	try:
		db_ref = db.reference("Faculty")
		Faculties = db_ref.get()
	except:
		network_error()
	try:
		db_ref = db.reference("Group")
		Groups = db_ref.get()
	except:
		network_error()
	try:
		db_ref = db.reference("Student")
		Students = db_ref.get()
	except:
		network_error()
	# studentData={
	# 				'personalemail' :'',
	# 				'nameof'  :'',
	# 				'phonenumber'	  :''		
	# }
	db_ref_string='Archive/%s'
	year=raw_input("Enter the year ")
	db_ref=db.reference(db_ref_string % year)

	i = 0
	for Project in Projects.values():

		new_archive=db_ref.push()

		data= {
		'areas':[],
		'description':'',
		'faculty':{
					'personalemail':'',
					'nameof':'',
					'phonenumber':''
					},
		'link':'',
		'student':[],
		'topic':''

		}

		# print str(Project['areas'])
		for area in Project['areas']:
			data['areas'].append(area)

		# print str(data['areas'])
		faculty=Project['faculty']
		facultyData=Faculties.get(faculty)
		# print("11111111111")
		# print str(facultyData)
		data['link']=Project['link']

		data['faculty']['personalemail']=facultyData['personalemail']
		data['faculty']['nameof']=facultyData['nameof']
		data['faculty']['phonenumber']=facultyData['phonenumber']
		group = Project['groupid']

		# print str(Groups[group])

		i = 0

		for suid in Groups[group]:

			data['student'].append({})

			# print str(Students.get(suid))
			data['student'][i]['personalemail']=Students.get(suid)['personalemail']
			data['student'][i]['nameof']=Students.get(suid)['nameof']
			data['student'][i]['phonenumber']=Students.get(suid)['phonenumber']
			i = i + 1

			# print str(data['student'])

		data['topic']=Project['topic']
		data['description']=Project['description']
		# print str(Project)
		# print str(data)
		print " {: <10}{: <25} archived".format(data['topic'],data['faculty']['nameof'])
		new_archive.set(data)
		print("------------------------------------------------------")



	

