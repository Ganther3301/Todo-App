import pyrebase as pb

config = {
  'apiKey': "AIzaSyBD87_zaJDxZfjHs6GtRbdb7VwoXqyiLLA",
  'authDomain': "todo-list-2005d.firebaseapp.com",
  'databaseURL': "https://todo-list-2005d-default-rtdb.firebaseio.com",
  'projectId': "todo-list-2005d",
  'storageBucket': "todo-list-2005d.appspot.com",
  'messagingSenderId': "306565975094",
  'appId': "1:306565975094:web:4cd38637bd2deaaa6c5c97",
  'measurementId': "G-XLFG8CBGEN"
}
fb = pb.initialize_app(config)
db = fb.database()
users = db.get().val() 
title = ''
username = ''
user = dict()

def login(uname,psswd):
	global user, username
	if uname in users:
		user = dict(db.child(uname).get().val())

		if psswd == user['password']:
			user = dict(db.child(uname).get().val())
			username = uname
			return True
	else:
		return False	

def create(name, username, psswd, email):
	uname = username
	global users
	if username in users:
		return False, 'u'
	elif len(psswd) < 8:
		return False, 'p' 
	else: 
		data = {'name':name, 'password':psswd, 'email':email, 'todo':{' ': {' ': 'False'}}}
		db.child(username).set(data)		
		users = db.get().val()
		return True

def get(key, todo = False):
	if todo:
		return user['todo'][title]

	else:
		return user[key]

def addTitle(name):
	global user
	data = {name: {' ': 'False'}}
	db.child(username).child('todo').update(data)
	user = dict(db.child(username).get().val())

def deleteTitle(name):
	global user
	db.child(username).child('todo').child(name).remove()
	user = dict(db.child(username).get().val())

def addItem(name, *dateTime):
	global user
	try:
		data = {name:{'value':'False', 'remind': 'True', 'datetime':str(dateTime[0])}}
	except:
		data = {name:{'value':'False', 'remind': 'False',}}
	db.child(username).child('todo').child(title).update(data)
	user = dict(db.child(username).get().val())

def deleteItem(name):
	global user
	db.child(username).child('todo').child(title).child(name).remove()
	user = dict(db.child(username).get().val())

def updateItem():
	global user
	db.child(username).update(user)

