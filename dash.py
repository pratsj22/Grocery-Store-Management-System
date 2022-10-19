from tkinter import *
from PIL import Image,ImageTk
from billing import BillClass
from prod import productClass

class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Grocery Management")
        #===title area=====
        # self.icon_title=PhotoImage (file="images/logo1.png")
        title=Label(self.root, text="Urban Grocer", font=("times new roman",40,"bold"), bg='#010c48', fg='white').place(x=0, y=0, relwidth=1, height=70)

        self.lbl_clock=Label(self.root, text="",font=("times new roman",17),bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=50)

        #-------Left Menu & Grocery Logo----------
        LeftMenu=Frame (self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0,y=102,width=1400,height=600)

        self.MenuLogo=Image.open("images/storepic.jpg")
        self.MenuLogo=self.MenuLogo.resize((1400,350), Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        lbl_menuLogo=Label (LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        #----Menu Label------
        lbl_menu = Label(LeftMenu, text="Menu",font=("times new roman", 20),bg="#009688").pack(side=TOP, fill=X)

        btn_prod = Button(LeftMenu,text="Product", command=self.product,font=("times new roman",20, "bold"),bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_bill = Button(LeftMenu,text="Bill",command=self.billing,font=("times new roman",20, "bold"),bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu,text="Exit", command=self.exit,font=("times new roman",20, "bold"),bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

    #------methods for menu------
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    
    def billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=BillClass(self.new_win)

    def exit(self):
        self.root.destroy()

if __name__ =="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()