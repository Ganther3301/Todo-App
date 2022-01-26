import os
import dotenv
import yagmail

dotenv.load_dotenv()

yagmail.register(os.getenv('EMAIL'), os.getenv('PASSWORD'))

yag = yagmail.SMTP(os.getenv('EMAIL'))

yag.send(to = 'hithesh2k2@gmail.com', subject = 'This is a test', contents = 'Hello')
