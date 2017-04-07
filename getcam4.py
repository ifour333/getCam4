import urllib
import os
import threading
import subprocess
from Tkinter import *

# TODO(blade1204) Add real time file size text

class getCam4Video(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText["text"] = "Url : "
        self.inputText.grid(row=0, column=0)

        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=6)

        self.get = Button(self)
        self.get["text"] = "Get"
        self.get["command"] = self.startMethod
        self.get.grid(row=2, column=0)

        self.get = Button(self)
        self.get["text"] = "Stop"
        self.get["command"] = self.stopMethod
        self.get.grid(row=2, column=1)

        self.displayText = Label(self)
        self.displayText["text"] = "something happened"
        self.displayText.grid(row=3, column=0, columnspan=7)

    def startMethod(self):
        self.userinput = self.inputField.get()
        if self.userinput == "":
            self.displayText["text"] = "No input string!!"
        else:
            self.displayText["text"] = self.inputField.get()
            self.getCam4(self.inputField.get())

    def stopMethod(self):
        self.displayText["text"] = "closed"
        stdout.close()
        stderr.close()
        p.terminate()

    def getCam4(self, url):
        # url = "http://zh.cam4.com/sensationnow"
        # url = input()
        content = urllib.urlopen(url).read()

        videoAppUrlStart = 12
        videoAppUrl = ""
        while content[content.find("videoAppUrl") + videoAppUrlStart] != '&':
            videoAppUrl += content[content.find("videoAppUrl") +
                                   videoAppUrlStart]
            videoAppUrlStart += 1
        print videoAppUrl

        videoPlayUrlStart = 13
        videoPlayUrl = ""
        while content[content.find("videoPlayUrl") + videoPlayUrlStart] != '&':
            videoPlayUrl += content[content.find(
                "videoPlayUrl") + videoPlayUrlStart]
            videoPlayUrlStart += 1
        print videoPlayUrl

        playerUrlStart = 12
        playerUrl = ""
        while content[content.find("playerUrl") + playerUrlStart] != '"':
            playerUrl += content[content.find("playerUrl") + playerUrlStart]
            playerUrlStart += 1
        print playerUrl

        command = "rtmpdump -r " + videoAppUrl + " -y " + videoPlayUrl + \
            " -W " + playerUrl + " -V -o " + videoPlayUrl + ".flv"
        print command

        threading.Thread(target=self.startcatch(command),
                         args=(), name='thread-catch').start()

    def startcatch(self, command):
        global p
        global stdout
        global stderr
        stdout = open("stdout.txt", "wb")
        stderr = open("stderr.txt", "wb")
        p = subprocess.Popen(command, stdout=stdout, stderr=stderr)
        self.displayText["text"] = p
        # subprocess.Popen([command],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    root = Tk()
    app = getCam4Video(master=root)
    app.mainloop()
