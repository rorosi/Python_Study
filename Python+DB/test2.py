import mysql.connector as mysql
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as MessageBox


def insert():
    id = e_id.get()
    name = e_name.get()
    product = e_product.get()
    stock = e_stock.get()

    if (name == "" or product == "" or stock == ""):
        MessageBox.showinfo("Insert Status", "ALL FIELDS ARE REQUIRED")
    elif (id != ""):
        MessageBox.showinfo("Insert Status", "번호를 넣지 마시오!")
    else:
        con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial",
                            auth_plugin="mysql_native_password")
        cursor = con.cursor()
        cursor.execute("insert into sample (name,product,date,stock) values(%s,%s,now(),%s)", (name, product, stock))
        cursor.execute("commit");

        e_name.delete(0, 'end')
        e_product.delete(0, 'end')
        e_stock.delete(0, 'end')
        MessageBox.showinfo("Insert Status", "등록하였습니다.")
        con.close()


def delete():
    id = e_id.get()
    if (id == ""):
        MessageBox.showinfo("Delete Status", "삭제하실 번호를 넣어주세요")
    else:
        con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
        cursor = con.cursor()
        cursor.execute("delete from sample where id = '" + e_id.get() + "'")
        cursor.execute("commit");
        reset()
        e_id.delete(0,'end')
        e_name.delete(0, 'end')
        e_product.delete(0, 'end')
        e_stock.delete(0, 'end')
        MessageBox.showinfo("Delete Status", "SUCCESS")
        con.close()



def update():
    id = e_id.get()
    name = e_name.get()
    product = e_product.get()
    stock = e_stock.get()

    if (name == "" or product == "" or stock == ""):
        MessageBox.showinfo("update Status", "ALL FIELDS ARE REQUIRED")
    else:
        con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
        cursor = con.cursor()
        cursor.execute("update sample set name='"+ name +"',product='"+ product +"', stock='"+ stock +"' where id='"+ id + "'")
        cursor.execute("commit");

        e_name.delete(0, 'end')
        e_product.delete(0, 'end')
        e_stock.delete(0, 'end')
        MessageBox.showinfo("update Status", "수정하였습니다.")
        con.close()


def get():
    treeview.delete(*treeview.get_children())
    if (e_id.get() == ""):
        MessageBox.showinfo("get Status", "id is compolsary for get")
    else:
        con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
        cursor = con.cursor()
        cursor.execute("select * from sample where id = '" + e_id.get() + "'")
        rows = cursor.fetchall()

        for row in rows:
            e_name.insert(0, row[1])
            e_product.insert(0, row[2])
            e_stock.insert(0, row[3])

        for row in rows:
            treeview.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))

        con.close()


def show():
    treeview.delete(*treeview.get_children())
    con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
    cursor = con.cursor()
    cursor.execute("select * from sample")
    rows = cursor.fetchall()
    for row in rows:
        treeview.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))

    con.close()


def reset():
    con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
    cursor = con.cursor()
    cursor.execute("ALTER TABLE sample AUTO_INCREMENT = 1")
    cursor.execute("SET @COUNT = 0")
    cursor.execute("update sample set id = @COUNT:=@COUNT+1")
    cursor.execute("commit");

    con.close()

put_pg = tk.Tk()
put_pg.title("데이터 입력 프로그램")
put_pg.geometry("500x700")


# 라벨
step = LabelFrame(put_pg,text="물품 입력:")
step.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=12)
Label(step,text="번호",font = "Arial 8 bold italic").grid(row=0,sticky='n', padx=5, pady=7)
Label(step,text="작성자",font = "Arial 8 bold italic").grid(row=1,sticky='n', padx=5, pady=7)
Label(step,text="상품명",font = "Arial 8 bold italic").grid(row=2,sticky='n', padx=5, pady=7)
Label(step,text="재고",font = "Arial 8 bold italic").grid(row=3,sticky='n', padx=5, pady=7)

# 버튼
Button(step,text ="입력",width=10,font=('Bahnschrift SemiBold', 8),activebackground="red",command=insert).grid(row=5,column=0,sticky=W,pady=4,padx=5)
Button(step,text="삭제",width=10,font=('Bahnschrift SemiBold', 8),command = delete).grid(row=5,column=2,sticky=W,pady=4,padx=5)
Button(step,text="수정",width=10,font=('Bahnschrift SemiBold', 8),command = update).grid(row=5,column=4,sticky=W,pady=4,padx=5)

get = Button(put_pg, text="데이터 조회", font=('Bahnschrift SemiBold', 10), bg="#d2d2d2", overrelief= "solid", command=get)
get.place(x=300, y=180)

show = Button(put_pg, text="전체 조회", font=('Bahnschrift SemiBold', 10), bg="#d2d2d2", overrelief= "solid", command=show)
show.place(x=400, y=180)

# 입력창
e_id = tk.Entry(step)
e_name = tk.Entry(step)
e_product = tk.Entry(step)
e_stock = tk.Entry(step)

e_id.place(x=90, y=10)
e_name.place(x=90, y=40)  # 위치를 지정해주는 명령어
e_product.place(x=90, y=70)
e_stock.place(x=90, y=100)

put_pg.bind('<Return>', input)  # 엔터키(이벤트)를 input 함수로 연결.

# 표 생성하기
step2 = LabelFrame(put_pg,text="상품 현황:")
step2.grid(row=1, columnspan=7, sticky='W',padx=5, pady=5, ipadx=243, ipady=128)
treeview = ttk.Treeview(step2, selectmode="extended", columns=["번호", "작성자", "상품명", "재고", "작성날짜"], displaycolumns=["번호", "작성자",
                                                                                                            "상품명", "재고", "작성날짜"])
treeview.place(x=0, y=10)
treeview.column("#0", width=0)
treeview.heading("번호", text="번호", anchor="center")

treeview.column("#1", width=50)
treeview.heading("작성자", text="작성자", anchor="center")

treeview.column("#2", width=80)
treeview.heading("상품명", text="상품명", anchor="center")

treeview.column("#3", width=100)
treeview.heading("재고", text="재고", anchor="center")

treeview.column("#4", width=50)
treeview.heading("작성날짜", text="작성날짜", anchor="center")

put_pg.mainloop()