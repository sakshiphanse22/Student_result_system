from tkinter import* 
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3 

class resultClass:    
  def __init__(self,root):
    
    self.root=root #root reinitialised
    self.root.title("Students Result Management System")
    self.root.geometry("1200x480+80+170")
    self.root.config(bg="white")#for background color
    self.root.focus_force()
    
    #---title---
    title=Label(self.root,text="Add Student Results ",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=10,y=15,width=1180,height=50)
    
#--------widgets-------
   #----------variables---------
    self.var_roll=StringVar()
    self.var_name=StringVar()
    self.var_course=StringVar()
    self.var_marks=StringVar()
    self.var_full_marks=StringVar()
    self.roll_list=[]
    self.fetch_roll()
    
    lbl_select=Label(self.root,text="Select student",font=("goudy old style",15,'bold'),bg="grey",fg="white").place(x=10,y=90) #add 40 to y-axis
    
    lbl_name=Label(self.root,text="Name",font=("goudy old style",15,'bold'),bg="grey",fg="white").place(x=10,y=150)
    
    lbl_course=Label(self.root,text="Course",font=("goudy old style",15,'bold'),bg="grey",fg="white").place(x=10,y=210)
    
    lbl_marks_ob=Label(self.root,text="Marks obtained",font=("goudy old style",15,'bold'),bg="grey",fg="white").place(x=10,y=270)
    
    lbl_full_marks=Label(self.root,text="Full Marks",font=("goudy old style",15,'bold'),bg="grey",fg="white").place(x=10,y=330)
    
    self.txt_student=ttk.Combobox(self.root,textvariable=self.var_roll,values=self.roll_list,font=("goudy old style",15,'bold'),state='readonly',justify=CENTER)
    
    self.txt_student.place(x=200,y=90,width=200)
    self.txt_student.set("Select")
    
    btn_search=Button(self.root,text='Search',font=("goudy old style",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.search).place(x=420,y=90,width=120,height=28)
    
    txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20,'bold'),bg="lightBlue",state="readonly",fg="black").place(x=200,y=150,width=340)
    
    txt_course=Entry(self.root,textvariable=self.var_course,font=("goudy old style",20,'bold'),bg="lightBlue",state="readonly",fg="black").place(x=200,y=210,width=340)
    
    txt_marks=Entry(self.root,textvariable=self.var_marks,font=("goudy old style",20,'bold'),bg="lightBlue",fg="black").place(x=200,y=270,width=340)
    
    txt_full_marks=Entry(self.root,textvariable=self.var_full_marks,font=("goudy old style",20,'bold'),bg="lightBlue",fg="black").place(x=200,y=330,width=340)
    
    #--------button--------
    btn_add=Button(self.root,text="submit",font=("times new roman",15),bg="lightgreen",activebackground="lightgreen",cursor="hand2",command=self.add).place(x=300,y=420,width=120,height=35)
    
    btn_clear=Button(self.root,text="clear",font=("times new roman",15),bg="lightgray",activebackground="lightgray",cursor="hand2",command=self.clear).place(x=430,y=420,width=120,height=35)

 #----content-window for image-----
    self.bg_img=Image.open("allimages/image5.jpg")
    self.bg_img=self.bg_img.resize((500,300))
    self.bg_img=ImageTk.PhotoImage(self.bg_img)
    
    self.lbl_bg=Label(self.root,image=self.bg_img).place(x=630,y=100) #main background image
    
   #-- ------------------------------------
  def fetch_roll(self):
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    try:
      cur.execute("select roll from student")
      rows=cur.fetchall()
      if len(rows)>0:
        for row in rows:
          self.roll_list.append(row[0])
    except Exception as ex:
      messagebox.showerror("Error",f"Error due to {str(ex)}") 
      
  def search(self):
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    try:
        cur.execute("select name,course from student where roll=?",(self.var_roll.get(),))
        row=cur.fetchone()
        if row!=None:
          self.var_name.set(row[0])
          self.var_course.set(row[1])
          
        else:
          messagebox.showerror("Error","No record found",parent=self.root)
          
    except Exception as ex:
      messagebox.showerror("Error",f"Error due to {str(ex)}") 
      
  def add(self):
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    try:
      if self.var_name.get()=="":
        messagebox.showerror("Error","Please first search student record",parent=self.root)
      else:
        cur.execute("select * from result where roll=? and course=?" ,(self.var_roll.get(),self.var_course.get()))
        row=cur.fetchone()
        if row!=None:
          messagebox.showerror("Error","Result already present",parent=self.root)
        else:
          per=(int(self.var_marks.get())*100)/int(self.var_full_marks.get())
          cur.execute("insert into result (roll,name,course,marks_ob,full_marks,per)values(?,?,?,?,?,?)",(
            self.var_roll.get(),
            self.var_name.get(),
            self.var_course.get(),
            self.var_marks.get(),
            self.var_full_marks.get(),
            str(per)
          ))
          con.commit()
          messagebox.showinfo("success","Result Added successfully",parent=self.root)
          self.show()
        
    except Exception as ex:
      messagebox.showerror("Error",f"Error due to {str(ex)}") 
      
  def clear(self):
    self.var_roll.set("Select"),
    self.var_name.set(""),
    self.var_course.set(""),
    self.var_marks.set(""),
    self.var_full_marks.set("")
  
if __name__=="__main__":   
  root=Tk()#tkinter class ka object
  obj=resultClass(root)
  root.mainloop()