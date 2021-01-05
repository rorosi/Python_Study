import mysql.connector as mysql
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as MessageBox


def insert():
    id = e_id.get()
    name = e_name.get()
    product = e_product.get()
    date = e_date.get()

    if(name=="" or product=="" or date==""):
        MessageBox.showinfo("Insert Status", "ALL FIELDS ARE REQUIRED")
    elif(id != ""):
        MessageBox.showinfo("Insert Status","번호를 넣지 마시오!")
    else:
        con = mysql.connect(host="localhost",user="root",password="xowjd57",database="tutorial",auth_plugin="mysql_native_password")
        cursor = con.cursor()
        cursor.execute("insert into sample (name,product,date) values(%s,%s,%s)",(name,product,date))
        cursor.execute("commit");

        e_name.delete(0,'end')
        e_product.delete(0, 'end')
        e_date.delete(0, 'end')
        MessageBox.showinfo("Insert Status", "SUCCESS")
        con.close()

def delete():
    id = e_id.get()
        try:
            if (id == ""):
                try:
                    MessageBox.showinfo("Delete Status", "삭제하실 번호를 넣어주세요")
                except ValueError:
                    MessageBox.showinfo("Delete Status", "숫자만 입력하세요")
            else:
                con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
                cursor = con.cursor()
                cursor.execute("delete from sample where id = '" + e_id.get() + "'")
                cursor.execute("commit");
                reset()
                e_name.delete(0, 'end')
                e_product.delete(0, 'end')
                e_date.delete(0, 'end')
                MessageBox.showinfo("Delete Status", "SUCCESS")
                con.close()
        except ValueError:
            MessageBox.showinfo("Delete Status", "숫자만 입력하세요")

def update():
    id = e_id.get();
    name = e_name.get();
    product = e_product.get();
    date = e_date.get();

    if (name == "" or product == "" or date == ""):
        MessageBox.showinfo("Update Status", "ALL FIELDS ARE REQUIRED")
    else:
        con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
        cursor = con.cursor()
        cursor.execute("update sample set name='"+ name +"',product='"+ product +"', date='"+ date +"' where id='"+ id + "'")
        cursor.execute("commit");

        e_name.delete(0, 'end')
        e_product.delete(0, 'end')
        e_date.delete(0, 'end')
        MessageBox.showinfo("Update Status", "SUCCESS")
        con.close()

def get():
        treeview.delete(*treeview.get_children())
        if (e_id.get() == ""):
            MessageBox.showinfo("Delete Status", "id is compolsary for delete")
        else:
            con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
            cursor = con.cursor()
            cursor.execute("select * from sample where id = '"+ e_id.get() +"'")
            rows = cursor.fetchall()

            for row in rows:
                e_name.insert(0, row[1])
                e_product.insert(0,row[2])
                e_date.insert(0, row[3])

            for row in rows:
                treeview.insert('', 'end', values=(row[0], row[1], row[2], row[3]))

            e_name.delete(0, 'end')
            e_product.delete(0, 'end')
            e_date.delete(0, 'end')
            con.close()

def show():
    treeview.delete(*treeview.get_children())
    con = mysql.connect(host="localhost", user="root", password="xowjd57", database="tutorial")
    cursor = con.cursor()
    cursor.execute("select * from sample")
    rows = cursor.fetchall()
    for row in rows:
        treeview.insert('', 'end', values=(row[0], row[1], row[2], row[3]))

    con.close

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

id = tk.Label(put_pg, text="번호")
id.place(x=0, y=10)
name = tk.Label(put_pg, text="작성자")
name.place(x=0, y=40)
product = tk.Label(put_pg, text="상품명")
product.place(x=0, y=70)
date = tk.Label(put_pg, text="입력일")
date.place(x=0, y=100)

# 버튼

insert = tk.Button(put_pg, text='입력', command=insert)
insert.place(x=200, y=10)

delete = Button(put_pg, text="삭제", font=("italic",10), bg="white", command=delete)
delete.place(x=200, y=30)

update = Button(put_pg, text="수정", font=("italic",10), bg="white", command=update)
update.place(x=200,y=50)

get = Button(put_pg, text="데이터 조회", font=("italic",10), bg="white", command=get)
get.place(x=200, y=70)

show = Button(put_pg, text="전체 조회", font=("italic",10), bg="white", command=show)
show.place(x=200, y=100)

# 입력창
e_id = tk.Entry(put_pg, width=20)
e_name = tk.Entry(put_pg, width=20)
e_product = tk.Entry(put_pg, width=20)
e_date = tk.Entry(put_pg, width=20)

e_id.place(x=48, y=10)
e_name.place(x=48, y=40)  # 위치를 지정해주는 명령어
e_product.place(x=48, y=70)
e_date.place(x=48, y=100)

put_pg.bind('<Return>', input)  # 엔터키(이벤트)를 input 함수로 연결.

# 표 생성하기
treeview = ttk.Treeview(put_pg, selectmode="extended", columns=["번호", "작성자", "상품명", "입력일"], displaycolumns=["번호", "작성자",
                                                                                                            "상품명",
                                                                                                            "입력일"])
treeview.place(x=10, y=170)
treeview.column("#0", width=50)
treeview.heading("번호", text="번호", anchor="center")

treeview.column("#1", width=50)
treeview.heading("작성자", text="작성자", anchor="center")

treeview.column("#2", width=50)
treeview.heading("상품명", text="상품명", anchor="center")

treeview.column("#3", width=50)
treeview.heading("입력일", text="입력일", anchor="center")

put_pg.mainloop()