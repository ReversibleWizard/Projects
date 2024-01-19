#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector
from datetime import datetime
from ipywidgets import Dropdown
import IPython.display as display
import random
import sys
import keyboard


# In[2]:


from mysql.connector import Error


# In[3]:


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


# In[4]:


connection = create_server_connection("localhost","root","sayak","bankdb")


# In[5]:

def check():
    while True:
        try:
            if keyboard.is_pressed('ENTER'):
                #print("you pressed Enter, so printing the list..")
                #print(a)
                break
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        except:
            break


def new_account():
    acc_num=random.randint(100000,999999)
    f_name = str(input("Enter your first name:"))
    check()
    l_name = str(input("Enter your last name:"))
    check()
    aadhar = int(input("Enter your Aadhar card number:"))
    check()
    dob_in = input("Enter your date of birth(dd/mm/yyyy):")
    check()
    dob =  datetime.strptime(dob_in, '%d/%m/%Y')
    check()
    addr = str(input("Enter your complete address:"))
    check()
    spl_sec_num = random.randint(10000,99999)
    
    acc_type = ' '
    while acc_type.lower() not in ['current', 'savings']:
        acc_type = input("Enter your account type(Current/Savings):")
        check()
        if acc_type.lower() not in ['current', 'savings']:
            print("Please enter a valid account type")
    bal = float(input("Enter the amount you want to deposit:"))
    check()
    pin = 0
    rpin = 1
    while(pin!=rpin):
        pin = int(input("Enter your pin:"))
        check()
        rpin = int(input("Please re-enter your pin:"))
        check()
        if pin!=rpin:
            print("The pin didn't match")
    print(">------------------------------------------<")
    data = (acc_num,f_name,l_name,aadhar,dob,addr,acc_type,bal,pin,spl_sec_num,)
    sql='call proc_Accounts(%s,%s,%s,%s,%s,%s,%s)'
    
    try:
        cursor = connection.cursor()
        if acc_type.lower() in ['current']:
            cursor.execute('INSERT INTO curr_accounts Values (%s,%s,%s,%s,%s,%s,%s,%s)',
                           (acc_num,f_name,l_name,aadhar,dob,addr,bal,pin,))
        elif acc_type.lower() in ['savings']:
            cursor.execute('INSERT INTO sav_accounts Values (%s,%s,%s,%s,%s,%s,%s,%s)',
                           (acc_num,f_name,l_name,aadhar,dob,addr,bal,pin,spl_sec_num,))
        #status = cursor.callproc('Accounts',data)
        cursor.execute('INSERT INTO Accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(data) )
        #print(cursor.fetchone())
        connection.commit()
        print(">------------------------------------------<")
        print("Your Account number is:{}".format(acc_num))
        print("Your Special Security number is:{}".format(spl_sec_num))
        print("Data Entered Successfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[6]:


#new_account(2)


# In[7]:


def view_account():
    acc_num = int(input("Enter your Account number:"))
    check()
    f_name = str(input("Enter your First name:"))
    check()
    dob_in = input("Enter your date of birth(dd/mm/yyyy):")
    check()
    dob =  datetime.datetime.strptime(dob_in, '%d-%m-%Y')
    check()
    pin = int(input("Please enter your pin:"))
    check()
    print(">------------------------------------------<")
    data = (acc_num,f_name,dob,pin,)
    try:
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM bankdb.accounts WHERE (acc_num=(%s) AND f_name=(%s) AND 
                       dob=(%s) AND pin=(%s))''',(acc_num,f_name,dob,pin,))
        #print(cursor.fetchone())
        result = cursor.fetchone()
        connection.commit()
        print("Data Found Successfully")
        print("Account number:{}".format(result[0]))
        print("First Name:{}".format(result[1]))
        print("Last Name:{}".format(result[2]))
        print("Aadhar Card Number:{}".format(result[3]))
        print("Date of Birth:{}".format(result[4]))
        print("Address:{}".format(result[5]))
        print("Account type:{}".format(result[6]))
        print(">------------------------------------------<")
        #for x in result:
         #   print(x)
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[8]:


#view_account()


# In[9]:


def deposit_money():
    acc_num = int(input("Enter your Account number:"))
    check()
    time = datetime.now()
    transaction_type = 'Debit'
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_num,))
        result = cursor.fetchone()
        pin = None
        while pin!=result[8]:
            pin = int(input("Enter your pin:"))
            if pin==result[8]:
                deposit = float(input("Enter the amount you want to deposit:"))
                new_bal=deposit+result[7]
                cursor.execute("UPDATE bankdb.accounts SET balance=(%s) WHERE acc_num=(%s)"
                               ,(new_bal,acc_num,))
                cursor.execute("INSERT INTO bankdb.transactions Values (%s,%s,%s,%s)",
                              (acc_num,time,transaction_type,deposit,))
                connection.commit()
                print("The money has been deposited")
            elif pin!=result:
                print("Incorrect Pin entered!!!")
            print(">-----------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[10]:


#deposit_money()


# In[11]:


def withdraw_money():
    acc_num = int(input("Enter your Account number:"))
    check()
    time = datetime.now()
    transaction_type = 'Credit'
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_num,))
        result = cursor.fetchone()
        pin = None
        while pin!=result[8]:
            pin = int(input("Enter your pin:"))
            check()
            if pin==result[8]:
                withdraw = float(input("Enter the amount you want to withdraw:"))
                check()
                if result[7]>=withdraw:
                        if result[7]<withdraw:
                            print("You have low balance!!")
                            withdraw_money()
                        new_bal=result[7]-withdraw
                                        
                cursor.execute("UPDATE bankdb.accounts SET balance=(%s) WHERE acc_num=(%s)"
                               ,(new_bal,acc_num,))
                cursor.execute("INSERT INTO bankdb.transactions Values (%s,%s,%s,%s)",
                              (acc_num,time,transaction_type,withdraw,))
                print("Your money is withdrawn")
                connection.commit()
            elif pin!=result:
                print("Incorrect Pin entered!!!")
        print(">----------------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)    


# In[12]:


#withdraw_money()


# In[13]:


def transfer():
    acc_no_1 = int(input("Enter your Account number :"))
    check()
    time = datetime.now()
    transaction_type_1 = 'Credit'
    transaction_type_2 = 'Debit'
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_no_1,))
        result1 = cursor.fetchone()
        pin = None
        while pin!=result1[8]:
            pin = int(input("Enter your pin:"))
            if(pin!=result1[8]):
                print("Incorrect Pin!!")
                
        acc_no_2 = int(input("Enter the reciver Account number:"))
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_no_2,))
        result2 = cursor.fetchone()
        if result2:
            pass
        else:
            print("Incorrect Account number")
            print("Sorry!! Please Re-enter all the details")
            transfer()
        Amount = float(input("Enter the amount your want to transfer:"))
        bal1 = result1[7] - Amount
        bal2 = result2[7] + Amount
        cursor.execute("UPDATE bankdb.accounts SET balance=(%s) WHERE acc_num=(%s)"
                               ,(bal1,acc_no_1,))
        cursor.execute("UPDATE bankdb.accounts SET balance=(%s) WHERE acc_num=(%s)"
                               ,(bal2,acc_no_2,))
        cursor.execute("INSERT INTO bankdb.transactions Values (%s,%s,%s,%s)",
                              (acc_no_1,time,transaction_type_1,Amount,))
        cursor.execute("INSERT INTO bankdb.transactions Values (%s,%s,%s,%s)",
                              (acc_no_2,time,transaction_type_2,Amount,))
        print("The Amount is transffered!!")
        connection.commit()
        print(">----------------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)       
        


# In[14]:


#transfer()


# In[15]:


def delete():
    acc_num = int(input("Please enter your account number:"))
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_num,))
        result = cursor.fetchone()
        pin = None
        while pin!=result[8]:
            pin = int(input("Enter your pin:"))
            if pin==result[8]:
                sure = str(input("Are you sure you want to delete your account(Y/N):"))
                if sure=='Y'or'y':
                    print("Your account with ACCOUNT NUMBER {} and ACCOUNT NAME {} is deleted".
                          format(result[0],(result[1]+' '+result[2])))
                    cursor.execute("DELETE FROM bankdb.accounts WHERE acc_num=(%s)",(acc_num,))
                connection.commit()
            elif pin!=result:
                print("Incorrect Pin entered!!!")
            print(">-----------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[16]:


#delete()


# In[17]:


def change_detail():
    acc_num = int(input("Please enter your Account num:"))
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_num,))
        result = cursor.fetchone()
        pin = None
        while pin!=result[8]:
            pin = int(input("Enter your pin:"))
            if pin==result[8]:
                print("The details you can change are:")
                print("1.Address")
                print("2.PIN")
                opt = 0
                while opt not in [1,2]:
                    opt = int(input("Please Enter your option number:"))
                    if opt==1:
                        sure = str(input("Are you sure you want to change your First name(Y/N):"))
                        if sure=='Y'or'y':
                            o_addr = None
                            while o_addr!=result[5]:
                                o_addr = str(input("Please enter your old Address:"))
                                if o_addr!=result[5]:
                                    print("Incorrect Old Address!!!!!")
                            n_addr = 'A'
                            r_n_addr = 'B'
                            while n_addr!=r_n_addr:
                                n_addr = str(input("Enter your new Address:"))
                                r_n_addr = str(input("Please re-enter your new Address:"))
                                if(n_addr!=r_n_addr):
                                    print("Address don't match!!!")
                                    print("Please Re-Enter")
                            cursor.execute("UPDATE bankdb.accounts SET addr=(%s) WHERE acc_num=(%s);",
                                           (n_addr,acc_num,))
                            print("Your Address has been changed!!!!!!!!!!!")
                            
                    elif opt==2:
                        sure = str(input("Are you sure you want to change your pin(Y?N):"))
                        if sure=='Y' or 'y':
                            n_pin = 0
                            r_n_pin = 1
                            while n_pin!=r_n_pin:
                                n_pin = int(input("Please enter your new 4 digit pin:"))
                                r_n_pin = int(input("Please re-enter your new pin:"))
                                if n_pin!=r_n_pin:
                                    print("The above two didn't match!!!")
                            cursor.execute("UPDATE bankdb.accounts SET pin=(%s) WHERE acc_num=(%s);",
                                           (n_pin,acc_num,))
                            print("Your PIN has been changed!!!!!")
                    else:
                        print("Please Enter a valid choice!!!!!!!!")
                connection.commit()
            elif pin!=result:
                print("Incorrect Pin entered!!!")
            print(">-----------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[18]:


#change_detail()


# In[19]:


def transaction_detials():
    acc_num = int(input("Please Enter your Account number:"))
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_num,))
        result = cursor.fetchone()
        if result==None:
            print('''Account number not found!!!
            Please Enter a valid Account number''')
            transaction_details()
            exit()
        pin = None
        while pin!=result[8]:
            pin = int(input("Enter your pin:"))
            if pin==result[8]:
                cursor.execute('SELECT * FROM bankdb.transactions WHERE (Account_Nunber=(%s))',(acc_num,))
                transactions = cursor.fetchall()
                print("Date and Time , Transaction Type , Transaction Amount")
                print("-----------------------------------")
                for x in range(len(transactions)):
                    print(f"{transactions[x][1]} , {transactions[x][2]} , {transactions[x][3]} ")
                    print("-------------------------------------")
                connection.commit()
            elif pin!=result:
                print("Incorrect Pin entered!!!")
            print(">-----------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[20]:


#transaction_detials()


# In[21]:


def new_employee():
    emp_id = random.randint(100,9999)
    emp_name = str(input("Enter employee name:"))
    emp_pass = None
    re_emp_pass = ' '
    while emp_pass!=re_emp_pass:
        emp_pass = str(input("Enter your password:"))
        re_emp_pass = str(input("Re-enter your password:"))
        if emp_pass!=re_emp_pass:
            print("The two passwords didn't match")
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO bankdb.employee Values (%s,%s,%s)',(emp_id,emp_name,emp_pass,))
        connection.commit()
        print(">------------------------------<")
        print("Your Employee Id is {}".format(emp_id))
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[22]:


#new_employee()


# In[23]:


def emp_login():
    emp_id = int(input("Enter your employee id:"))
    time = datetime.now()
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.employee WHERE (employee_id=(%s))',(emp_id,))
        result = cursor.fetchone()
        emp_pass = ' '
        while emp_pass!=result[2]:
            emp_pass = str(input("Enter your password:"))
            if emp_pass!=result[2]:
                print("Incorrect Password!!!!")
            
        if emp_pass==result[2]:
            cursor.execute('INSERT INTO bankdb.employee_entry Values (%s,%s)',(emp_id,time,))
            return True
        connection.commit()
        print("You are logged in")
        print(">-------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


# In[24]:


#emp_login()


# In[38]:


def customer_login():
    time = datetime.now()
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bankdb.accounts")
        check_result = cursor.fetchall()
        check = False
        while check!=True:
            acc_num = int(input("Please Enter your Account number:"))
            for x in range(len(check_result)):
                if acc_num==check_result[x][0]:
                    check = True
                    correct_pin = check_result[x][8] 
                    break
                else :
                    check = False
            if check==False:
                print("Enter a valid account number!!!!!!")
        if check==True:
            pin = 0
            while pin!=correct_pin:
                pin = int(input("Enter your Account Pin:"))
                if pin!=correct_pin:
                    print("Please enter correct pin!!!!!!")
            cursor.execute('INSERT INTO bankdb.customer_entry VALUES (%s,%s)',(acc_num,time,))
            b = True
        return [b,acc_num]
    
    except Exception as e:
        print("Data Entered wrongly")
        print(e)        
            


# In[40]:


#customer_login()


# In[41]:


def new_account_for_existing_customer_via_employee():

    try:
        acc_num = int(input("Enter your account number:"))
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))',(acc_num,))
        result = cursor.fetchone()
        if result==None:
            print("The account doesn't exist")
            ans = input("Do you want create a new account(Y/N):")
            if ans.upper()=='Y':
                new_account()
            else:
                return
        new_acc_num=random.randint(100000,999999)
        f_name = result[1]
        l_name = result[2]
        aadhar = result[3]
        dob = result[4]
        addr = result[5]
        spl_sec_num = random.randint(10000,99999)
    
        acc_type = ' '
        while acc_type.lower() not in ['current', 'savings']:
            acc_type = input("Enter your account type(Current/Savings):")
            if acc_type.lower() not in ['current', 'savings']:
                print("Please enter a valid account type")
        bal = float(input("Enter the amount you want to deposit:"))
        pin = 0
        rpin = 1
        while(pin!=rpin):
            pin = int(input("Enter your pin:"))
            rpin = int(input("Please re-enter your pin:"))
            if pin!=rpin:
                print("The pin didn't match")
        print(">------------------------------------------<")
        data = (new_acc_num,f_name,l_name,aadhar,dob,addr,acc_type,bal,pin,spl_sec_num,)
        if acc_type.lower() in ['current']:
            cursor.execute('INSERT INTO curr_accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (acc_num,f_name,l_name,aadhar,dob,addr,bal,pin,spl_sec_num,))
        elif acc_type.lower() in ['savings']:
            cursor.execute('INSERT INTO sav_accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (acc_num,f_name,l_name,aadhar,dob,addr,bal,pin,spl_sec_num,))
        cursor.execute('INSERT INTO Accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(data) )
        connection.commit()
        print(">------------------------------------------<")
        print("Your Account number is:{}".format(new_acc_num))
        print("Data Entered Successfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


def new_account_for_existing_customer(acc_num):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))', (acc_num,))
        result = cursor.fetchone()
        if result == None:
            print("The account doesn't exist")
            ans = input("Do you want create a new account(Y/N):")
            if ans.upper() == 'Y':
                new_account()
            else:
                return
        new_acc_num = random.randint(100000, 999999)
        f_name = result[1]
        l_name = result[2]
        aadhar = result[3]
        dob = result[4]
        addr = result[5]
        spl_sec_num = random.randint(10000, 99999)

        acc_type = ' '
        while acc_type.lower() not in ['current', 'savings']:
            acc_type = input("Enter your account type(Current/Savings):")
            if acc_type.lower() not in ['current', 'savings']:
                print("Please enter a valid account type")
        bal = float(input("Enter the amount you want to deposit:"))
        pin = 0
        rpin = 1
        while (pin != rpin):
            pin = int(input("Enter your pin:"))
            rpin = int(input("Please re-enter your pin:"))
            if pin != rpin:
                print("The pin didn't match")
        print(">------------------------------------------<")
        data = (new_acc_num, f_name, l_name, aadhar, dob, addr, acc_type, bal, pin, spl_sec_num,)
        if acc_type.lower() in ['current']:
            cursor.execute('INSERT INTO curr_accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (acc_num, f_name, l_name, aadhar, dob, addr, bal, pin, spl_sec_num,))
        elif acc_type.lower() in ['savings']:
            cursor.execute('INSERT INTO sav_accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (acc_num, f_name, l_name, aadhar, dob, addr, bal, pin, spl_sec_num,))
        cursor.execute('INSERT INTO Accounts Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (data))
        connection.commit()
        print(">------------------------------------------<")
        print("Your Account number is:{}".format(new_acc_num))
        print("Your Special Security Number is {}".format(spl_sec_num))
        print("Data Entered Successfully")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


def employee_check_customer_transaction_details():
    acc_num = int(input("Please Enter your Account number:"))

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))', (acc_num,))
        result = cursor.fetchone()
        if result == None:
            print('''Account number not found!!!
                Please Enter a valid Account number''')
            employee_check_customer_transaction_details()
            exit()
        spl_sec_pin = None
        while spl_sec_pin != result[9]:
            spl_sec_pin = int(input("Enter your special security pin:"))
            if spl_sec_pin == result[9]:
                cursor.execute('SELECT * FROM bankdb.transactions WHERE (Account_Nunber=(%s))', (acc_num,))
                transactions = cursor.fetchall()
                print("Date and Time , Transaction Type , Transaction Amount")
                print("-----------------------------------")
                for x in range(len(transactions)):
                    print(f"{transactions[x][1]} , {transactions[x][2]} , {transactions[x][3]} ")
                    print("-------------------------------------")
                new_spl_sec=spl_sec_pin
                while new_spl_sec==spl_sec_pin:
                    new_spl_sec = random.randint(10000,99999)
                cursor.execute("UPDATE bankdb.accounts SET Special_Security_Number=(%s) WHERE acc_num=(%s);",
                               (new_spl_sec, acc_num,))
                connection.commit()

            elif spl_sec_pin != result:
                print("Incorrect Pin entered!!!")
        print("Your New Special Security number is:{}".format(new_spl_sec))
        print(">-----------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)

def Customer_to_customer_transfer():
    acc_no_1 = int(input("Enter Customer Account number :"))
    time = datetime.now()
    transaction_type_1 = 'Credit'
    transaction_type_2 = 'Debit'

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))', (acc_no_1,))
        result1 = cursor.fetchone()
        spl_sec_pin = None
        while spl_sec_pin != result1[9]:
            spl_sec_pin = int(input("Enter your Special Security pin:"))
            if (spl_sec_pin != result1[9]):
                print("Incorrect Pin!!")

        acc_no_2 = int(input("Enter the reciver Account number:"))
        cursor.execute('SELECT * FROM bankdb.accounts WHERE (acc_num=(%s))', (acc_no_2,))
        result2 = cursor.fetchone()
        if result2:
            pass
        else:
            print("Incorrect Account number")
            print("Sorry!! Please Re-enter all the details")
            transfer()
        Amount = float(input("Enter the amount your want to transfer:"))
        bal1 = result1[7] - Amount
        bal2 = result2[7] + Amount
        cursor.execute("UPDATE bankdb.accounts SET balance=(%s) WHERE acc_num=(%s)"
                       , (bal1, acc_no_1,))
        cursor.execute("UPDATE bankdb.accounts SET balance=(%s) WHERE acc_num=(%s)"
                       , (bal2, acc_no_2,))
        cursor.execute("INSERT INTO bankdb.transactions Values (%s,%s,%s,%s)",
                       (acc_no_1, time, transaction_type_1, Amount,))
        cursor.execute("INSERT INTO bankdb.transactions Values (%s,%s,%s,%s)",
                       (acc_no_2, time, transaction_type_2, Amount,))
        print("The Amount is transffered!!")
        connection.commit()
        print(">----------------------------------------------<")
    except Exception as e:
        print("Data Entered wrongly")
        print(e)


def main():
    choice = 0
    while choice!=5:
        print('''                
                        WELCOME TO OUR BANK MANAGEMENT SYSTEM                   
                                
            1. Employee Login
            2. New Employee
            3. Customer Login        
            4. New Customer
            5. Exit
            
            ''')
        choice = int(input("Enter your choice:"))
        if choice==1:
            r = emp_login()
            while r==True:
                emp_choice = 0
                while emp_choice!=5:
                    print('''
                        1. Create New customer 
                        2. Customer Transaction detail
                        3. Customer to Customer to Transfer
                        4. Change Customer details
                        5. Exit
                            ''')
                    emp_choice = int(input("Enter your choice:"))
                    if emp_choice==1:
                        old_new = bool(input("Is the customer a present Account holder(T/F):"))
                        if old_new==True:
                            new_account_for_existing_customer_via_employee()
                        else:
                            new_account()
                    elif emp_choice==2:
                        employee_check_customer_transaction_details()
                    elif emp_choice == 3:
                        Customer_to_customer_transfer()
                    elif emp_choice == 4:
                        change_detail()
                    elif emp_choice == 5:
                        r=False
                    elif emp_choice not in [1,2,3,4,5]:
                        print("Please enter a valid choice")
                        
        elif choice == 2:
            new_employee()
        
        elif choice == 3:
            check = False
            acc_num = 0
            [check,acc_num] = customer_login()
            if check==True:
                customer_choice = 0
                while  customer_choice!=8:
                    print('''
                                Please choose one of the following:
                                ----------------------------------
                        1. Create a new Account
                        2. Show Transaction details
                        3. Transfer Money
                        4. Withdraw Money
                        5. Deposit Money
                        6. Change Account Details
                        7. Delete Account
                        8. Exit
                            ''')
                    customer_choice = int(input("Enter your choice:"))
                    if customer_choice == 1:
                        new_account_for_existing_customer(acc_num)
                    elif customer_choice == 2:
                        transaction_detials()
                    elif customer_choice == 3:
                        transfer()
                    elif customer_choice == 4: 
                        withdraw_money()
                    elif customer_choice == 5:
                        deposit_money()
                    elif customer_choice == 6:
                        change_detail()
                    elif customer_choice == 7:
                        delete()
                    elif customer_choice == 8:
                        print("THANK YOU")
                        check=False
                        print(">-----------------------------------------------<")
                    elif customer_choice not in [1,2,3,4,5,6,7,8]:
                        print("Please enter a valid choice")
                
        elif choice==4:
            new_account()
            
        elif choice == 5:
            print("THANK YOU!!!!!!!!!!")
            print(">---------------------------------------<")
            break

        else:
            print("Enter a valid choice!!!")
            
            
            
main()    


# In[ ]:




