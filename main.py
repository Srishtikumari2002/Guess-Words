from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import webbrowser
import random
import os
import time

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# main app class
class rootApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry("1200x700")
        self.title("Guess Words")
        self.iconbitmap("images/logo.ico")
        self.resizable(width=False, height=False)

        #we will place multiple frames in a container
        #and show the one we want
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in (HomePage, InfoPage, GamePage):
            page_name = i.__name__
            frame = i(parent=container, controller=self)
            self.frames[page_name] = frame

            #put all of the pages in the same location
            #the one on the top of the stacking order
            #will be the one that is visible

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
#____________________________________________________________________________________________________________________________________________________________________
# autoscroll class
class AutoScroll(Scrollbar):

    # defining set method with all
    # its parameter
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:

            #using grid_remove
            self.tk.call("place", "forget", self)
        
        else:
            self.place(x=382, y=50, height=610)
        Scrollbar.set(self, low, high)
#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# some counters 
pn = 0
scr = 0
hang = 0
win_count = 0
bulbs = 0
selected_word = ""
selected_hint = ""
guessed = []

if os.path.isfile("prev_details.txt") == True:
    with open("prev_details.txt","r") as  f:
        gems = int(f.read())
else:
    gems = 30

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# home page class
class HomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "green")

        def info():
            messagebox.showinfo("About","Welcome Player,\nYou are going to play a word guessing game.\nIn this game you will be given meaning\n of a word and you have to guess the correct word.\nYou get coins on guessing the correct word and\ncan use those coins to get a hint if you stuck\n somewhere.\n\t\tGood Luck")

        title = Button(self, bd=0, text="GUESS WORDS", font=("helvetica", 100, "bold"), fg="white", bg="green", activebackground="green", activeforeground="black", command=info)
        title.pack(fill="both")

        play = Button(self, bd=0, text="PLAY", font=("helvetica", 50 ), activebackground="green", activeforeground="black", bg="green", fg="white", command=lambda: controller.show_frame("GamePage"))
        play.pack()

        Info = Button(self, bd=0, text="INFO", font=("helvetica", 50), activebackground="green", activeforeground="black", bg="green", fg="white", command=lambda: controller.show_frame("InfoPage"))
        Info.pack()
#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#info page class
class InfoPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "blue")

        exit_btn_img = ImageTk.PhotoImage(Image.open("images//exit.png"))
        exit_btn = Button(self, bd=0, bg="blue", activebackground="blue", image=exit_btn_img, command=lambda: controller.show_frame("HomePage"))
        exit_btn.image = exit_btn_img
        exit_btn.place(x=1072,y=10)

        title = Label(self, text="Rules and Information", bg="blue", fg="yellow", font=("Algerian", 60, "italic"))
        title.pack()

        rules = """This is a word guessing game. In this game your are given meaning of a word and you have to guess that word correctly.You earn coins for correct answers depending on how much time you took to complete the level.You can use those coins to skip a level or can get hint for those coins. If you guess a wrong word you lose one move out of six and hangman gets created on the screen. You can use only three hints per question. This game is developed by Srishti Kumari.\nSome part of the code was derived from:"""
        info1 = ImageTk.PhotoImage(Image.open("images/info1.png").resize((1000,580)))
        info2 = ImageTk.PhotoImage(Image.open("images/info2.png").resize((1000,580)))
        info3 = ImageTk.PhotoImage(Image.open("images/info3.png").resize((1000,580)))

        def open(link):
            webbrowser.open(link)
        color = "green"
        lbl = Label(self, bg="blue", fg="white", font=("helvetica", 22))
        rule = Text(self, bg="blue", bd=0, fg="white", font=("helvetica", 22), wrap=WORD, width=63, height=15, cursor="arrow")
        rule.insert(END, rules)
        rule.tag_configure("link", foreground="red", underline=True)
        rule.tag_bind("link", "<Button-1>", lambda event, color= color:open("http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter"))
        rule.tag_configure("link2", foreground="red", underline=True)
        rule.tag_bind("link2", "<Button-1>", lambda event, color= color:open("https://github.com/pythontutorials/HANGMAN-GAME"))
        rule.insert(END, "http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter","link")
        rule.insert(END, " and ")
        rule.insert(END, "https://github.com/pythontutorials/HANGMAN-GAME","link2")
        rule.insert(END, "\t"*11+"Enjoy Playing!")
        rule.config(state=DISABLED) 
        rule.place(x=90, y=230)


        def next():
            global pn
            if pn == 0:
                prev_btn.place(x=10, y=630)
                rule.place_forget()
                lbl.config(image=info1)
                lbl.image = info1
                lbl.place(x=90, y=100)
                pn += 1
            elif pn == 1:
                lbl.config(image=info2)
                lbl.image = info2
                pn += 1
            elif pn == 2:
                next_btn.place_forget()
                lbl.config(image=info3)
                lbl.image = info3
                pn += 1
        def prev():
            global pn
            if pn == 1:
                prev_btn.place_forget()
                rule.place(x=90, y=230)
                lbl.place_forget()
                pn -= 1
            elif pn == 2:
                lbl.config(image=info1)
                lbl.image = info1
                pn -= 1
            elif pn == 3:
                next_btn.place(x=1126,y=630)
                lbl.config(image=info2)
                lbl.image = info2
                pn -= 1

        next_btn_img = ImageTk.PhotoImage(Image.open("images/next.png").resize((50,50)))
        next_btn = Button(self, bd=0, bg="blue", activebackground="blue", image=next_btn_img, command=next)
        next_btn.image = next_btn_img
        next_btn.place(x=1126, y=630)

        prev_btn_img = ImageTk.PhotoImage(Image.open("images/next.png").resize((50,50)).rotate(180, expand=1))
        prev_btn = Button(self, bd=0, bg="blue", activebackground="blue", image=prev_btn_img, command=prev)
        prev_btn.image = prev_btn_img

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#game page class
class GamePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "#E7FFFF")

        start_time = time.time()
        c = [start_time]
        exit_btn_img = ImageTk.PhotoImage(Image.open("images/exit.png"))
        exit_btn = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=exit_btn_img, command=lambda: controller.show_frame("HomePage"))
        exit_btn.image = exit_btn_img
        exit_btn.place(x=1072,y=10)

        scores = StringVar()
        scores.set("SCORE:"+str(scr))
        score = Label(self, textvariable=scores, bd=0, bg="#E7FFFF", fg="black", font=("helvetica", 25))
        score.place(x=8,y=4)

        def coin_info():
            messagebox.showinfo("HOW TO USE COINS?", "You earn coins when you give correct answers.\nThese coins can be used to get hint if you stuck somewhere.\n\nFirst Hint - 5 coins\nSecond Hint - 10 coins\nThird Hint - 15 coins\nSkip word - 30coins\n\nAlso you can use only three hints per question.")

        coins_btn_img = ImageTk.PhotoImage(Image.open("images/gem.png").resize((48,40)))
        coins_btn = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=coins_btn_img, command=coin_info)
        coins_btn.image = coins_btn_img
        coins_btn.place(x=8,y=40)

        gold = StringVar()
        gold.set(":"+str(gems))
        coins = Label(self, bd=0, bg="#E7FFFF", textvariable=gold, fg="black", font=("helvetica", 25))
        coins.place(x=60,y=40)

        # choosing the word and meaning
        def choose():
            global selected_hint,selected_word
            word_bank = open('images/words.txt','r').readlines()
            size = len(word_bank)-1
            index = random.randint(0,size)
            selected_word = word_bank[index].strip('\n')
            hint_bank = open('images/hints.txt','r').readlines()
            selected_hint = hint_bank[index].strip('\n')

        choose()

        #creation of word dashes variables
        cr_word = list("_"*len(selected_word))
        x = ""
        un_word = StringVar()
        for i in cr_word:
            x += i
        un_word.set(" ".join(str(x)))
        dashes = Label(self, bd=0, textvariable=un_word, font=("Helvetica",40), bg="#E7FFFF", fg="black", cursor="arrow", width=28, height=1)
        dashes.place(x=180, y=450)

        def next_game(): # next game function
            global win_count,hang,selected_word,selected_hint,bulbs,guessed
            hangmans[hang].place_forget()
            win_count,hang,bulbs = 0,0,0
            choose()
            for i in alphabets:
                i[0].place(x=i[2],y=i[-1])
            hangmans[hang].place(x=300,y=-50)
            clue.config(state=NORMAL)
            clue.delete("0.0", END)
            clue.insert(END, "HINT: "+selected_hint.capitalize())
            clue.config(state=DISABLED)
            cr_word.clear()
            guessed.clear()
            for k in range(len(selected_word)):
                cr_word.append("_")
            x = ""
            for i in cr_word:
                x += i
            un_word.set(" ".join(str(x)))
            c[0] = time.time()
            with open("prev_details.txt", "w") as f:
                f.write(str(gems))

        def check(letter, btn): # button click check function
            global hang,scr, win_count,selected_word,gems,guessed
            btn.place_forget()
            myword = selected_word.lower()
            if letter in myword:
                for i in range(0,len(myword)):
                    if myword[i]== letter:
                        guessed.append(letter)
                        win_count += 1
                        cr_word[i]=letter.upper()
                        x = ""
                        for i in cr_word:
                            x += i
                        un_word.set(" ".join(str(x)))

                with open("prev_details.txt", "w") as f:
                        f.write(str(gems))

                if win_count == len(myword):
                    end_time = time.time()
                    scr += 1
                    time_taken = end_time-c[0]
                    if time_taken < 4.0:
                        gems += 10
                    elif 4.0 <= time_taken <8.0:
                        gems += 5
                    elif 8.0 <= time_taken < 12.0:
                        gems += 2
                    else:
                        gems += 1
                    gold.set(":"+str(gems))

                    with open("prev_details.txt", "w") as f:
                        f.write(str(gems))
                    answer = messagebox.askyesno('GAME OVER','YOU WON!\nTHE WORD WAS "{}."\nDO YOU WANT TO PLAY AGAIN?'.format(selected_word.upper()))
                    if answer == True:
                        scores.set("SCORE:"+str(scr))
                        next_game()
                    else:
                        controller.show_frame("HomePage") 
                        next_game()
                    
            else:
                hangmans[hang].place_forget()
                hang += 1
                hangmans[hang].place(x=300,y=-50)
                with open("prev_details.txt", "w") as f:
                        f.write(str(gems))
                if hang == 6:
                    with open("prev_details.txt", "w") as f:
                        f.write(str(gems))
                    answer = messagebox.askyesno('GAME OVER','YOU LOST!\nTHE WORD WAS "{}."\nDO YOU WANT TO PLAY AGAIN?'.format(selected_word.upper()))
                    if answer == True:
                        next_game()
                    else:
                        controller.show_frame("HomePage")
                        next_game()

        def get_hint():
            global bulbs,guessed,selected_word,gems
            if bulbs <3:
                bulb_word = set(selected_word)
                guessed_word = set(guessed)
                if bulbs == 0:
                    if gems >=5:
                        ans = random.choice(list(bulb_word-guessed_word))
                        for z in alphabets:
                            if z[1] == ans:
                                butn = z[0]
                        
                        answer = messagebox.askyesno("GET HINT", "DO YOU WANT TO USE COINS TO GET HINT?")
                        if answer == True:
                            check(ans, butn)
                            bulbs +=1
                            gems -= 5
                            with open("prev_details.txt", "w") as f:
                                f.write(str(gems))
                            gold.set(":"+str(gems))
                    else:
                        messagebox.showwarning("NO COINS", "YOU DON'T HAVE ENOUGH COINS.\n GAIN SOME BY GIVING CORRECT ANSWERS.")
                elif bulbs == 1:
                    if gems >=10:
                        ans = random.choice(list(bulb_word-guessed_word))
                        for z in alphabets:
                            if z[1] == ans:
                                butn = z[0]
                        answer = messagebox.askyesno("GET HINT", "DO YOU WANT TO USE COINS TO GET HINT?")
                        if answer == True:
                            check(ans, butn)
                            bulbs +=1
                            gems -= 10
                            with open("prev_details.txt", "w") as f:
                                f.write(str(gems))
                            gold.set(":"+str(gems))
                    else:
                        messagebox.showwarning("NO COINS", "YOU DON'T HAVE ENOUGH COINS.\n GAIN SOME BY GIVING CORRECT ANSWERS.")
                elif bulbs == 2:
                    if gems >=15:
                        ans = random.choice(list(bulb_word-guessed_word))
                        for z in alphabets:
                            if z[1] == ans:
                                butn = z[0]
                        answer = messagebox.askyesno("GET HINT", "DO YOU WANT TO USE COINS TO GET HINT?")
                        if answer == True:
                            check(ans, butn)
                            bulbs +=1
                            gems -= 15
                            with open("prev_details.txt", "w") as f:
                                f.write(str(gems))
                            gold.set(":"+str(gems))
                    else:
                        messagebox.showwarning("NO COINS", "YOU DON'T HAVE ENOUGH COINS.\n GAIN SOME BY GIVING CORRECT ANSWERS.")
            else:
                messagebox.showerror("MAX HINT", "YOU CAN ONLY USE UPTO THREE HINTS PER LEVEL?")

        h1 = ImageTk.PhotoImage(Image.open("images/h1.png"))
        h2 = ImageTk.PhotoImage(Image.open("images/h2.png"))
        h3 = ImageTk.PhotoImage(Image.open("images/h3.png"))
        h4 = ImageTk.PhotoImage(Image.open("images/h4.png"))
        h5 = ImageTk.PhotoImage(Image.open("images/h5.png"))
        h6 = ImageTk.PhotoImage(Image.open("images/h6.png"))
        h7 = ImageTk.PhotoImage(Image.open("images/h7.png"))

        c1 = Label(self, bd=0, bg="#E7FFFF", image=h1)
        c1.image = h1
        c2 = Label(self, bd=0, bg="#E7FFFF", image=h2)
        c2.image = h2
        c3 = Label(self, bd=0, bg="#E7FFFF", image=h3)
        c3.image = h3
        c4 = Label(self, bd=0, bg="#E7FFFF", image=h4)
        c4.image = h4
        c5 = Label(self, bd=0, bg="#E7FFFF", image=h5)
        c5.image = h5
        c6 = Label(self, bd=0, bg="#E7FFFF", image=h6)
        c6.image = h6
        c7 = Label(self, bd=0, bg="#E7FFFF", image=h7)
        c7.image = h7

        b1_img = ImageTk.PhotoImage(Image.open("images/a.png"))
        b2_img = ImageTk.PhotoImage(Image.open("images/b.png"))
        b3_img = ImageTk.PhotoImage(Image.open("images/c.png"))
        b4_img = ImageTk.PhotoImage(Image.open("images/d.png"))
        b5_img = ImageTk.PhotoImage(Image.open("images/e.png"))
        b6_img = ImageTk.PhotoImage(Image.open("images/f.png"))
        b7_img = ImageTk.PhotoImage(Image.open("images/g.png"))
        b8_img = ImageTk.PhotoImage(Image.open("images/h.png"))
        b9_img = ImageTk.PhotoImage(Image.open("images/i.png"))
        b10_img = ImageTk.PhotoImage(Image.open("images/j.png"))
        b11_img = ImageTk.PhotoImage(Image.open("images/k.png"))
        b12_img = ImageTk.PhotoImage(Image.open("images/l.png"))
        b13_img = ImageTk.PhotoImage(Image.open("images/m.png"))
        b14_img = ImageTk.PhotoImage(Image.open("images/n.png"))
        b15_img = ImageTk.PhotoImage(Image.open("images/o.png"))
        b16_img = ImageTk.PhotoImage(Image.open("images/p.png"))
        b17_img = ImageTk.PhotoImage(Image.open("images/q.png"))
        b18_img = ImageTk.PhotoImage(Image.open("images/r.png"))
        b19_img = ImageTk.PhotoImage(Image.open("images/s.png"))
        b20_img = ImageTk.PhotoImage(Image.open("images/t.png"))
        b21_img = ImageTk.PhotoImage(Image.open("images/u.png"))
        b22_img = ImageTk.PhotoImage(Image.open("images/v.png"))
        b23_img = ImageTk.PhotoImage(Image.open("images/w.png"))
        b24_img = ImageTk.PhotoImage(Image.open("images/x.png"))
        b25_img = ImageTk.PhotoImage(Image.open("images/y.png"))
        b26_img = ImageTk.PhotoImage(Image.open("images/z.png"))

        b1 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b1_img, font=10, command=lambda:check("a",b1))
        b1.image = b1_img
        b2 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b2_img, font=10, command=lambda:check("b",b2))
        b2.image = b2_img
        b3 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b3_img, font=10, command=lambda:check("c",b3))
        b3.image = b3_img
        b4 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b4_img, font=10, command=lambda:check("d",b4))
        b4.image = b4_img
        b5 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b5_img, font=10, command=lambda:check("e",b5))
        b5.image = b5_img
        b6 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b6_img, font=10, command=lambda:check("f",b6))
        b6.image = b6_img
        b7 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b7_img, font=10, command=lambda:check("g",b7))
        b7.image = b7_img
        b8 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b8_img, font=10, command=lambda:check("h",b8))
        b8.image = b8_img
        b9 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b9_img, font=10, command=lambda:check("i",b9))
        b9.image = b9_img
        b10 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b10_img, font=10, command=lambda:check("j",b10))
        b10.image = b10_img
        b11 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b11_img, font=10, command=lambda:check("k",b11))
        b11.image = b11_img
        b12 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b12_img, font=10, command=lambda:check("l",b12))
        b12.image = b12_img
        b13 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b13_img, font=10, command=lambda:check("m",b13))
        b13.image = b13_img
        b14 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b14_img, font=10, command=lambda:check("n",b14))
        b14.image = b14_img
        b15 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b15_img, font=10, command=lambda:check("o",b15))
        b15.image = b15_img
        b16 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b16_img, font=10, command=lambda:check("p",b16)) 
        b16.image = b16_img
        b17 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b17_img, font=10, command=lambda:check("q",b17))
        b17.image = b17_img
        b18 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b18_img, font=10, command=lambda:check("r",b18))
        b18.image = b18_img
        b19 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b19_img, font=10, command=lambda:check("s",b19))
        b19.image = b19_img
        b20 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b20_img, font=10, command=lambda:check("t",b20))
        b20.image = b20_img
        b21 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b21_img, font=10, command=lambda:check("u",b21))
        b21.image = b21_img
        b22 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b22_img, font=10, command=lambda:check("v",b22))
        b22.image = b22_img
        b23 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b23_img, font=10, command=lambda:check("w",b23))
        b23.image = b23_img
        b24 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b24_img, font=10, command=lambda:check("x",b24))
        b24.image = b24_img
        b25 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b25_img, font=10, command=lambda:check("y",b25))
        b25.image = b25_img
        b26 = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=b26_img, font=10, command=lambda:check("z",b26))
        b26.image = b26_img

        alphabets = [[b1,'a',0,595],[b2,'b',70,595],[b3,'c',140,595],[b4,'d',210,595],[b5,'e',280,595],[b6,'f',350,595],[b7,'g',420,595],[b8,'h',490,595],[b9,'i',560,595],[b10,'j',630,595],[b11,'k',700,595],[b12,'l',770,595],[b13,'m',840,595],[b14,'n',910,595],[b15,'o',980,595],[b16,'p',1050,595],[b17,'q',1120,595],[b18,'r',280,645],[b19,'s',350,645],[b20,'t',420,645],[b21,'u',490,645],[b22,'v',560,645],[b23,'w',630,645],[b24,'x',700,645],[b25,'y',770,645],[b26,'z',840,645]]
        hangmans = [c1,c2,c3,c4,c5,c6,c7]

        for i in alphabets:
            i[0].place(x=i[2],y=i[-1])
        hangmans[hang].place(x=300,y=-50)

        clue = Text(self, font=("Helvetica", 20), bd=0, bg="#E7FFFF", fg="black", width=25, height=10)
        clue.insert(END, "HINT: "+selected_hint.capitalize())
        clue.config(state=DISABLED, cursor="arrow", selectbackground="#E7FFFF", wrap=WORD, selectforeground="black")
        clue.place(x=720, y=70)

        def skip(): # skip the level function
            global gems
            with open("prev_details.txt", "w") as f:
                        f.write(str(gems))
            if gems >= 30:
                answer = messagebox.askyesno("SKIP LEVEL", "DO YOU WANT TO USE COINS TO SKIP THIS LEVEL?")
                if answer == True:
                    gems -= 30
                    with open("prev_details.txt", "w") as f:
                        f.write(str(gems))
                    gold.set(":"+str(gems))
                    next_game()
            else:
                messagebox.showwarning("NO COINS", "YOU DON'T HAVE ENOUGH COINS.\n GAIN SOME BY GIVING CORRECT ANSWERS.")
        
        skip_img = ImageTk.PhotoImage(Image.open("images/next.png").resize((50,50)))
        skip_btn = Button(self, bd=0, bg="#E7FFFF", image=skip_img, activebackground="#E7FFFF", command=skip)
        skip_btn.image = skip_img
        skip_btn.place(x=1130, y=480)

        hint_btn_img = ImageTk.PhotoImage(Image.open("images/hint.png").resize((40,40)))
        hint_btn = Button(self, bd=0, bg="#E7FFFF", activebackground="#E7FFFF", image=hint_btn_img, command=get_hint)
        hint_btn.image = hint_btn_img
        hint_btn.place(x=1025, y=15)
#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# let's run the app
if __name__ == "__main__":
    app = rootApp()
    app.mainloop() 