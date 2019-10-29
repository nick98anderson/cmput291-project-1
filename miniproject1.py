import sqlite3
import sys
import random
from datetime import date
'''Resources for SQLite in python and implementing user logins
https://eclass.srv.ualberta.ca/pluginfile.php/5149362/mod_label/intro/SQLite-in-Python-1.pdf -- BEST
https://eclass.srv.ualberta.ca/mod/page/view.php?id=3659763 -- Assignment Spec
https://github.com/imilas/291PyLab -- BEST
https://eclass.srv.ualberta.ca/pluginfile.php/5149359/mod_label/intro/QL-eSQL.pdf?time=1567207038507 -- SQL inside applications slides'''

db = sys.argv[1]
conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON;')	
conn.commit()

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
        input_option = input("Selection option: ")
        option = int(input_option)

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


def register_birth(): #needs nbregplace, put baby in PERSONS first
    birthregno = random.randint(1,999) #Need to make this a UNIQUE number
    nbfname = input("Newborn's First Name: ")
    nblname = input("Newborn's Last Name: ")
    nbregdate = date.today() #Could use SQL datetime instead, not sure how this will convert
    #cursor.execute("SELECT city FROM users WHERE uid = ?", (username)) #Having trouble figuring out how to pass in username
    #nbregplace = cursor.fetchall()
    nbregplace = input("Newborn's birthplace: ") #needs to be 
    nbgender = input("Newborn's Gender (M/F): ") #https://stackoverflow.com/questions/8761778/limiting-python-input-strings-to-certain-characters-and-lengths
    nbf_fname = input("Newborn's Father's First Name: ")
    nbf_lname = input("Newborn's Father's Last Name: ")
    nbm_fname = input("Newborn's Mother's First Name: ")
    nbm_lname = input("Newborn's Mother's Last Name: ")

    cursor.execute("SELECT fname, lname FROM persons WHERE ? = fname AND ? = lname", (nbm_fname, nbm_lname))
    nbmother = cursor.fetchall()
    cursor.execute("SELECT fname, lname FROM persons WHERE ? = fname AND ? = lname", (nbf_fname, nbf_lname))
    nbfather = cursor.fetchall()

    while nbmother == []:
    	nbm_fname = input("Confirm Mother's first name: ") # Need to make sure this isn't null
    	nbm_lname = input("Confirm Mother's last name: ") # Need to make sure this isn't null
    	motherbdate = input("What is the Mother's birth date? (YYYY-MM-DD): ")
    	motherbplace = input("What is the Mother's birth place? (format): ")
    	motheraddress = input("What is the Mother's address? (format): ")
    	motherphone = input("What is the Mother's phone number?: (###-###-####)")
    	mother_data = (motherfname,motherlname,motherbdate,motherbplace,motheraddress,motherphone)
    	cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", mother_data)
    	conn.commit()
    	break

    while nbfather == []:
    	nbf_fname = input("Confirm Father's first name: ") # Need to make sure this isn't null
    	nbf_lname = input("Confirm Father's last name: ") # Need to make sure this isn't null
    	fatherbdate = input("What is the Father's birth date? (YYYY-MM-DD): ")
    	fatherbplace = input("What is the Father's birth place?: ")
    	fatheraddress = input("What is the Father's address?: ")
    	fatherphone = input("What is the Father's phone number? (###-###-####): ")
    	father_data = (fatherfname,fatherlname,fatherbdate,fatherbplace,fatheraddress,fatherphone)
    	cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", father_data)
    	conn.commit()
    	break

    cursor.execute("SELECT address FROM persons WHERE ? = fname AND ? = lname", (nbm_fname, nbm_lname)) #Finds mother's address
    nbaddress = cursor.fetchall()
    cursor.execute("SELECT phone FROM persons WHERE ? = fname AND ? = lname", (nbm_fname, nbm_lname)) #Finds mother's phone number
    nbphone = cursor.fetchall()

    baby_data = (birthregno,nbfname,nblname,nbregdate,nbregplace,nbgender,nbf_fname,nbf_lname,nbm_fname,nbm_lname)
    person_data = (nbfname, nblname, nbregdate, nbregplace, str(nbaddress), str(nbphone))
    cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", person_data) #First we register the baby as a person
    conn.commit()
    cursor.execute("INSERT INTO births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname) VALUES (?,?,?,?,?,?,?,?,?,?)", baby_data) #We then register it as a birth
    conn.commit()
    print("Registration Complete! Returning to Agent Options")
    
    
    

def register_marriage():
    marriageno = random.randint(1,999) #Need to make this a UNIQUE number
    marriagedate = date.today() #Could use SQL datetime instead, not sure how this will convert
    marriageplace = input("Where is the couple getting married?: ") #THIS needs to be the user's city again
    p1fname = input("What is partner 1's first name?: ")
    p1lname = input("What is partner 1's last name?: ")
    p2fname = input("What is partner 2's first name?: ")
    p2lname = input("What is partner 2's last name?: ")

    cursor.execute("SELECT fname, lname FROM persons WHERE ? = fname AND ? = lname", (p1fname, p1lname))
    partner1 = cursor.fetchall()
    cursor.execute("SELECT fname, lname FROM persons WHERE ? = fname AND ? = lname", (p2fname, p2lname))
    partner2 = cursor.fetchall()

    while partner1 == []:
    	p1fname = input("Confirm Partner 1's first name: ") # Need to make sure this isn't null
    	p1lname = input("Confirm Partner 1's last name: ") # Need to make sure this isn't null
    	partner1bdate = input("What is Partner 1's birth date? (YYYY-MM-DD): ")
    	partner1bplace = input("What is the Partner 1's birth place? (format): ")
    	partner1address = input("What is the Partner 1's address? (format): ")
    	partner1phone = input("What is the Partner 1's phone number?: (###-###-####)")
    	partner1_data = (p1fname,p1lname,partner1bdate,partner1bplace,partner1address,partner1phone)
    	cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", partner1_data)
    	conn.commit()
    	break

    while partner2 == []:
    	p2fname = input("Confirm Partner 2's first name: ") # Need to make sure this isn't null
    	p2lname = input("Confirm Partner 2's last name: ") # Need to make sure this isn't null
    	partner2bdate = input("What is the Partner 2's birth date? (YYYY-MM-DD): ")
    	partner2bplace = input("What is the Partner 2's birth place?: ")
    	partner2address = input("What is the Partner 2's address?: ")
    	partner2phone = input("What is the Partner 2's phone number? (###-###-####): ")
    	partner2_data = (p2fname,p2lname,partner2bdate,partner2bplace,partner2address,partner2phone)
    	cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", partner2_data)
    	conn.commit()
    	break

    marriage_data = (marriageno,marriagedate,marriageplace,p1fname,p1lname,p2fname,p2lname)
    cursor.execute("INSERT INTO marriages(regno,regdate,regplace,p1_fname,p1_lname,p2_fname,p2_lname) VALUES (?,?,?,?,?,?,?)", marriage_data)
    conn.commit()


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


