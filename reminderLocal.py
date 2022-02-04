import pyrebase as pb
import yagmail
import pause
import datetime	
import multiprocessing

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
users = dict(db.get().val())


yagmail.register('todolistreminder123@gmail.com', 'Project123')

yag = yagmail.SMTP('todolistreminder123@gmail.com')

def reminder():
	users = dict(db.get().val()) 
	remind = [] 

	for user in users:
		for task_title in users[user]['todo']:
			for task_name in users[user]['todo'][task_title]:
				if task_name != ' ':
					if(users[user]['todo'][task_title][task_name]["value"] == "False" and users[user]['todo'][task_title][task_name]["remind"] == "True"):
						dateTime = datetime.datetime.strptime(users[user]['todo'][task_title][task_name]["datetime"], '%Y-%m-%d %X')
						if(datetime.datetime.now() > dateTime):
							users[user]['todo'][task_title][task_name]["value"] = "incomplete"
						elif(dateTime not in remind):
							remind.append(dateTime)

	db.update(users)
	remind.sort()

	for i in remind:
		print(f'Waiting for {str(i)}')
		pause.until(i)
		remindEmails = {}  

		for user in users:
			for task_title in users[user]['todo']:
				for task_name in users[user]['todo'][task_title]:
					if task_name != ' ':
						if(users[user]['todo'][task_title][task_name]["value"] == "False" and users[user]['todo'][task_title][task_name]["remind"] == "True"):
							dateTime = datetime.datetime.strptime(users[user]['todo'][task_title][task_name]["datetime"], '%Y-%m-%d %X')
							if(dateTime == i):
								users[user]['todo'][task_title][task_name]["value"] = 'incomplete'
								if(users[user]['email'] not in remindEmails): 
									remindEmails[users[user]['email']] = []
								remindEmails[users[user]['email']].append(task_name)	

		for email in remindEmails:
			for task in remindEmails[email]:
				yag.send(to = email, subject = 'You have an incomplete task', contents = f'Your task \'{task}\' is not completed yet. Please reschedule it')	
				print(f'mail sent to {email} about {task}')
		db.update(users)

process1 = multiprocessing.Process(target = reminder,)

def checker():
	global process1
	process1.start()
	while True:
		users = dict(db.get().val())
		time.sleep(5)
		if(users == dict(db.get().val())):
			print('Not changed')
			continue
		print("Changed")
		process1.kill()
		process1 = multiprocessing.Process(target = reminder,)
		process1.start()


process2 = multiprocessing.Process(target = checker)

if __name__ == '__main__':
	process2.start()

