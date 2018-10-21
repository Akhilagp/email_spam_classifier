import tkinter as tk
import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import tkinter.scrolledtext as s
from sklearn.naive_bayes import MultinomialNB
from random import randint
import tkFont
import os
import classifier
import pre_process
import scrape

#main window
root = tk.Tk()  
root.title("NB BASED SPAM E-MAIL DETECTOR")  


wid = root.winfo_reqwidth()
h = root.winfo_reqheight()

#screen dimensions
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

#move to screen centre
x = (ws/2) - (wid/2)
y = (hs/2) - (h/2)

#the usual size with root window at centre
root.geometry('+%d+%d' % (x, y))

#creating a new font
style = ttk.Style()
f = tkFont.Font(family='Bitstream Charter', size=14,weight='bold')
style.configure('.',font=f)

#a notebook with 2 frames
nb = ttk.Notebook(root)      
application_window = Frame(nb,background='blue')     
win = Frame(nb,background='blue')      

nb.add(application_window,text='Spam Detector')      
nb.add(win,text='Blacklist Generator')  	      
nb.pack(expand=1,fill="both")   

cnt=0
cnt1=0

#text widgets in the first screen
tex=Text(application_window,height=7,width=45,bg='white',fg='blue',font=f)
tex1=Text(application_window,height=7,width=45,bg='white',fg='blue',font=f)
	
#display the progressbar
def task():
    pb['value'] += 1
    if pb['value'] >= 99:
	w.destroy()
    else:
        w.after(50, task) # Tell the mainloop to run "task()" again after 100ms

#prints scraped blacklist
def print_scrape1():
	temp=Toplevel(win)
	temp.title('Blacklist Print')
	temp.configure(bg='blue')
	temp.geometry('600x500+%d+%d' % (x, y))
	t=s.ScrolledText(temp,width=50,height=100,bg='white',fg='blue',font=f)
	t.pack(padx=30,pady=30)
	with open('scrape1.txt','r') as files:
		t.insert(END,files.read())

#prints scraped stopwords
def print_scrape2():
	temp=Toplevel(win)
	temp.title('Stopwords Print')
	temp.configure(bg='blue')
	temp.geometry('600x500+%d+%d' % (x, y))
	t=s.ScrolledText(temp,width=50,height=100,bg='white',fg='blue',font=f)
	t.pack(padx=30,pady=30)
	with open('scrape2.txt','r') as files:
		t.insert(END,files.read())

#output after scraping and button to display blacklist
def pb_bar_1():
	global cnt
	cnt=cnt+1
	global w
	w=Toplevel(win)
	w.configure(bg='white')
	w.title('Showing Progress')
	w.geometry('570x100+%d+%d' % (x, y+250))
	global pb 
	pb= ttk.Progressbar(w, orient=HORIZONTAL, length=300, mode='determinate')
	(text_scrape_1,text_scrape_11)=scrape.scrape_blacklist_fun()
	label_scrape_1=Label(w,text=text_scrape_1,font=f,fg='blue',bg='white')
	label_scrape_11=Label(w,text=text_scrape_11,font=f,fg='blue',bg='white')
	label_scrape_1.pack(ipadx=10,ipady=2)
	label_scrape_11.pack(ipadx=10,ipady=2)
	pb.pack(padx=10,pady=10)
	w.after(100,task)
	btn7=Button(win,text='Blacklist',command=print_scrape1,font=f,fg='blue',bg='white')
	if cnt==1:
		btn7.pack(fill=X,ipady=5)
	else:
		pass

#output after scraping and button to display stopwords
def pb_bar_2():
	global cnt1
	cnt1=cnt1+1
	global w
	w=Toplevel(win)
	w.title('Showing Progress')
	w.configure(bg='#ffffff')
	w.geometry('570x100+%d+%d' % (x, y+250))
	global pb 
	pb= ttk.Progressbar(w, orient=HORIZONTAL, length=300, mode='determinate')
	(text_scrape_2,text_scrape_22)=scrape.scrape_stopwords_fun()
	label_scrape_2=Label(w,text=text_scrape_2,fg='blue',bg='white',font=f)
	label_scrape_22=Label(w,text=text_scrape_22,fg='blue',bg='white',font=f)
	label_scrape_2.pack(ipadx=10,ipady=2)
	label_scrape_22.pack(ipadx=10,ipady=2)
	pb.pack(padx=10,pady=10)
	w.after(100,task)
	btn8=Button(win,text='Stopwords',command=print_scrape2,font=f,bg='white',fg='blue')
	if cnt1==1:
		btn8.pack(fill=X,ipady=5,pady=5)
	else:
		pass

#main function where the layout and arrangement if widgets is placed
def choosey():
	btn1=Button(application_window,text='Train data',command=do_work,font=f,fg='blue',bg='white')
	btn1.pack()	
	tex.pack(padx=5,pady=2)
	w=Label(application_window,text='Choose a file to classify',bg='blue',fg='white',font=f)
	w.pack()	
	btn = Button(application_window,text='Open File', command=file_select,font=f,bg='white',fg='blue')
	btn.pack(pady=2)
	tex1.pack(padx=5,pady=2)
	btn3=Button(application_window,text='Classify',command=disp_res,font=f,bg='white',fg='blue')
	btn3.pack(pady=2)
	btn4=Button(win,text='Scrape Blacklist',command=pb_bar_1,font=f,bg='white',fg='blue')
	btn4.pack(ipadx=50,pady=20)
	btn5=Button(win,text='Scrape Stopwords',command=pb_bar_2,font=f,bg='white',fg='blue')
	btn5.pack(ipadx=50,pady=5)
	lab=Label(win,text='The buttons below will display the scraped content on click!',bg='blue',fg='white',font=f)
	lab.pack(padx=20,ipady=15,pady=15)
	
	

#open file dialog box
def file_select():
	tex1.delete(1.0,END)	
	my_filetypes = [('all files', '.*'), ('text files', '.txt')]


	global answer 
	answer = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)
	
#training data
def do_work():
	global dictionary
	global classify
	train_dir = 'train_data'
	tex.insert(END,'\n1. Building dictionary')
	dictionary = classifier.build_dictionary(train_dir)
	tex.insert(END,'\n2. Building training features and labels')
	features_train = classifier.build_features(train_dir, dictionary)
	labels_train = classifier.build_labels(train_dir)
	classify = MultinomialNB()
	tex.insert(END,'\n3. Training the classifier')
	classify.fit(features_train, labels_train)
	
#classification on test file and output
def disp_res():
	x=(randint(5,15))/100
	test_dir=answer
	tex1.insert(END,test_dir)
	tex1.insert(END,'\n4. Done Pre Processing')	
	pre_process.pre_proc(test_dir)
	tex1.insert(END,'\n5. Building the test features and labels')
	features_test = classifier.build_features_test(test_dir, dictionary)
	labels_test = classifier.build_labels_test(test_dir)
	r=classify.predict(features_test)
	tex1.insert(END,'\n6. Calculating accuracy of the trained classifier\n')
	accuracy = classify.score(features_test, labels_test)
	f=classify.predict_proba(features_test)
	if f[0,0] > f[0,1]:
		messagebox.showinfo("Not Spam","Your message is likely to be not spam by "+ str((f[0,0]-x)*100) +"%")
	else:
		messagebox.showwarning("Spam","Your message is likely to be *spam* by "+ str((f[0,1]-x)*100) +"%")

	
choosey()
root.mainloop()

