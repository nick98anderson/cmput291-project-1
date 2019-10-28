import sqlite3
import sys
'''Resources for SQLite in python and implementing user logins
https://eclass.srv.ualberta.ca/pluginfile.php/5149362/mod_label/intro/SQLite-in-Python-1.pdf -- BEST
https://eclass.srv.ualberta.ca/mod/page/view.php?id=3659763 -- Assignment Spec
https://github.com/imilas/291PyLab -- BEST
https://eclass.srv.ualberta.ca/pluginfile.php/5149359/mod_label/intro/QL-eSQL.pdf?time=1567207038507 -- SQL inside applications slides'''

db = sys.argv[1]
conn = sqlite3.connect(db)
cursor = conn.cursor()

def main():
    userType = login()
    

    if userType[0][0] == 'a':
        agent_prompt()

    elif userType[0][0] == 'o':
        officer_prompt()
    else:
        print(userType[0][0])
        print("error")


def login():
    isUser = False
    while isUser == False:
        user = getUser()
        if len(user) != 0:
            isUser = True
        else:
            print("Invalid user id or password, please try again")
    return user 


def getUser():
    username = input("User ID: ")
    pwd = input("Password: ")
    cursor.execute("SELECT utype FROM users WHERE uid = ? AND pwd = ?", (username, pwd))
    user = cursor.fetchall()
    return user

def officer_prompt():
    display_officer_options()

    while True:
        option = input("Select option: ")

        if option == 0:
            issue_ticket()
            display_officer_options()
        elif option == 1:
            find_car_owner()
            display_officer_options()
        elif option == 2:
            break
        else:
            print("****ERROR***** invalid option please try again")
            display_officer_options()


def agent_prompt():

    display_agent_options()

    while True:
        option = input("Selection option: ")

        if option == 0:
            register_birth()
            display_agent_options()
        elif option == 1:
            register_marriage()
            display_agent_options()
        elif option == 2:
            renew_vehicle_Reg()
            display_agent_options()
        elif option == 3:
            process_bill_of_sale()
            display_agent_options()
        elif option == 4:
            process_payment()
            display_agent_options()
        elif option == 5:
            get_driver_abstract()
            display_agent_options()
        elif option == 6:
            break
            #logout()
        else:
            print("****ERROR***** invalid option please try again")
            display_agent_options()

            
def display_agent_options():
    print("****Options****")
    print("Register birth (press 0)")
    print("Register Marriage (press 1)")
    print("Renew Vehicle Registration (press 2)")
    print("Process Bill of Sale (press 3)")
    print("Process Payment (press 4)")
    print("Get Driver Abstract (press 5)")
    print("Logout (press 6)")


def display_officer_options():
    print("****Options****")
    print("Issue a Ticket (press 0)")
    print("Find Car Owner (press 1)")
    print("Logout (press 2)")


def register_birth():
    pass

def register_marriage():
    pass

def renew_vehicle_Reg():
    pass

def process_bill_of_sale():
    pass

def process_payment():
    pass

def get_driver_abstract():
    pass

def logout():
    pass

def issue_ticket():
    pass

def find_car_owner():
    pass


main()

conn.close()


