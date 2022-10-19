import os
import tempfile
from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from sql_connection import get_sql_connection
import time

class BillClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Grocery Management")
        self.cart_list=[]
        self.chk_print=0
        #===title area=====
        # self.icon_title=PhotoImage (file="images/logo1.png")
        title=Label(self.root, text="Urban Grocer", font=("times new roman",40,"bold"), bg='#010c48', fg='white').place(x=0, y=0, relwidth=1, height=70)

        self.lbl_clock=Label(self.root, text="",font=("times new roman",15),bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #=======Product Frame=============
        ProductFrame1=Frame(self.root,bd=4, relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410, height=580)
        PTitle=Label(ProductFrame1, text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        #====Product Search Frame======
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1, bd=2,relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)
        lbl_search=Label(ProductFrame2, text="Search Product | By Name ",font=("times new roman", 15, "bold"),bg="white", fg="green").place(x=2, y=5)
        lbl_name=Label(ProductFrame2, text="Product Name",font=("times new roman",15,"bold"), bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2, textvariable=self.var_search,font=("times roman", 15), bg="lightyellow").place(x=128,y=48, width=150, height=22)
        btn_search=Button(ProductFrame2, text="Search",command=self.search, font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all=Button(ProductFrame2, text="Show All",command=self.show, font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285, y=10, width=100, height=25)

        #----TreeView-------
        ProductFrame3=Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=400)
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.xview)

        #----Adding Headings to TreeView-------
        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"] = "headings"
        
        self.product_Table.pack(fill=BOTH, expand=1)
        
        self.product_Table.column("pid", width=50)
        self.product_Table.column("name", width=120)
        self.product_Table.column("price", width=150)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)

        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note=Label(ProductFrame1, text="Note: 'Enter 0 Qunatity to remove product from the Cart'",font=("goudy old style",12), bg="white",fg="red").pack(side=BOTTOM, fill=X)

        #=====CustomerFrame==
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110,width=530, height=70)
        cTitle=Label(CustomerFrame, text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP, fill=X)
        lb1_name=Label(CustomerFrame, text="Name", font=("times new roman",15), bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman",13),bg="lightyellow").place(x=80, y=35, width=160)
        lb1_contact=Label(CustomerFrame, text="Contact No.", font=("times new roman",15), bg="white").place(x=260,y=35)
        txt_contact=Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman",13),bg="lightyellow").place(x=360, y=35, width=160)

        Cal_Cart_Frame=Frame(self.root,bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=190,width=530, height=360)

        cart_Frame=Frame(Cal_Cart_Frame, bd=5, relief=RIDGE)
        cart_Frame.place(x=5,y=10,width=510, height=342)
        self.cartTitle=Label(cart_Frame, text="Cart \t\t\t Total Product: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)
        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.xview)

        #----Adding Headings to TreeView-------
        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable["show"] = "headings"
        
        self.CartTable.pack(fill=BOTH, expand=1)
        
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=150)
        self.CartTable.column("price", width=100)
        self.CartTable.column("qty", width=50)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #===ADD Cart Widgets Frame==
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550,width=530, height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry (Add_CartWidgetsFrame, textvariable=self.var_pname,font=("times new roman",15), bg="lightyellow", state='readonly').place(x=5,y=35, width=190, height=22)
        lbl_p_price=Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry (Add_CartWidgetsFrame, textvariable=self.var_price,font=("times new roman",15), bg="lightyellow", state='readonly').place(x=230,y=35, width=150, height=22)
        lbl_p_qty=Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry (Add_CartWidgetsFrame, textvariable=self.var_qty,font=("times new roman",15), bg="lightyellow").place(x=390,y=35, width=120, height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame, text="In Stock [0]", font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame, text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray", cursor="hand2").place(x=180,y=70,width=150, height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame, text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange", cursor="hand2").place(x=340,y=70,width=180, height=30)

        #===billing area====:
        billFrame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=110, width=410, height=410)
        BTitle=Label(billFrame,text="Customer Bill Area", font=("goudy old style", 20,"bold"),bg="#262626", fg="white").pack(side=TOP, fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        billMenuFrame=Frame(self.root, bd=2,relief=RIDGE, bg= 'white')
        billMenuFrame.place(x=953, y=520, width=410, height=140)
        self.lbl_amnt=Label(billMenuFrame, text='Bill Amount\n[0]',font=("goudy old style", 15,"bold"),bg="orange")
        self.lbl_amnt.place(x=2,y=5,width=120, height=70)
        
        self.lbl_discount=Label(billMenuFrame, text='Discount\n5%',font=("goudy old style", 15,"bold"),bg="yellow")
        self.lbl_discount.place(x=124,y=5,width=120, height=70)
        
        self.lbl_net_pay=Label(billMenuFrame, text='Net Pay\n[0]',font=("goudy old style", 15,"bold"),bg="red")
        self.lbl_net_pay.place(x=246,y=5,width=160, height=70)

        btn_print=Button(billMenuFrame, text='Print',command=self.print_bill, font=("goudy old style",15,"bold"),bg="lightgreen")
        btn_print.place(x=2,y=80,width=120, height=50)
        btn_clear_all=Button(billMenuFrame, text='Clear All',command=self.clear_all, font=("goudy old style",15, "bold"),bg="lightgray")
        btn_clear_all.place(x=124, y=80,width=120, height=50)
        btn_generate=Button(billMenuFrame, text='Generate/Save Bill',command=self.generate_bill,font=("goudy old style",11, "bold"),bg="light blue")
        btn_generate.place(x=246,y=80,width=160, height=50)

        self.show()
        self.bill_top()

    def show(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            cur.execute("Select pid,name,price,qty,status from product where status='In-Stock' order by pid")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END, values=row)
        except Exception as ex:
            messagebox.showerror ("Error",f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required", parent=self.root)
            else:
                cur.execute("Select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%'and status='In-Stock'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required", parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        else:
            price_cal=float(self.var_price.get())
            price_cal=float(price_cal)
            cart_data=[self.var_pid.get(), self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #=======update_cart====
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                messagebox. askyesno('Confirm',"Product already present\nDo you want to Update Remove from the Cart List")
                if self.var_qty.get()=="0":
                    self.cart_list.pop(index_)
                else:
                    # pid,name, price, qty,status
                    self.cart_list[index_][2]=price_cal #price
                    self.cart_list[index_][3]=self.var_qty.get()#qty
            else:
                self.cart_list.append(cart_data)
                        
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amount\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror ("Error",f"Please Add product to the Cart!!!", parent=self.root)
        else:
            #====BILL Top====
            self.bill_top()
            #====BILL Middle====
            self.bill_middle()
            #====BILL Bottom====
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated/Save in Backend",parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\t Urban Grocer
\tPhone No: {self.var_contact.get()}  , Mumbai-400002
{str("="*47)}
Customer Name: {self.var_cname.get()}
Ph no. :{self.var_contact.get()}
Bill No: {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name\t\t\tQTY\tPrice
{str("="*47)}
            '''
        self.txt_bill_area.delete('1.0' , END)
        self.txt_bill_area.insert('1.0', bill_top_temp)


    def bill_middle(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Out-Of-Stock'
                if int(row[3])!=int(row[4]):
                    status='In-Stock'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END, "\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                # ====update qty in product table========
                cur.execute('Update product set qty=%s, status=%s where pid=%s',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            self.show()
        except Exception as ex:
            messagebox.showerror ("Error",f"Error due to : {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\t\tRs.{self.bill_amnt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n    
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0
    
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print', "Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open (new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror('Print',"Please generate bill, to print the receipt", parent=self.root)

if __name__ =="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()