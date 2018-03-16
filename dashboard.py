"""
Created on Tue Feb 27 21:27:55 2018

@author: abhiram haridas (abhiramharidas@gmail.com)
"""

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
import dash_utils

cred = credentials.Certificate('/home/adilash/Downloads/admin-PA.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-allocator.firebaseio.com/',
    'storageBucket': 'project-allocator.appspot.com'       
})

def network_error():

	print "\nUnable to read/write data  Check your internet connection and try again. If connection is alright modify source to view stacktrace.\n"
	
	print "\n The traceback for the error occurred\n"
	traceback.print_exc()
	print "\n\n"

	sys.exit()



def manage_users():

	print ("\nEnter 1 to manage students")
	print ("Enter 2 to manage faculty")
	print ("Enter 3 to exit")

	choice = raw_input()
	
	try:
		choice = int(choice)
	except ValueError:
		print "\nError! Invalid input.\n"
		return

	if choice == 1:

		while(1):

			print ("\nEnter 1 to add student")
			print ("Enter 2 to remove student")
			print ("Enter 3 to edit student")
			print ("Enter 4 to batch upload")
			print ("Enter 5 to view student details")
			print ("Enter 0 to exit")
			choice = raw_input()

			db_ref_string = 'Student/%s'           #Student/uid
	
			try:
				choice = int(choice)
			except ValueError:
				print "\nError! Invalid input.\n"
				continue
	
			if choice == 1:
	
				name = raw_input("\nEnter student name : ")
				login_mail = raw_input("Enter login mail : ")
				password = raw_input("Enter login password : ")
				roll_no = raw_input("Enter student roll number : ")
				p_email = raw_input("Enter personal email : ")
				phone = raw_input("Enter phone : ")
	
				
	
				try:
	
					user = auth.create_user(
    					email = login_mail,
    					email_verified = True,
    					password = password,
    					disabled=False)
	
					data = {
	
						'nameof' : name,
						'personalemail' : p_email,
						'rollnumber' : roll_no,
						'phonenumber' : phone,
						'uid' : user.uid,
						'groupid' : ''
					}
	
					db_ref = db.reference(db_ref_string % user.uid)
					db_ref.set(data)
					print('\nStudent added successfully')

				except firebase_admin.auth.AuthError as error:
					print('')
					print error.code
					#traceback.print_exc()
					continue
				except ValueError as error:
					print('')
					print error
					#traceback.print_exc()
					continue	
				except:
					network_error()

			elif choice == 2:

				login_mail = raw_input('Enter login_mail of student to be removed : ')

				try:
					user = auth.get_user_by_email(login_mail)
				except firebase_admin.auth.AuthError as error:
					print('')
					print error.code
					#traceback.print_exc()
					continue
				except ValueError as error:
					print('')
					print error					
					#traceback.print_exc()
					continue

				except:
					network_error()
					

				try:
					db_ref = db.reference(db_ref_string % user.uid)
					db_ref.delete()
					auth.delete_user(user.uid)
					print('\nStudent removed successfully')
				except:
					network_error()


			elif choice == 3:

				login_mail = raw_input('Enter login_mail of student to be edited : ')

				try:
					user = auth.get_user_by_email(login_mail)
				except firebase_admin.auth.AuthError as error:
					print('')
					print error.code
					#traceback.print_exc()
					continue
				except ValueError as error:
					print('')
					print error					
					#traceback.print_exc()
					continue

				except:
					network_error()

				print ("\nEnter 1 to edit student name")
				print ("Enter 2 to edit student phone")
				print ("Enter 3 to edit student personal email")
				print ("Enter 4 to change student password")
				print ("Enter 5 to exit")
				choice = raw_input()
	
				db_ref_string = 'Student/%s'           #Student/uid
		
				try:
					choice = int(choice)
				except ValueError:
					print "\nError! Invalid input.\n"
					continue

				if choice == 1:
					name = raw_input("Enter new name : ")

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'nameof' : name})
						print('\nName edited successfully')
					except:
						network_error()

				elif choice == 2:
					phone = raw_input("Enter new phone number : ")

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'phonenumber' : phone})
						print('\nPhone number edited successfully')
					except:
						network_error()
					

				elif choice == 3:

					p_email = raw_input("Enter new personal email : ")

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'personalemail' : p_email})
						print('\nPersonal email edited successfully')
					except:
						network_error()

				elif choice == 4:

					new_password = raw_input("Enter new password : ")

					try:
						user = auth.update_user(user.uid, password = new_password)
						print('\npassword edited successfully')
					
					except firebase_admin.auth.AuthError as error:
						print('')
						print error.code
						#traceback.print_exc()
						continue
					except:
						network_error()

				elif choice == 5:
					continue
				else:
					print "\nError! Invalid input.\n"
					continue

			elif choice ==4:
				filename=raw_input("Enter file name :")
				rows=[]
				with open(filename, 'r') as csvfile:
					csvreader=csv.reader(csvfile)

					for row in csvreader:
						rows.append(row)
				
				for row in rows:
					print(row[0]+' '+row[1])
					try:
		
						user = auth.create_user(
	    					email = row[2],
	    					email_verified = True,
	    					password = row[0],
	    					disabled=False)
		
						data = {
		
							'nameof' : row[1],
							'personalemail' : row[4],
							'rollnumber' : row[0],
							'phonenumber' : row[3],
							'uid' : user.uid,
							'groupid' : ''
						}
		
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.set(data)
						print('\n',row[0],' added successfully')

					except firebase_admin.auth.AuthError as error:
						print('')
						print error.code
						#traceback.print_exc()
						continue
					except ValueError as error:
						print('')
						print error
						#traceback.print_exc()
						continue	
					except:
						network_error()
			elif choice == 5:
				db_ref_string= 'Student'
				

			elif choice == 0:
				break
			else:
				print "\nError! Invalid input.\n"
				continue


	elif choice == 2:

		while(1):

			print ("\nEnter 1 to add faculty")
			print ("Enter 2 to remove faculty")
			print ("Enter 3 to edit faculty")
			print ("Enter 4 to exit")
			choice = raw_input()

			db_ref_string = 'Faculty/%s'           #Faculty/uid
	
			try:
				choice = int(choice)
			except ValueError:
				print "\nError! Invalid input.\n"
				continue

			if choice == 1:
	
				name = raw_input("\nEnter faculty name : ")
				login_mail = raw_input("Enter login mail : ")
				password = raw_input("Enter login password : ")
				p_email = raw_input("Enter personal email : ")
				phone = raw_input("Enter phone : ")

				try:
	
					user = auth.create_user(
    					email = login_mail,
    					email_verified = True,
    					password = password,
    					disabled=False)
	
					data = {
	
						'nameof' : name,
						'personalemail' : p_email,
						'phonenumber' : phone,
						'uid' : user.uid,
						'limit' : 5                  #default value is 5
					}
	
					db_ref = db.reference(db_ref_string % user.uid)
					db_ref.set(data)
					print('\nFaculty added successfully')

				except firebase_admin.auth.AuthError as error:
					print('')
					print error.code
					#traceback.print_exc()
					continue
				except ValueError as error:
					print('')
					print error
					#traceback.print_exc()
					continue	
				except:
					network_error()


			elif choice == 2:

				login_mail = raw_input('Enter login_mail of faculty to be removed : ')

				try:
					user = auth.get_user_by_email(login_mail)
				except firebase_admin.auth.AuthError as error:
					print('')
					print error.code
					#traceback.print_exc()
					continue
				except ValueError as error:
					print('')
					print error					
					#traceback.print_exc()
					continue

				except:
					network_error()
					

				try:
					db_ref = db.reference(db_ref_string % user.uid)
					db_ref.delete()
					auth.delete_user(user.uid)
					print('\nFaculty removed successfully')
				except:
					network_error()


			elif choice == 3:

				login_mail = raw_input('Enter login_mail of faculty to be edited : ')

				try:
					user = auth.get_user_by_email(login_mail)
				except firebase_admin.auth.AuthError as error:
					print('')
					print error.code
					#traceback.print_exc()
					continue
				except ValueError as error:
					print('')
					print error					
					#traceback.print_exc()
					continue

				except:
					network_error()

				print ("\nEnter 1 to edit faculty name")
				print ("Enter 2 to edit faculty phone")
				print ("Enter 3 to edit faculty personal email")
				print ("Enter 4 to change faculty password")
				print ("Enter 5 to change faculty limit")
				print ("Enter 6 to exit")
				choice = raw_input()
	
				db_ref_string = 'Faculty/%s'           #Faculty/uid

				try:
					choice = int(choice)
				except ValueError:
					print "\nError! Invalid input.\n"
					continue

				if choice == 1:
					name = raw_input("Enter new name : ")

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'nameof' : name})
						print('\nName edited successfully')
					except:
						network_error()

				elif choice == 2:
					phone = raw_input("Enter new phone number : ")

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'phonenumber' : phone})
						print('\nPhone number edited successfully')
					except:
						network_error()
					

				elif choice == 3:

					p_email = raw_input("Enter new personal email : ")

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'personalemail' : p_email})
						print('\nPersonal email edited successfully')
					except:
						network_error()

				elif choice == 4:

					new_password = raw_input("Enter new password : ")

					try:
						user = auth.update_user(user.uid, password = new_password)
						print('\npassword edited successfully')
					
					except firebase_admin.auth.AuthError as error:
						print('')
						print error.code
						#traceback.print_exc()
						continue
					except:
						network_error()

				elif choice == 5:
					limit = raw_input("Enter new limit : ")

					try:
						limit = int(limit)
					except ValueError:
						print "\nError! Invalid limit value.\n"
						continue

					try:
						db_ref = db.reference(db_ref_string % user.uid)
						db_ref.update({'limit' : limit})
						print('\nLimit edited successfully')
					except:
						network_error()
					
				elif choice == 6:
					continue
				else:
					print "\nError! Invalid input.\n"
					continue
				
			elif choice == 4:
				break
			else:
				print "\nError! Invalid input.\n"
				continue




def manage_AOE():

	db_ref_string = 'AreaExpertise'
	try:
		db_ref = db.reference(db_ref_string)
		data = db_ref.get()
	except:
		network_error()


	while(1):

		print ("\nEnter 1 to view Areas of Expertise")
		print ("Enter 2 to add Area of Expertise")
		print ("Enter 3 to remove Area of Expertise")
		print ("Enter 4 to edit Area of Expertise")
		print ("Enter 5 to exit")
	
		choice = raw_input()
		
		try:
			choice = int(choice)
		except ValueError:
			print "\nError! Invalid input.\n"
			continue
	
		if choice == 1:
	
			print('')
			i = 0
			for key in data:
				print i," ",data[key]
				i = i+1
	
		elif choice == 2:
	
			new_area = raw_input("Enter new Area of Expertise : ")
			
	
			try:
				new_area_ref = db_ref.push()
				new_area_ref.set(new_area)
				data[new_area_ref.key] = new_area
				print('\nArea of Expertise added successfully')

			except:
				network_error()
	
		elif choice == 3:
	
			print('')
			i = 0
			keys = []
			for key in data:
				print i," ",data[key]
				keys.append(key)
				i = i+1
	
			print('')
			index = raw_input("Enter index of item to remove : ")
	
			try:
				index = int(index)
			except ValueError:
				print "\nError! Invalid input.\n"
				continue
	
			if index >= len(data):
				print "\nError! Invalid input.\n"
				continue
	
			data.pop(keys[index])
	
			try:
				db_ref.set(data)
				print('\nArea of Expertise removed successfully')
			except:
				network_error()
	
		elif choice == 4:
	
			print('')
			i = 0
			keys = []
			for key in data:
				print i," ",data[key]
				keys.append(key)
				i = i+1
	
			print('')
			index = raw_input("Enter index of item to edit : ")
			new_val = raw_input("Enter new value : ")
	
			try:
				index = int(index)
			except ValueError:
				print "\nError! Invalid input.\n"
				continue
	
			if index >= len(data):
				print "\nError! Invalid input.\n"
				continue
	
			data[keys[index]] = new_val
	
			try:
				db_ref.set(data)
				print('\nArea of Expertise edited successfully')
			except:
				network_error()
	
		elif(choice == 5):
			return;
		else:
			print "Invalid input"

	



#============================================   MAIN FUNCTION STARTS HERE ===================================================


choice = 0
print ("Welcome to Project Allocator Admin console!\n")

while(choice != 3):	
	
	print ("\nEnter 1 to manage users")
	print ("Enter 2 to manage Areas of Expertise")
	print ("Enter 3 to exit")

	choice = raw_input()
	
	try:
		choice = int(choice)
	except ValueError:
		print "\nError! Invalid input.\n"
		choice = 0
		continue

	if(choice == 1):
		manage_users()
	elif(choice == 2):
		manage_AOE()
	elif(choice == 3):
		continue;
	else:
		print "\nError! Invalid input.\n"

