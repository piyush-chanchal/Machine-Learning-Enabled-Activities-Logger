#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 23:20:08 2020

@author: piyush
"""








class mainWindow():
    def __init__(self,root,heightMain,widthMain):
        root.geometry(""+str(widthMain)+"x"+str(heightMain))
        root.title("Activities logger")
        cnvsStruct = Canvas(root)
        cnvsStruct.place(x=0,y=0,width=widthMain,height=heightMain)

        ############Menu section
        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Exit', command=root.destroy)

        #####Add categories Menu options
        self.addCatMenu = Menu(self.menu,tearoff=False)
        self.menu.add_cascade(label="Options",menu=self.addCatMenu)
        self.addCatMenu.add_command(label="Add/Remove Categories",command=self.fnAddCat)

        #####Help Menu
        self.helpmenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About',command=self.aboutMenu)

        




        #Placeholder for showing top 4 suggested categories by machine learning algorithm
        cnvsStruct.create_rectangle(((widthMain*80)/100),0,widthMain,(heightMain/4),fill="#003d66",outline="")
        cnvsStruct.create_rectangle(((widthMain*80)/100),(heightMain/4),widthMain,(heightMain/2),fill="#0099ff",outline="")
        cnvsStruct.create_rectangle(((widthMain*80)/100),(heightMain/2),widthMain,((heightMain*75)/100),fill="#80ccff",outline="")
        cnvsStruct.create_rectangle(((widthMain*80)/100),((heightMain*75)/100),widthMain,heightMain,fill="#e6f5ff",outline="")
        cnvsStruct.create_rectangle(0,((heightMain*60)/100),((widthMain*80)/100),heightMain,fill="#bfbfbf",outline="")



        #Entry widget for hours and minutes
        self.inHrs = Entry(root,bg="#f2f2f2",font=("Times",50))
        self.inHrs.place(x=5,y=30,width=80,height=50)

        lblSep = Label(root,text=":",font=("Times",30))
        lblSep.place(x=100,y=40,width=15,height=25)

        self.inMns = Entry(root,bg="#f2f2f2",font=("Times",50))
        self.inMns.place(x=125,y=30,width=100,height=50)

        #Label widget for hours and minutes
        lblHrs = Label(root,text="Hours",font=("Times",20,"bold"))
        lblHrs.place(x=15,y=10,height=20)

        lblMns = Label(root,text="Minutes",font=("Times",20,"bold"))
        lblMns.place(x=130,y=10,height=20)


        #Entry and label widget for Title/Summary
        self.inTitle = Entry(root,bg="#f2f2f2",font=("Times",25))
        self.inTitle.place(x=5,y=111,width=500,height=40)

        lblTitle = Label(root,text="Summary",font=("Times",18,"bold"))
        lblTitle.place(x=15,y=92,height=20)


        #Label and Entry widget of Description
        lblDesc = Label(root,text="Detail",font=("Times",18,"bold"))
        lblDesc.place(x=15,y=165,height=20)

        self.inDesc = Text(root,bg="#f2f2f2",font=("Times",20))
        self.inDesc.place(x=5,y=185,height=165,width=350)

        #Submit button widget
        #bg option not working in mac so used highlightbackground instead
        self.btnSubmit = Button(root,highlightbackground="gray",text="Submit",font=("Times",50,"bold"), command = self.submitButAction)
        self.btnSubmit.place(x=370,y=180,height=178,width=268)

        #Date and Time label widget
        lblHeader = Label(root,text="Activity done at:\n",fg="#000000",font=("Times",15,"bold"))
        lblHeader.place(x=240,y=0)

        
        self.lblDateTime = Label(root,font=("Times",18))
        self.lblDateTime.place(x=240,y=20) 
        
        #rendering time dynamically
        self.time()

        btnDateChange = Button(root,text="Change",highlightbackground="#e6e6e6",font=("Times",12,"bold"),command=self.changeButAction)
        btnDateChange.place(x=320,y=40,height=20)


        #Label of category list
        self.lblCat = Label(root,text="Categories",font=("Times",14,"bold"))
        self.lblCat.place(x=400,y=10)

        
        #rendering main category drop down list
        self.mainCatList = ttk.Combobox(root,font=("Times",18))
        self.mainCatList.place(x=400,y=30,width=230)

        self.catListUpdate()
        self.modelTraining()


    def modelTraining(self):
        df = pd.read_csv("/Users/piyush/Desktop/ProjectsGitHub/ActivitiesLoggerV1/Data/20201203.csv")
        df_new = df[['TotalMinutes','ActivityDoneTimeNumeric','Category']]
        inputs = df_new.drop('Category',axis='columns')
        target = df_new[['Category']]
        from sklearn.preprocessing import LabelEncoder
        le_category = LabelEncoder()
        target['Category_n'] = le_category.fit_transform(target['Category'])
        target = target.drop('Category',axis="columns")
        from sklearn import tree
        model = tree.DecisionTreeClassifier()
        model.fit(inputs,target)
        print(model.predict([[400,50.67]]))


    def catListUpdate(self):
        dfCatMain = pd.read_csv("/Users/piyush/Desktop/ProjectsGitHub/ActivitiesLoggerV1/catData/mainCat.csv",index_col=False)
        catList = ['*Please Select Category']

        dfRow,dfCol = dfCatMain.shape
        for catIter in range(dfRow):
            catList.append(dfCatMain['mainCatName'][catIter])

        self.mainCatList['values'] = tuple(catList)
        self.mainCatList.current(0)
    
    def time(self):
        self.dateTimeNow = datetime.now()
        self.strDateTime = str(self.dateTimeNow.strftime("%x"))+"\n"+str(self.dateTimeNow.strftime("%X"))
        self.lblDateTime.config(text=self.strDateTime)
        self.timer = self.lblDateTime.after(1000,self.time)
    
      
    def aboutMenu(self):
    #    self.AbtWin = Toplevel(root)
    #    self.AbtWin.overrideredirect(1)
    #    self.AbtWin.configure(bg="#000000",bd=1)
    #    self.AbtWin.geometry("173x143+300+300")
    #    self.Msg = Message(self.AbtWin, text="This application is developed in Python by using TextBlob and TKinter library. In case of any concern, please contact to email id Piyush.Chanchal@hotmail.com",bg='#F5F5F5')
    #    self.Msg.pack()
    #    self.OKBtn= Button(self.AbtWin,text='OK',width=173,command=self.AbtWin.destroy,bg='#696969',fg='#ffffff')
    #    self.OKBtn.pack()
    #    self.AbtWin.mainloop()
        print("About button has been pressed")

    def fnAddCat(self):
        self.flgRem=0
        self.mainCatWin = Toplevel(root)
        Label(self.mainCatWin,text="Category name").place(x=10,y=10)
        self.inNewCat = Entry(self.mainCatWin)
        self.inNewCat.place(x=10,y=30)
        Button(self.mainCatWin,text="Add",command=self.addNewMainCat).place(x=10,y=60)
        Button(self.mainCatWin,text="Remove",command=self.fnRemoveMainCat).place(x=60,y=60)
        if path.exists("catData/mainCat.csv"):
            self.fetchMainCat()

    def fnRemoveMainCat(self):
        self.flgRem=0
        dfCatMain = pd.read_csv("/Users/piyush/Desktop/ProjectsGitHub/ActivitiesLoggerV1/catData/mainCat.csv",index_col=False)
        dfRow,dfCol = dfCatMain[dfCatMain.mainCatName==self.inNewCat.get()].shape
        if(dfRow>0):
            dropRowInd = dfCatMain[dfCatMain.mainCatName==self.inNewCat.get()].index
            print(dfCatMain)
            dfCatMain = dfCatMain.drop([dfCatMain.index[dropRowInd[0]]])
            dfCatMain.to_csv('catData/mainCat.csv',mode='w',index=False)
            self.flgRem=1
            self.fetchMainCat()
            self.catListUpdate()

        if(dfRow<1):
            messagebox.showerror("showerror", "Main Category does not exist")


    def fetchMainCat(self):
        self.mainCatCsv = pd.read_csv("catData/mainCat.csv")
        yAxisVal = 110
        for mainCatIter in range(len(self.mainCatCsv.index.unique())):
            yAxisVal = yAxisVal + 20
            catIter = Label(self.mainCatWin,text=str(self.mainCatCsv.index[mainCatIter]+1)+". "+str(self.mainCatCsv['mainCatName'].unique()[mainCatIter]))
            catIter.place(x=10,y=yAxisVal)
            if self.flgRem==1:
                nextCatBlnk = Label(self.mainCatWin,text="                                       ")
                nextCatBlnk.place(x=10,y=yAxisVal+20)

    def addNewMainCat(self):
        dfCatMain = pd.read_csv("/Users/piyush/Desktop/ProjectsGitHub/ActivitiesLoggerV1/catData/mainCat.csv",index_col=False)
        dfRow,dfCol = dfCatMain[dfCatMain.mainCatName==self.inNewCat.get()].shape
        if(dfRow>0):
            messagebox.showerror("showerror", "Main Category already exist")

        if(dfRow<1):
            newDictRow = {"mainCatName":str(self.inNewCat.get())}
            dfCatMain = dfCatMain.append(newDictRow,ignore_index=True)
            dfCatMain.to_csv('catData/mainCat.csv',mode='w',index=False)
            self.fetchMainCat()
            self.catListUpdate()


    def changeButAction(self):
        print("Change button has been pressed")
        self.calWin = Toplevel(root)
        self.cal = Calendar(self.calWin,
                   font="Arial 14", selectmode='day',
                   cursor="arrow", year=2020, month=12, day=3)
        self.cal.pack(fill="both", expand=True)
        Button(self.calWin, text="ok", command=self.timepick).pack()


    def timepick(self):
        self.calVal = self.cal.selection_get()
        self.timePick = Toplevel(self.calWin)
        Label(self.timePick,text="ENTER TIME \nFormat HH:MM:SS\n(24 Hrs)").pack()
        self.inTime = Entry(self.timePick)
        self.inTime.insert(1,"01:00:00")
        self.inTime.pack()
        Button(self.timePick,text="ok",command=self.timeValPick).pack()
        print(self.calVal)
    
    def timeValPick(self):
        self.timeVal = self.inTime.get()
        print(self.timeVal)
        self.lblDateTime.after_cancel(self.timer)
        self.lblDateTime.config(text=""+ str(self.calVal) + "\n" + str(self.timeVal))
        self.calWin.destroy()
        self.inTime.destroy()


    def submitButAction(self):
        print("Submit button has been pressed")
        self.strYYYYMMDD = str(self.dateTimeNow.strftime("%Y"))+str(self.dateTimeNow.strftime("%m"))+str(self.dateTimeNow.strftime("%d"))
        print(self.strYYYYMMDD)

        self.sNum=1


        ##Retrieving all fields data and saving into variables. Then writing it into csv files
        self.hours=str(self.inHrs.get())
        self.minutes=str(self.inMns.get())
        self.totalMinutes=(int(self.hours)*60)+int(self.minutes)
        self.actDoneOn=str(self.lblDateTime.cget("text")[0:self.lblDateTime.cget("text").find("\n")])
        self.actDoneAt=str(self.lblDateTime.cget("text")[self.lblDateTime.cget("text").find("\n")+1:])
        self.actLoggedOn=str(self.dateTimeNow.strftime("%x"))
        self.actLoggedAt=str(self.dateTimeNow.strftime("%X"))
        self.lblDispDateTime = self.lblDateTime["text"]
        self.lblDispTimeHrs=int(self.lblDispDateTime[int(self.lblDispDateTime.find("\n")+1):self.lblDispDateTime.find(":")])
        self.lblDispTimeMins=int(self.lblDispDateTime[self.lblDispDateTime.find(":")+1:self.lblDispDateTime.rfind(":")])
        self.lblDispTimeSec=int(self.lblDispDateTime[self.lblDispDateTime.rfind(":")+1:])
        self.ActivityDoneTimeNumeric=self.lblDispTimeHrs + (self.lblDispTimeMins/60) + (self.lblDispTimeSec/(60*60))
        self.catValue=self.mainCatList.get()
        self.titleText=self.inTitle.get()
        self.desText=self.inDesc.get("1.0","end-1c")
        self.csvWrite()



    def csvWrite(self):
        flgCSV = 0
        if path.exists("Data/" + self.strYYYYMMDD + ".csv"):
            flgCSV = 1
        with open("Data/" + self.strYYYYMMDD + ".csv", 'a', newline='') as csvfile:
            inData = csv.writer(csvfile)
            if flgCSV==0:
                inData.writerow(['S. No.', 'hours', 'Minutes', 'TotalMinutes','Activity done on(date)', 'Activity done at(time)','ActivityDoneTimeNumeric','Activity logged on(date)', 'Activity logged at(time)','Category','Title','Description'])
            inData.writerow([self.sNum,self.hours, self.minutes, self.totalMinutes,self.actDoneOn,self.actDoneAt,self.ActivityDoneTimeNumeric,self.actLoggedOn,self.actLoggedAt,self.catValue,self.titleText,self.desText])


from tkinter import *
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox
import csv
import os.path
from os import path
from tkcalendar import Calendar, DateEntry
import pandas as pd

root = Tk()


#Height and Width of main window
heightMain=600
widthMain=800

mainWindow(root,heightMain,widthMain)

root.mainloop()


 
