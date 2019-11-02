import sqlite3
import sys
import random
from datetime import datetime, timedelta, date
'''Resources for SQLite in python and implementing user logins
https://eclass.srv.ualberta.ca/pluginfile.php/5149362/mod_label/intro/SQLite-in-Python-1.pdf -- BEST
https://eclass.srv.ualberta.ca/mod/page/view.php?id=3659763 -- Assignment Spec
https://github.com/imilas/291PyLab -- BEST
https://eclass.srv.ualberta.ca/pluginfile.php/5149359/mod_label/intro/QL-eSQL.pdf?time=1567207038507 -- SQL inside applications slides
https://stackoverflow.com/questions/973541/how-to-set-sqlite3-to-be-case-insensitive-when-string-comparing -- Case sensitive for SQL'''

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
	'''The agent should be able to register a birth by providing the first name, the last name, the gender, the birth date, the birth place of the newborn, 
	as well as the first and last names of the parents. The registration date is set to the day of registration (today's date) and the registration place is set to the city of the user. 
	The system should automatically assign a unique registration number to the birth record. The address and the phone of the newborn are set to those of the mother. If any of the parents is not in the database, 
	the system should get information about the parent including first name, last name, birth date, birth place, address and phone. For each parent, any column other than the first name and last name can be null if it is not provided.'''
    birthregno = random.randint(1,999) #Need to make this a UNIQUE number
    nbfname = input("Newborn's First Name: ")
    nblname = input("Newborn's Last Name: ")
    nbregdate = date.strftime("%Y-%m-%d") #Could use SQL datetime instead, not sure how this will convert
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
	'''The user should be able to provide the names of the partners and the system should assign the registration date and place and a unique registration number as discussed in registering a birth. 
	If any of the partners is not found in the database, the system should get information about the partner including first name, last name, birth date, birth place, address and phone. 
	For each partner, any column other than the first name and last name can be null if it is not provided.'''
    marriageno = random.randint(1,999) #Need to make this a UNIQUE number
    marriagedate = date.strftime("%Y-%m-%d") #Could use SQL datetime instead, not sure how this will convert
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
	'''The user should be able to provide an existing registration number and renew the registration. 
	The system should set the new expiry date to one year from today's date if the current registration either has expired or expires today. 
	Otherwise, the system should set the new expiry to one year after the current expiry date.'''
    vehicleregno = input("Enter the vehicle's registration number: ")
    cursor.execute("SELECT regdate FROM registrations WHERE ? = regno", (vehicleregno))
    rawexpiry = cursor.fetchall()
    currentexpiry = datetime.strptime(rawexpiry, "%Y-%m-%d")
    todays_date = date.strftime("%Y-%m-%d")

    if currentexpiry <= todays_date:
    	newexpiry = currentexpiry.replace(todays_date.year + 1)

	else:
		newexpiry = currentexpiry.replace(currentexpiry.year + 1)


def process_bill_of_sale():
	'''The user should be able to record a bill of sale by providing the vin of a car, the name of the current owner, the name of the new owner, and a plate number for the new registration. 
	If the name of the current owner (that is provided) does not match the name of the most recent owner of the car in the system, the transfer cannot be made. 
	When the transfer can be made, the expiry date of the current registration is set to today's date and a 
	new registration under the new owner's name is recorded with the registration date and the expiry date set by the system to today's date and a year after today's date respectively. 
	Also a unique registration number should be assigned by the system to the new registration. The vin will be copied from the current registration to the new one.'''
    entered_vin = input("What is the VIN of the vehicle that is to be sold?: ")
    current_owner_fname = input("What is the first name of the vehicle's current owner?: ")
    current_owner_lname = input("What is the last name of the vehicle's current owner?: ")
    new_owner = input("What is the name of the new owner?: ")
    entered_plate = input("What is the requested new license plate number?: ")

    cursor.execute("SELECT r.fname, r.lname FROM registrations r WHERE ? = r.vin AND ? = r.fname AND ? = r.lname AND regdate = (SELECT max(r2.regdate) FROM registrations r2 WHERE r.fname = r2.fname AND r.lname = r2.lname AND r.vin = r2.vin)", (current_owner_fname, current_owner_lname, entered_vin))
    latest_owner = cursor.fetchall() #Need to heavily test this query, mostly for case sensitivity


    if latest_owner == []:
    	print("This person does not exist in the database. Exiting.")
    	display_agent_options()

    elif (latest_owner[0].lower() != current_owner_fname.lower()) OR (latest_owner[1].lower() != current_owner_fname.lower()):
    	print("The name you have entered is not the latest owner of this vehicle. Exiting.")
    	display_agent_options()

    else: 
    	current_expiry = date.strftime("%Y-%m-%d")
    	cursor.execute("UPDATE registrations SET ? = expiry WHERE ? = vin", (current_expiry, entered_vin))
    	new_registration_date = date.strftime("%Y-%m-%d")
    	new_expiry_date = current_expiry.replace(current_expiry.year + 1)
    	unique_registration_number = random.randint(1,999) #Need to make this a UNIQUE number
    	new_owner_data = (unique_registration_number, new_registration_date, new_expiry_date, entered_plate, entered_vin, current_owner_fname, current_owner_lname)
    	cursor.execute("INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?,?,?,?,?,?,?)", new_owner_data)
    	conn.commit()





def process_payment(): #might need to worry about floats
	'''The user should be able to record a payment by entering a valid ticket number and an amount. 
	The payment date is automatically set to the day of the payment (today's date). 
	A ticket can be paid in multiple payments but the sum of those payments cannot exceed the fine amount of the ticket.'''
    ticketnumber = input("Enter the ticket number: ")
    paymentamount = input("Enter the payment amount: ")
    paymentdate = date.strftime("%Y-%m-%d")

    cursor.execute("SELECT fine FROM tickets WHERE ? = tno", (ticketnumber))
    fine_amount = cursor.fetchall()
    if paymentamount > fine_amount:
    	paymentamount = fine_amount
    	print("You have overpaid this ticket. The true amount paid was $" + str(paymentamount))
    	fine_amount = fine_amount - paymentamount
    	cursor.execute("UPDATE tickets SET ? = fine WHERE ? = tno", (fine_amount, ticketnumber))
    	conn.commit()
    else:
    	fine_amount = fine_amount - paymentamount
    	print("Ticket paid for $" + str(paymentamount))
    	cursor.execute("UPDATE tickets SET ? = fine WHERE ? = tno", (fine_amount, ticketnumber))
    	conn.commit()

    payment_data = (ticketnumber, paymentdate, paymentamount)
    cursor.execute("INSERT INTO payments(tno, pdate, amount) VALUES (?,?,?)", payment_data)
    conn.commit()


def get_driver_abstract(): #No idea if this works or not. The last constraint about 5 or more tickets definitely is not implemented yet. Need to test how the for loop is going to work for fetching all the columns. Maybe abstract_info[i] in the loop?
	#The user should be able to enter a first name and a last name and get a driver abstract, which includes number of tickets, the number of demerit notices, the total number of demerit points received both within the past two years and within the lifetime. 
	#The user should be given the option to see the tickets ordered from the latest to the oldest. For each ticket, you will report the ticket number, 
	#the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
	#If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
    abstract_fname = input("What is the driver's first name?: ")
    abstract_lname = input("What is the driver's last name?: ")
    cursor.execute("SELECT regno FROM registrations WHERE ? = fname AND ? = lname", (abstract_fname, abstract_lname))
    abstract_regno = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE ? = regno", (abstract_regno))
    number_of_tickets = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM demeritNotices WHERE ? = fname AND ? = lname", (abstract_fname, abstract_lname))
    number_of_demeritNotices = cursor.fetchall()

    cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE ? = fname AND ? = lname AND ddate >= date('now', '-2 years')", (abstract_fname, abstract_lname))
    recent_number_demerits = cursor.fetchall()

    cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE ? = fname AND ? = lname", (abstract_fname, abstract_lname))
    total_number_demerits = cursor.fetchall()

    optional_order = input("Would you like to see the tickets in order of latest to oldest? (Y/N): ")

    while (optional_order.lower() != "y") OR (optional_order.lower() != "n"):
    	optional_order = input("Incorrect response. Would you like to see the tickets in order of latest to oldest? (Y/N): ")
    	break

    if optional_order.lower() == "y":
    	for i in abstract_regno:  #not sure how this will work
			cursor.execute("SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t LEFT OUTER JOIN registrations r ON r.regno = t.regno LEFT OUTER JOIN vehicles v on v.vin = r.vin WHERE ? = t.regno ORDER BY t.vdate DESC", (abstract_regno[i]))
			abstract_info = cursor.fetchall() #might need to move this out of the for loop
			print(abstract_info)

    elif optional_order.lower() == "n":
    	for i in abstract_regno:  #not sure how this will work
			cursor.execute("SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t LEFT OUTER JOIN registrations r ON r.regno = t.regno LEFT OUTER JOIN vehicles v on v.vin = r.vin WHERE ? = t.regno", (abstract_regno[i]))
			abstract_info = cursor.fetchall() #might need to move this out of the for loop
			print(abstract_info)






def logout():
    pass

def issue_ticket():
    pass

def find_car_owner():
    pass


main()

	
conn.close()


