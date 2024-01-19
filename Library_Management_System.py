#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime as dt 


# In[2]:


def create_server_connection(host_name, user_name, user_password,user_db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=user_db
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


# In[3]:


connection = create_server_connection("localhost", "root",'sayak2004',"mydb_library")


# In[4]:


def addbook():
    bn=input("Enter BOOK Name:")
    c=input("Enter BOOK Code:")
    t=input("Total Books:")
    s=input("Enter subject:")
    data=(bn,c,t,s,'failure')
    #sql='insert into book(name,code,total,subject) values(%s,%s,%s,%s)'
    
    sql='call proc_bookresigtration(%s,%s,%s,%s)'
    
    try:
        cursor = connection.cursor()
        status = cursor.callproc('proc_bookresigtration',data)
        cursor.execute('select @_proc_bookresigtration_4' )
        print(cursor.fetchone())
        #connection.commit()
        print(">------------------------------------------<")
        print("Data Entered Successfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)
    main()


# In[5]:


def main():
    print(""" 
                            LIBRARY MANAGER
    1.ADD BOOK
    2.ISSUE BOOK
    3.SUBMIT BOOK
    4.DELETE BOOK
    5.DISPLAY BOOKS
    6.STUDENT REGISTRATION 
    """)
    choice=input("Enter Task No.:")
    print(">----------------------------------------<")
    if (choice=='1'):
        addbook()
    elif(choice=='2'):
        issueb()
    elif(choice=='3'):
        submitb()
    elif(choice=='4'):
        dbook()
    elif(choice=='5'):
        dispbook()
    elif(choice=='6'):
        studentreg()
    else:
        print("Wrong Choice......")
        main()


# In[6]:


def issueb():
    r=input("Enter Reg No:")
    co=input("Enter Book Code:")
    d=input("Enter Date:")
    date_str = '29/12/2017' # The date - 29 Dec 2017

    format_str = '%d/%m/%Y' # The format
    datetime_obj = dt.datetime.strptime(d, format_str)
    #print(datetime_obj.date())

    data =(r,co,datetime_obj.date(),'failure')
    sql='call proc_bookissue(%s,%s,%s)'
    
    
    try:
        cursor = connection.cursor()
        status = cursor.callproc('proc_bookissue',data)
        cursor.execute('select @_proc_bookresigtration_4' )
        print(cursor.fetchone())
        #connection.commit()
        print(">------------------------------------------<")
        print("Book issued succesfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)
    main()


# In[7]:


def studentreg():
    n=input("Enetr Name:")
    r=input("Enter Reg No:")
    data =(n,r,'failure')
    #sql="insert into student(name,registration) value(%s,%s)"
    
    sql='call proc_bookresigtration(%s,%s,%s,%s)'
    
    
    try:
        cursor = connection.cursor()
        status = cursor.callproc('proc_studentregistration',data)
        cursor.execute('select @_proc_bookresigtration_2' )
        print(cursor.fetchone())
        #connection.commit()
        print(">------------------------------------------<")
        print("Data Entered Successfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)
    main()


# In[8]:


def dbook():
    ## delete book from master 
    co=input("Enter Book Code:")
    data =(co,'failure')
    sql='call proc_bookdelete(%s)'
    
    
    try:
        cursor = connection.cursor()
        status = cursor.callproc('proc_bookdelete',data)
        cursor.execute('select @_proc_bookdelete_1' )
        print(cursor.fetchone())
        #connection.commit()
        print(">------------------------------------------<")
        print("Book delete succesfully")
    except Exception as e:
        print("Book1 Already issued ")
        print(e)
    main()


# In[9]:


def submitb():
    r=input("Enter Reg No:")
    co=input("Enter Book Code:")
    d=input("Enter Date:")
    date_str = '29/12/2017' # The date - 29 Dec 2017

    format_str = '%d/%m/%Y' # The format
    datetime_obj = dt.datetime.strptime(d, format_str)
    #print(datetime_obj.date())

    data =(r,co,datetime_obj.date(),'failure')
    sql='call proc_bookreturn(%s,%s,%s)'
    
    
    try:
        cursor = connection.cursor()
        status = cursor.callproc('proc_bookreturn',data)
        cursor.execute('select @_proc_bookreturn_4' )
        print(cursor.fetchone())
        #connection.commit()
        print(">------------------------------------------<")
        print("Book Return succesfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)
    main()


# In[10]:


def dispbook():
    a="select * from book"
    c=connection.cursor()
    c.execute(a)
    myresult=c.fetchall()
    for i in myresult:
        print("Book Name:",i[0])
        print("Book Code:",i[1])
        print("Total:",i[3])
        print(">---------------------------------------<")
    main()


# In[ ]:


def pswd():
    ps=input("Enter Password")
    if ps=="XYZ@SCHOOL":
        main()
    else:
        print("Wrong Password")
        pswd()
pswd()    

