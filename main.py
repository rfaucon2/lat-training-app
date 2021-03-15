import tkinter as tk
import os
from random import seed, randint
from urllib.request import pathname2url
import sqlite3

personnes = ['premiere personne \ndu singulier', 'deuxieme personne \ndu singulier', 'troisieme personne \ndu singulier', 'premiere personne \ndu pluriel', 'deuxieme personne \ndu pluriel', 'troisieme personne \ndu pluriel']

temps = ['present', 'imparfait', 'parfait']

termG1 = ['o', 'as', 'at', 'amus', 'atis', 'ant']
termG2 = ['eo', 'es', 'et', 'emus', 'etis', 'ent']
termG3 = ['o', 'is', 'it', 'imus', 'itis', 'unt']
termG3_5 = ['io', 'is', 'it', 'imus', 'itis', 'iunt']
termG4 = ['io', 'is', 'it', 'imus', 'itis', 'iunt']

termImp = ['bam', 'bas', 'bat', 'bamus', 'batis', 'bant']

termPerf = ['i', 'isti', 'it', 'imus', 'istis', 'erunt']

class App(tk.Frame):
    #Init functions
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        #Init the root of the window
        self.root = master
        #Create the database connection variable
        self.conn = None
        #init the point variable
        self.point = 0
        self.pointCounterLabel = tk.StringVar()
        self.pointCounterLabel.set("Points: "+str(self.point))
        #Init the consigne variable
        self.consigne = tk.StringVar()
        #init the background color variable
        self.bgcolor = "#1f1f1f"
        #use the init functions
        self.initvariables()
        self.initWindow()
        self.initDB()
        self.getDBLength()
        self.initLevelChoiceScreen()
        


    def initvariables(self):
        #Init the answer variables
        self.answer = ""
        self.trueAnswer = tk.StringVar()
        #Init the list that contain the already done verbes
        self.done = []
        #init the variable the contain the last verbe done
        self.last = ""
        #init the point variable
        self.point = 0
        self.pointCounterLabel = tk.StringVar()
        self.pointCounterLabel.set("Points: "+str(self.point))
        #Init the consigne variable
        self.consigne = tk.StringVar()

    def initWindow(self):
        #Init the size of the window
        self.root.geometry("480x360")
        #Set the resizability to false
        self.root.resizable(False, False)
        #set the tits to that thing
        self.root.title("uizeiuzbeoifuyz")
        #Set the icon of the window
        self.root.iconbitmap("cursed_cat.ico")
        #Set the background color of the window
        self.root.config(bg=self.bgcolor)

    def initLevelChoiceScreen(self):
        self.clearWindow()

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', font=('Courrier', 15), padx=75, bg=self.bgcolor)
        self.space.grid(row=0, column=0)

        #Create a label to tell the user what is this screen
        self.label = tk.Label(self.root, text="Choisis la difficulté", bg=self.bgcolor, fg='white', font=('Courrier', 15))
        self.label.grid(row=0, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', font=('Courrier', 15), padx=75, bg=self.bgcolor)
        self.space.grid(row=1, column=0)

        #Create a button to select level 1
        self.lv1 = tk.Button(self.root, text="Niveau 1: \nSeulement le présent.", command=self.setDif1)
        self.lv1.grid(row=2, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', font=('Courrier', 15), padx=75, bg=self.bgcolor)
        self.space.grid(row=3, column=0)

        #Create a button to select level 2
        self.lv2 = tk.Button(self.root, text="Niveau 2: \nPrésent et imparfais.", command=self.setDif2)
        self.lv2.grid(row=4, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', font=('Courrier', 15), padx=75, bg=self.bgcolor)
        self.space.grid(row=5, column=0)

        #Create a button to select level 3
        self.lv3 = tk.Button(self.root, text="Niveau 3: \nPrésent, imparfais et parfait.", command=self.setDif3)
        self.lv3.grid(row=6, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', font=('Courrier', 15), padx=75, bg=self.bgcolor)
        self.space.grid(row=7, column=0)

        #Create a label to tell a user why there is the slider
        self.label = tk.Label(self.root, text='Longueur du test:', fg="white", font=('Courrier', 10), bg=self.bgcolor)
        self.label.grid(row=8, column=1)

        #create the slider to sel the test length
        self.lengthSlider = tk.Scale(self.root, from_=5, to=(self.dicoLength * 2), orient="horizontal", highlightthickness=0, bg=self.bgcolor, fg='white')
        self.lengthSlider.grid(row=9, column=1)

    def initGameWindow(self):
        self.clearWindow()
        self.initvariables()

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', pady=25, padx=40, bg=self.bgcolor)
        self.space.grid(row=0, column=0)

        #Create the consigne label
        self.consigneLabel = tk.Label(self.root, textvariable=self.consigne , font=("Courrier", 15), fg='white', bg=self.bgcolor)
        self.consigneLabel.grid(row=1, column=1)

        #Create the point counter
        self.pointCounter = tk.Label(self.root, textvariable=self.pointCounterLabel, font=("Courrier", 10), fg='white', bg=self.bgcolor, justify='right')
        self.pointCounter.grid(row = 0, column=0)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', pady=50, padx=40, bg=self.bgcolor)
        self.space.grid(row=2, column=0)

        #Init the text entry and a label to tell the user how to validate
        self.answerEntry = tk.Entry(self.root, textvariable=self.answer, width=25, font=("Courrier", 10))
        self.answerEntry.grid(row=3, column=1)
        self.label = tk.Label(self.root, text = "Appuyez sur entrer\npour valider", bg=self.bgcolor, fg='white')
        self.label.grid(row=4, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', font=("Courrier", 5), bg=self.bgcolor)
        self.space.grid(row=5, column=0)

        #Create a button to go to the menu
        self.lv1 = tk.Button(self.root, text="End", command=self.endGame, font=("Courrier", 15))
        self.lv1.grid(row=6, column=0, sticky='sw')

        #Bind the key enter to the function verifAnswer
        self.root.bind('<Return>', self.verifAnswer)
        self.baseLength = self.testLength
        #Pick a consigne and start the game
        self.pickConsigne()
    
    ######################################################

    #Database init functions
    def initDB(self):
        #Try to connect to the database
        if not os.path.isfile('dico.db'):
            self.DBErrorScreen()
        else:
            self.conn = sqlite3.connect('dico.db')
            self.c = self.conn.cursor()

    def DBErrorScreen(self):
        self.clearWindow()
        self.label = tk.Label(self.root, justify='left', fg = 'white', bg = self.bgcolor, font = ('Courrier', 20) , text="Error: Could not load the file 'dico.db'. \n\nMake sure this file is in the same folder \nas the file 'App.exe'.")
        self.label.grid()
        
    def getDBLength(self):
        i = 1
        while True:
            self.c.execute("SELECT id FROM verbes WHERE id = {}".format(i))
            if self.c.fetchone() == None:
                if i == 1:
                    self.dicoLength = i
                else:
                    self.dicoLength = i-1
                    break
            else: 
                i += 1

    ######################################################

    #Difficulty functions
    
    def setDif1(self):
        #set the test difficulty
        self.difficulty = 1
        #set the test length
        self.testLength = int(self.lengthSlider.get())
        #init the game window
        self.initGameWindow()

    def setDif2(self):
        #set the test difficulty
        self.difficulty = 2
        #set the test length
        self.testLength = int(self.lengthSlider.get())
        #init the game window
        self.initGameWindow()

    def setDif3(self):
        #set the test difficulty
        self.difficulty = 3
        #set the test length
        self.testLength = int(self.lengthSlider.get())
        #init the game window
        self.initGameWindow()
    
    ######################################################

    def clearWindow(self):
        #delete all the elements in the window
        for i in self.root.winfo_children():
            i.destroy() 
    
    ######################################################

    #Ingame functions
    def tupleToStr(self, In):
        v = []
        for i in In:
            if i not in ["(", ")", "'", ","]:
                v.append(i)
        w = ""
        for a in v: 
            w = w + a    
        return w

    def pickConsigne(self):
        if(self.testLength > 0):
            self.testLength -= 1

            while True:
                verbeInfo = self.pickRandomVerbInfo()
                if verbeInfo[0] != self.last and not verbeInfo in self.done:
                    break
                else:
                    continue
        
            self.done.append(verbeInfo)
            self.last = verbeInfo[0]
            self.c.execute("SELECT francais FROM verbes WHERE id = {}".format(verbeInfo[0]))
            self.consigne.set("Quelle est la {0} {1} du verbe '{2}'".format(personnes[verbeInfo[2]] , temps[verbeInfo[1]], self.tupleToStr(self.c.fetchone())))

            #if the verb is in the present tense, add the right termination
            if verbeInfo[1] == 0:
                self.c.execute("SELECT radical FROM verbes WHERE id = {}".format(verbeInfo[0])) 
                ans = self.tupleToStr(self.c.fetchone())

                self.c.execute("SELECT groupe FROM verbes WHERE id = {}".format(verbeInfo[0]))
                groupe = self.tupleToStr(self.c.fetchone())

                if groupe == '1':
                    self.trueAnswer.set(ans + termG1[verbeInfo[2]])          
                elif groupe == '2':
                    self.trueAnswer.set(ans + termG2[verbeInfo[2]])
                elif groupe == '3':
                    self.trueAnswer.set(ans + termG3[verbeInfo[2]])
                elif groupe == '3.5':
                    self.trueAnswer.set(ans + termG3_5[verbeInfo[2]])
                elif groupe == '4':
                    self.trueAnswer.set(ans + termG4[verbeInfo[2]])

            #if the verb is in the imperfect tense, add the right termination
            elif verbeInfo[1] == 1:
                self.c.execute("SELECT radical FROM verbes WHERE id = {}".format(verbeInfo[0])) 
                ans = self.tupleToStr(self.c.fetchone())

                self.c.execute("SELECT groupe FROM verbes WHERE id = {}".format(verbeInfo[0]))
                groupe = self.tupleToStr(self.c.fetchone())

                if groupe == '1':
                    self.trueAnswer.set(ans + "a" + termImp[verbeInfo[2]])             
                elif groupe == '2':
                    self.trueAnswer.set(ans + "e" + termImp[verbeInfo[2]])
                elif groupe == '3':
                    self.trueAnswer.set(ans + "e" + termImp[verbeInfo[2]])
                elif groupe == '3.5':
                    self.trueAnswer.set(ans + "ie" + termImp[verbeInfo[2]])
                elif groupe == '4':
                    self.trueAnswer.set(ans + "ie" + termImp[verbeInfo[2]])

            #if the verb is in the perfect tense, add the right termination
            elif verbeInfo[1] == 2:
                self.c.execute("SELECT parfait FROM verbes WHERE id = {}".format(verbeInfo[0]))
                ans = self.tupleToStr(self.c.fetchone())

                self.c.execute("SELECT groupe FROM verbes WHERE id = {}".format(verbeInfo[0]))
                groupe = self.tupleToStr(self.c.fetchone())

                self.trueAnswer.set(ans + termPerf[verbeInfo[2]])

        else:
            self.endGame()

    def pickRandomVerbInfo(self):
        #choose a randow verbe
        verbeId = randint(1, self.dicoLength)
        #depending on the difficulty, pick random tense and person
        if self.difficulty == 1:
            temps = 0
            pers = randint(0, 5)
        elif self.difficulty == 2:
            temps = randint(0, 1)
            pers = randint(0, 5)
        elif self.difficulty == 3:
            temps = randint(0, 2)
            pers = randint(0, 5)

        return [verbeId, temps, pers]

    def verifAnswer(self, event=None):
        #get the answer entered
        self.answer = self.answerEntry.get()
        #Clear the text entry
        self.answerEntry.delete(0, 'end')
        #if the answer sent is the same as th true answer, add a point and update the counter 
        if(self.answer == self.trueAnswer.get()):
            self.point+=1
            self.pointCounterLabel.set("Points: "+str(self.point))
        #pick another consigne
        self.pickConsigne()
    
    ######################################################

    #When the game ends

    def endGame(self):
        self.clearWindow()
        self.root.unbind('<Return>')

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', pady=25, padx=70, bg=self.bgcolor)
        self.space.grid(row=0, column=0)

        self.label = tk.Label(self.root, text="Fini !", font=("Courrier", 35), fg='white', bg=self.bgcolor)
        self.label.grid(row=1, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', pady=10, padx=40, bg=self.bgcolor)
        self.space.grid(row=2, column=0)

        #Display the number of question successed
        self.label = tk.Label(self.root, text=(str(self.point)+" / "+ str(self.baseLength)+" questions reussies"), font=("Courrier", 15), fg='white', bg=self.bgcolor)
        self.label.grid(row=3, column=1)

        #Display the percentage of succed
        self.label = tk.Label(self.root, text=(str((self.point/self.baseLength)*100)+r"% de reussite"), font=("Courrier", 15), fg='white', bg=self.bgcolor)
        self.label.grid(row=4, column=1)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', pady=25, padx=40, bg=self.bgcolor)
        self.space.grid(row=5, column=0)

        #Create space to make the window look good
        self.space = tk.Label(self.root, text='', padx=40, bg=self.bgcolor)
        self.space.grid(row=5, column=3)

        #Create a button to quit the app
        self.lv1 = tk.Button(self.root, text="Quit", command=self.root.destroy, font=("Courrier", 15))
        self.lv1.grid(row=6, column=0, sticky='sw', padx=5)

        #Create a button to go to the menu
        self.lv1 = tk.Button(self.root, text="Menu", command=self.initLevelChoiceScreen, font=("Courrier", 15))
        self.lv1.grid(row=6, column=2, sticky='se', padx=50)
        

if __name__ == '__main__':
    #Create the window
    root = tk.Tk()
    #Create the app
    myapp = App(root)
    #Run the app
    myapp.mainloop()