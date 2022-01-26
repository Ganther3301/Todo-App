import yagmail

async def run():
	yagmail.register('todolistreminder123@gmail.com', 'Project123')

	yag = yagmail.SMTP('todolistreminder123@gmail.com')

	yag.send(to = 'hithesh2k2@gmail.com', subject = 'This is a test', contents = 'Hello')

run()