from tkinter import *
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3
from tkinter import ttk
from googletrans import Translator, LANGUAGES

# Initialize text-to-speech engine
eng = pyttsx3.init()
voice = eng.getProperty('voices')
eng.setProperty('voice', voice[0].id)

def search():
    try:
        data = json.load(open('data.json'))
        word = entrybox.get().lower()  # Ensure case-insensitivity
        selected_language = comb_sor.get()

        if word in data:
            meaning = data[word]
            trans = Translator()
            textarea.delete(1.0, END)
            for item in meaning:
                translated_text = trans.translate(item, dest=selected_language).text
                textarea.insert(END, u'\u2022' + translated_text + '\n\n')
        elif len(get_close_matches(word, data.keys())) > 0:
            close_match = get_close_matches(word, data.keys())[0]
            res = messagebox.askyesno("Confirm", f'Did you mean {close_match} instead?')
            if res:
                entrybox.delete(0, END)
                entrybox.insert(END, close_match)
                meaning = data[close_match]
                textarea.delete(1.0, END)
                for item in meaning:
                    translated_text = trans.translate(item, dest=selected_language).text
                    textarea.insert(END, u'\u2022' + translated_text + '\n\n')
            else:
                messagebox.showerror('Error', "The word doesn't exist, please double-check it.")
                entrybox.delete(0, END)
                textarea.delete(1.0, END)
        else:
            messagebox.showerror('Error', "The word doesn't exist, please double-check it.")
            entrybox.delete(0, END)
            textarea.delete(1.0, END)
    except Exception as e:
        messagebox.showerror('Error', f"An error occurred: {e}")

def clear():
    entrybox.delete(0, END)
    textarea.delete(1.0, END)

def iexit():
    res = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if res:
        root.destroy()

def wordaudio():
    eng.say(entrybox.get())
    eng.runAndWait()

def meaningaudio():
    eng.say(textarea.get(1.0, END))
    eng.runAndWait()

root = Tk()
root.geometry('1000x600+100+25')
root.title('TALKING DICTIONARY')
root.resizable(0, 0)

bgimage = PhotoImage(file="bg.png")
bglabel = Label(root, image=bgimage)
bglabel.place(x=0, y=0)

label1 = Label(root, text="Enter word:", font=('Aptos', 25, 'bold'), fg='green', bg='white')
label1.place(x=450, y=20)

entrybox = Entry(root, font=('Aptos', '20', 'bold'), justify='center')
entrybox.place(x=460, y=80)

searchimage = PhotoImage(file='search.png')
searchbutton = Button(root, image=searchimage, bd=0, bg='whitesmoke', cursor='hand2', activebackground='whitesmoke', command=search)
searchbutton.place(x=470, y=124)

micimage = PhotoImage(file="mic.png")
micbutton = Button(root, image=micimage, bd=0, bg='whitesmoke', cursor='hand2', activebackground='whitesmoke', command=wordaudio)
micbutton.place(x=600, y=124)

meaninglabel = Label(root, text="Meaning:", font=('Aptos', 20, 'bold'), fg='green', bg='white')
meaninglabel.place(x=450, y=190)

textarea = Text(root, width=34, height=8, font=('arial', 18, 'bold'), bd=8, relief=GROOVE)
textarea.place(x=460, y=240)

audioimage = PhotoImage(file='microphone.png')
audioButton = Button(root, image=audioimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2', command=meaningaudio)
audioButton.place(x=530, y=500)

list_text = list(LANGUAGES.values())
comb_sor = ttk.Combobox(root, value=list_text)
comb_sor.place(x=300, y=300, height=40, width=100)
comb_sor.set("english")

clearimage = PhotoImage(file='clear.png')
clearButton = Button(root, image=clearimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2', command=clear)
clearButton.place(x=660, y=500)

exitimage = PhotoImage(file='exit.png')
exitButton = Button(root, image=exitimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2', command=iexit)
exitButton.place(x=790, y=500)

def enter_function(event):
    searchbutton.invoke()

root.bind('<Return>', enter_function)
root.mainloop()
