import sqlite3
import sys

#Driver function
def main():
    loadDB()


#Loads database file as command line argument
def loadDB():
    db = sys.argv[1]
    conn = sqlite3.connect(db)


def login():
    return

def authenticateUser():
    return


main()









