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
users = dict(db.get().val()) 

def sort(unsorted_data):
	int_data = []

	for date, times in unsorted_data.items():
		date = date.split("-")
		for d in date:
			date[date.index(d)] = int(d)

		int_times = []

		for time in times:
			time = int(time.replace(":", ""))
			int_times.append(time)

		int_times.sort()
		int_data.append((date, int_times))

	#Sort dates
	for i in range(len(int_data)):
		minimum_index = i
		for j in range(i+1, len(int_data)):
			if(int_data[j][0][2] < int_data[minimum_index][0][2]):
				minimum_index = j
			elif(int_data[j][0][1] < int_data[minimum_index][0][1]):
				minimum_index = j
			elif(int_data[j][0][0] < int_data[minimum_index][0][0]):
				minimum_index = j

		temp = int_data[i]
		int_data[i] = int_data[minimum_index]
		int_data[minimum_index] = temp

	sorted_data = {}

	for data in int_data:
		date = ""
		for i in data[0]:
			date += str(i) + "-"
		date=date[:-1]

		times = []

		for j in data[1]:
			j = str(j)
			if(len(j) != 4):
				j = "0"*(4-len(j)) + j
			times.append(j[:2] + ":" + j[2:])

		sorted_data[date] = times

	return(sorted_data)



remind = {}

# print(users)
for user in users:
	print(user)
	for task_title in users[user]['todo']:
		for task_name in users[user]['todo'][task_title]:
			if task_name != ' ':
				print(task_name)
				if(users[user]['todo'][task_title][task_name]["value"] == "False"):
					if(users[user]['todo'][task_title][task_name]["date"] not in remind):
						remind[users[user]['todo'][task_title][task_name]["date"]] = []
					remind[users[user]['todo'][task_title][task_name]["date"]].append(users[user]['todo'][task_title][task_name]["time"])
dates = sort(remind)
print(dates)

for date in dates:
	for time in dates[date]:
		timeList = list(map(int, time.split(':')))
		print(timeList)