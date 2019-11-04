import sqlite3
import sys
import datetime
from random import randrange


'''Resources for SQLite in python and implementing user logins
https://eclass.srv.ualberta.ca/pluginfile.php/5149362/mod_label/intro/SQLite-in-Python-1.pdf -- BEST
https://eclass.srv.ualberta.ca/mod/page/view.php?id=3659763 -- Assignment Spec
https://github.com/imilas/291PyLab -- BEST
https://eclass.srv.ualberta.ca/pluginfile.php/5149359/mod_label/intro/QL-eSQL.pdf?time=1567207038507 -- SQL inside applications slides'''

db = sys.argv[1]
conn = sqlite3.connect(db)
cursor = conn.cursor()

def double_quote(word):
    return "'%s'" % word

def main():
    print("***WELCOME****")
    user = login()
    

    if user[0][0] == 'a':
        agent_prompt(str(user[0][1]))

    elif user[0][0] == 'o':
        officer_prompt()
    else:
        print(user[0][0])
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
    username = raw_input("User ID: ")
    pwd = raw_input("Password: ")
    cursor.execute("SELECT utype, city FROM users WHERE uid = ? AND pwd = ?", (username, pwd))
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
            logout()
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
            logout()
        else:
            print("****ERROR***** invalid option please try again")
            display_agent_options()

            
def display_agent_options(city):
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
    print("Loging out....")
    main()


#Todo-> Check for valid date, string matching
def issue_ticket():
    
    while True:
        regno = int(input("Enter a registration number: "))
        cursor.execute("SELECT regno, vin, fname, lname FROM registrations WHERE regno = ?;", (regno,))
        regInfo = cursor.fetchall()
        conn.commit()

        if regInfo == []:
            option = raw_input('Registration number not found would you like to try again (y/n): ')
            if option == 'n':
                return 
        elif regInfo[0][0] == regno:
            break
    
    vin = regInfo[0][1]
    fname = regInfo[0][2]
    lname = regInfo[0][3]

    cursor.execute("SELECT make, model, year, color FROM vehicles WHERE vin = ?;",(vin,))
    vehicleInfo = cursor.fetchall()
    conn.commit()

    make = vehicleInfo[0][0]
    model = vehicleInfo[0][1]
    year = vehicleInfo[0][2]
    color = vehicleInfo[0][3]
    
    print("\n***Vehicle Info***")
    print("Make: " + str(make))
    print("Model: " + str(model))
    print("Year: " + str(year))
    print("Color: " + str(color))

    while True:
        vDate = raw_input('Enter violation date (YYYY-MM-DD)')
        vText = raw_input('Enter violation text: ')
        fineAmount = raw_input(('Enter fine amount: '))

        if fineAmount.isdigit() == False:
            print('ERROR, Invalid fine value entered please try again')
        
        if vDate == '':
            vDate = datetime.datetime.now().strftime("%Y-%m-%d")

        if vText == '':
            vText = None

        else:
            break
    
    tno = randrange(1000000000)

    while True:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM tickets WHERE tno=?)", (tno,))
        temp = cursor.fetchall()
        if int(temp[0][0]) == 1:
            tno = randrange(1000000000)
        else:
            conn.commit()
            break

    
    cursor.execute("insert into tickets values(?,?,?,?,?)", (tno,regno,fineAmount,vText,vDate))
    conn.commit()


def find_car_owner():
    selectQuery = "SELECT v.make, v.model, v.year, v.color, r.plate, regdate, expiry, fname, lname FROM vehicles v LEFT JOIN registrations r ON r.vin = v.vin WHERE "
    carDetails = ['make', 'model', 'year', 'color', 'plate']
    userSelections = []
    userValues = []

    for i in range(0, len(carDetails)):
        temp = raw_input("Enter "+carDetails[i] + " (Optional): ")
        if temp != '':
            userValues.append(temp)
            userSelections.append(carDetails[i])

    if len(userValues) == 0:
        print("ERROR, you must enter at least one of the fields")
        return

    for i in range(0, len(userSelections)):
        if i == len(userSelections) - 1:
            if userSelections[i] == 'year':
                selectQuery += 'v.'+ userSelections[i] + '=' + userValues[i]
            elif userSelections[i] == 'plate':
                selectQuery += 'r.'+userSelections[i] + '=' + double_quote(userValues[i])
            else:
                selectQuery += 'v.' + userSelections[i] + ' LIKE ' + double_quote(userValues[i])
        else:
            if userSelections[i] == 'year':
                selectQuery += 'v.'+ userSelections[i] + '=' + userValues[i] + ' AND '
            elif userSelections[i] == 'plate':
                selectQuery += 'r.'+userSelections[i] + '=' + double_quote(userValues[i]) + ' AND '
            else:
                selectQuery += 'v.' + userSelections[i] + ' LIKE ' + double_quote(userValues[i]) + ' AND '
    
    selectQuery += " GROUP BY v.vin"

    cursor.execute(selectQuery)
    fetched = cursor.fetchall()


    if len(fetched) == 0:
        print('No results found')

    elif len(fetched) >= 4:
        formated_row = '{:<10} {:>6} {:>6} {:>6} {:^10}' 
        i = 1
        for row in fetched:
            if i == 1:
                print("    "+formated_row.format("Make", "Model", "Year", "Color", "Plate"))
            
            print(str(i)+ "   " + formated_row.format(row[0], row[1], row[2], row[3], row[4]))
            i = i + 1

        selectionRow = int(raw_input("Select row from vehicles for more information: "))

        while selectionRow < 1 or selectionRow > len(fetched):
            print("ERROR, invalid selection please try again")
            selectionRow = int(raw_input("Select row from vehicles for more information: "))
        
        selection = fetched[selectionRow-1]

        make = str(selection[0])
        model = str(selection[1])
        year = str(selection[2])
        color = str(selection[3])
        plate = str(selection[4])
        formated_row = '{:<10} {:^10} {:^10} {:^10} {:^10} {:^15} {:^15} {:^15} {:^15}'

        if plate == "None":
            print(formated_row.format("Make", "Model", "Year", "Color", "Plate","Regdate","Expiry Date","First name", "Last name"))
            print(formated_row.format(make, model, year, color, plate, "None", "None", "None", "None"))

        else:
            selectQuery = """SELECT v.make, v.model, v.year, v.color, r.plate, r.regdate, r.expiry, r.fname, r.lname FROM vehicles v 
            LEFT JOIN registrations r ON v.vin = r.vin WHERE v.make like ? AND v.model like ? AND v.year = ? AND v.color LIKE ? AND r.plate = ?
            ORDER BY r.regdate DESC LIMIT 1"""
            cursor.execute(selectQuery, (make, model, year, color, plate))
            fetched = cursor.fetchall() 
            print(formated_row.format("Make", "Model", "Year", "Color", "Plate","Regdate","Expiry Date","First name", "Last name"))
            for row in fetched:
                print(formated_row.format(*row))

    else:
        formated_row = '{:<10} {:^10} {:^10} {:^10} {:^10} {:^15} {:^15} {:^15} {:^15}'
        selectQuery += "AND r.regdate = (SELECT MAX(regdate) FROM registrations WHERE vin = v.vin)"
        print(selectQuery)
        print(formated_row.format("Make", "Model", "Year", "Color", "Plate","Regdate","Expiry Date","First name", "Last name"))
        for row in fetched:
            print(formated_row.format(*row))


    conn.commit()


main()

conn.close()



