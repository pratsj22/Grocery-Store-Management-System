from tkinter import *
# from PIL import Image,ImageTk
from tkinter import ttk,messagebox

from sql_connection import get_sql_connection

class productClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1050x570+300+130")
        self.root.title("Grocery Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #-------Variables---------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.sup_list = ['Select', 'Yash Enterprises', 'Megha Supermart', '11th Avenue Grocery Store','Signature Supermarket','Millennial Grocery Store']
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        product_Frame=Frame(self.root, bd=2,relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)
        
        #===title====
        title = Label(product_Frame, text="Manage Products",font=("goudy old style",18), bg="#0f4d7d",fg="white").pack(side=TOP, fill=X)
        
        lbl_supplier = Label(product_Frame, text="Supplier",font=("goudy old style",18), bg="white").place(x=30, y=60)
        lbl_product_name = Label(product_Frame, text="Name",font=("goudy old style",18), bg="white").place(x=30, y=110)
        lbl_price = Label(product_Frame, text="Price",font=("goudy old style",18), bg="white").place(x=30, y=160)
        lbl_qty = Label(product_Frame, text="Quantity",font=("goudy old style",18), bg="white").place(x=30, y=210)
        lbl_status = Label(product_Frame, text="Status",font=("goudy old style",18), bg="white").place(x=30, y=260)

        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER, font=("goudy old style",15))
        cmb_sup.place(x=150,y=60,width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("goudy old style",15), bg="white").place(x=150, y=110, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("goudy old style",15), bg="white").place(x=150, y=160, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style",15), bg="white").place(x=150, y=210, width=200)
        
        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status,values=("In-Stock", "Out-Of-Stock"),state='readonly',justify=CENTER, font=("goudy old style",15))
        cmb_status.place(x=150,y=260,width=200)
        cmb_status.current(0)

        btn_add=Button (product_Frame, command=self.add, text="Add", font=("goudy old style", 15),bg="#2196f3",fg="white",cursor="hand2").place(x=10, y=400, width=100,height=40)
        btn_update=Button(product_Frame, command=self.update, text="Update", font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete=Button(product_Frame, command=self.delete, text="Delete", font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230, y=400,width=100, height=40)
        btn_clear=Button(product_Frame, command=self.clear, text="Clear", font=("goudy old style",15),bg="#607d8b",fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)

        #-----SearchFrame----
        SearchFrame = LabelFrame(self.root,text="Search Products", font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=470, y=10, width=575, height=80)

        #-----Search options----
        cmb_search=ttk.Combobox(SearchFrame, textvariable=self.var_searchby,values=("Select", "Supplier", "Name"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search= Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style",15), bg="white").place(x=200, y=10, width=200)
        btn_search= Button(SearchFrame, command=self.search, text="Search", font=("goudy old style",15),bg="#4caf50",fg="white").place(x=410,y=9,width=150, height=30)

        #----TreeView-------
        p_frame=Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=470, y=100, width=575, height=390)
        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)
        self.product_table=ttk.Treeview(p_frame,columns=("pid", "Supplier", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.xview)

        #----Adding Headings to TreeView-------
        self.product_table.heading("pid",text="P ID")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name",text="Product Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status",text="Status")
        self.product_table["show"] = "headings"
        
        self.product_table.pack(fill=BOTH, expand=1)

        self.product_table.column("pid",width=40)
        self.product_table.column("Supplier",width=160)
        self.product_table.column("name",width=115)
        self.product_table.column("price",width=95)
        self.product_table.column("qty",width=65)
        self.product_table.column("status",width=95)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)

        self.show()
    #----Database Part-------
    def show(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            cur.execute("Select * from product order by pid")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END, values=row)
        except Exception as ex:
            messagebox.showerror ("Error",f"Error due to : {str(ex)}", parent=self.root)

    def add(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            if self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All field are required",parent=self.root)
            else:
                cur.execute("""Select * from product where name=%s""",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror ("Error","Product already available", parent=self.root)
                else:
                    print(self.var_sup.get())
                    print(self.var_name.get())
                    print(self.var_price.get())
                    print(self.var_qty.get())
                    print(self.var_status.get())
                    cur.execute("""Insert into product (Supplier, name, price, qty, status) values(%s, %s, %s, %s, %s)""",
                    (
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror ("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def update(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Product Name required",parent=self.root)
            else:
                cur.execute("UPDATE PRODUCT SET Supplier=%s, name=%s, price=%s, qty=%s, status=%s where pid=%s",
                (
                    self.var_sup.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get(),
                    self.var_pid.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Product Updated Successfully",parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror ("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Name required",parent=self.root)
            else:
                conf = messagebox.askyesno("Confirm", "Do you really want to delete record ?", parent=self.root)
                if(conf==True):
                    cur.execute("DELETE FROM PRODUCT WHERE pid=%s",(self.var_pid.get(),)) 
                    con.commit()
                    messagebox.showinfo("Success", "Product Deleted Successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_pid.set("")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("In-Stock")

        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=get_sql_connection()
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror ("Error","Select Search By option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required", parent=self.root)
            else:
                cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data (self, ev):
        f=self. product_table.focus()
        content=(self. product_table.item(f))
        row=content['values']

        self.var_pid.set(row[0])
        self.var_sup.set(row[1])
        self.var_name.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.var_status.set(row[5])

    

if __name__ =="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()