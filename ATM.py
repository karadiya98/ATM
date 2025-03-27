import random
import mysql.connector as connector
database = connector.connect(host="localhost", username="root", password="ali@786",database="atm")

# global variables 
total=0
deposit=0
withdraw=0

def login_signin():
    print("\n\t\t ATM MACHINE\n")
    print("\t1) login\n\t2) signin\n")
    choice = int(input("\tenter your choice :-"))
    if choice == 1:
        print("\n\t\t>> LOGIN\n")
        username1 = input("\tenter your username: ")
        password1 = input("\tenter your password: ")
        s = database.cursor()
        select1 = "SELECT username, password FROM t1"
        s.execute(select1)
        result = s.fetchall()
        user_found = False  
        for i in result:
            if username1 == i[0] and password1 == i[1]:
                print("\n\t\t\tLogin successful!\n")
                user_found = True
                break
        if not user_found:
            print("Invalid credentials. Username or password do not match.")

    elif choice == 2:
        print("\n\t\t>> CREATE ACCOUNT\n")
        id1 = int(input("\t\tenter your id: "))
        username1 = input("\t\tcreate your username: ")
        password1 = input("\t\tcreate your password: ")
        name1 = input("\t\ttype your name: ")
        branch1 = input("\t\tEnter your branch: ")
        # Check if username already exists
        obj = database.cursor()
        check_username = "SELECT username FROM t1 WHERE username = %s"
        obj.execute(check_username, (username1,))
        result = obj.fetchall()
        if result:
            print("\t\tUsername already exists! Please choose another one.")
        else:
            total = int(input("\t\tYou need to deposit 5000 for further processing... :- "))
            while total != 5000:
              print("\t\t\t\tIncorrect amount. Please deposit 5000 to continue.\n ")
              total = int(input("\t\t\t\tYou need to deposit 5000 for further processing... :- "))
            print("\n\t\t\t\tDeposit successful! You can now proceed further")
            deposit=total
            random_checkbkNO = random.randint(20000,30000)     
            insert = "INSERT INTO t1 (id, name, branch, username, password,total,deposit,checkbook_no) VALUES (%s, %s, %s, %s, %s, %s , %s,%s)"
            value = (id1, name1, branch1, username1, password1,total,deposit,random_checkbkNO)
            obj.execute(insert, value)
            database.commit()
            print("\n\t\t\tAccount created successfully!\n")
            print("\t\tyour checkbook number is :-",random_checkbkNO)
    print("---------------------------------------------------------------------------------------------")
          
def depositfn():
    print("\n\t\t\t>> DEPOSIT\n") 
    # Get deposit amount and checkbook number from user input
    deposit = float(input("\t\t enter amount to deposit :- "))
    check = input("\t\t required Checbook_N0 :- ")
    # Retrieve the current total for the given checkbook number
    obj = database.cursor()
    get_checkbk = "SELECT total FROM t1 WHERE checkbook_no = %s"
    obj.execute(get_checkbk, (check,))
    result = obj.fetchone()
    # Check if a record was found
    if result is None:
        print("\t\t No record found for the given checkbook number.")
        return
    # Calculate new total
    old_total = result[0]
    total = old_total + deposit  # Add deposit to the old total  
    # Update the total in t1 table
    update_query = "UPDATE t1 SET total=%s WHERE checkbook_no=%s"
    obj.execute(update_query, (total, check))
    # Update the deposit table
    update_query = "UPDATE t1 SET deposit=%s WHERE checkbook_no=%s"
    obj.execute(update_query, (deposit, check))
    print("\n\t\t\t\t CASH IS DEPOSITED SUCCESFULLY\n")
    # Commit the transaction
    database.commit()
    print("---------------------------------------------------------------------------------------------")


def withdrawfn():
    print("\n\t\t\t>> WITHDRAW\n")
   # Get deposit amount and checkbook number from user input
    withdraw = float(input("\t\t enter amount to withdraw :- "))
    check = input("\t\t required Checbook_N0 :- ")
   # Retrieve the current total for the given checkbook number
    obj = database.cursor()
    get_checkbk = "SELECT total FROM t1 WHERE checkbook_no = %s"
    obj.execute(get_checkbk, (check,))
    result = obj.fetchone()
    # Check if a record was found
    if result is None:
        print("\t\t No record found for the given checkbook number.")
        return
    # Calculate new total
    old_total = result[0]
    total = old_total-withdraw  # sub withdraw to the old total
    if withdraw<=total:
        # Update the total in t1 table
        update_query = "UPDATE t1 SET total=%s WHERE checkbook_no=%s"
        obj.execute(update_query, (total, check))
        # Update the deposit table
        update_query = "UPDATE t1 SET withdraw=%s WHERE checkbook_no=%s"
        obj.execute(update_query, (withdraw, check))
        print("\n\t\t\t\t CASH IS WITHDRAWED SUCCESFULLY\n")
        # Commit the transaction
        database.commit()
    else:
        print("\t\twithdraw amount is more than your balance")   
    print("---------------------------------------------------------------------------------------------")     

def status():
     print("\n\t\t\t>> YOUR STATUS \n")
     # to show status we need their checbookpass_No
     check = input("\t\t FIRST enter your Checbook_N0 :- ")
     if check is None:
        print("\t\t No record found for the given checkbook number.")
        return
     obj = database.cursor()
     get_checkbk = "SELECT * FROM t1 WHERE checkbook_no = %s"
     obj.execute(get_checkbk, (check,))
     result = obj.fetchall()
     print(result)
     print("---------------------------------------------------------------------------------------------")

def logout():
    print("\n\t\t\t>> LOGOUT PROCESS.. \n")
    check = input("\t\t FIRST enter your Checbook_No :- ")
    if check is None or check.strip() == "":
        print("\t\t No record found for the given checkbook number.")
        return
    obj = database.cursor()
    get_checkbk = "delete FROM t1 WHERE checkbook_no = %s"
    obj.execute(get_checkbk, (check,))
    # Check if any rows were affected (deleted)
    if obj.rowcount > 0:
        print("\t\t !! YOUR ACCOUNT IS CANCELLED !!")
    else:
        print("\t\t No record found for the given checkbook number.")
    database.commit()    
    print("---------------------------------------------------------------------------------------------")





def menu():
    print("---------------------------------------------------------------------------------------------")
    print("\n\t\t\t*** ATM MACHINE ***\n")
    print("\t\t\t1) open account\n\t\t\t2) deposit\n\t\t\t3) withdraw\n\t\t\t4) status\n\t\t\t5) logout\n\t\t\t6) profile\n\t\t\t7) HISTORY\n\t\t\t8) exit")
    print("---------------------------------------------------------------------------------------------")

def switch_case(option):
    if option == 1:
        login_signin()  # Call the login_signin function
    elif option == 2:
        depositfn()  # Call the deposit function
    elif option == 3:
        withdrawfn()  # Call the withdraw function
    elif option == 4:
        status()  # Call the status function
    elif option == 5:
        logout()  # Call the logout function
    elif option == 8:
        print("Thank you for visiting the ATM machine!")
        exit()  # Exit the program if user chooses 8
    else:
        print("Invalid option selected!")


# Main function to control the ATM flow
if __name__ == "__main__":
    choice = 0
    while choice != 8:
        menu()  # Display menu
        choice = int(input("\nENTER YOUR CHOICE :- "))
        switch_case(choice)  # Execute the selected option
        if choice != 8:  # Ask if the user wants to continue unless they've chosen option 8 to exit
            continue_choice = int(input("\n\t\tWANT TO CONTINUE? YES=1 & NO=0 :- "))
            print("\n")
            if continue_choice == 0:
                print("**************************************************************************")
                print("\n\t\t\tThank you for visiting the ATM machine!\n")
                print("**************************************************************************")
                break  # Exit the loop and end the program



