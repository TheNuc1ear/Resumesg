import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = con.cursor()
myuserid = 657483952
myusername = 'AlvinJ_007'


def CREATETABLE():
    print("Creating now")
    cur.execute('''CREATE TABLE TGMUSERS
      (USERID TEXT PRIMARY KEY     NOT NULL,
      USERNAME           TEXT    NOT NULL,
      FIRSTNAME            TEXT,
      REFERRALCODE        TEXT,
      REFERRORID        TEXT,  
      NOOFREF        INT);''')
    print("Table created successfully")
    con.commit()
    con.close()


def NEWENTRY(a, b, c, d, e, f):
    cur.execute('INSERT INTO TGMUSERS (USERID, USERNAME, FIRSTNAME, REFERRALCODE, REFERRORID, NOOFREF) VALUES (%s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f))
    con.commit()
    print("Values inserted")


def UPDATE_NOOFREF(userid):
    num = GETNOOFREF(userid)
    num = int(num[0])
    num += 1
    cur.execute(
        'UPDATE TGMUSERS set NOOFREF = %s where USERID = %s', (num, userid,))
    con.commit()
    print("Value updated")


def VIEWENTRIES():
    cur.execute(
        'SELECT USERID, USERNAME, FIRSTNAME, REFERRALCODE, NOOFREF from TGMUSERS')
    rows = cur.fetchall()
    for row in rows:
        print("Userid = ", row[0])
        print("Username = ", row[1])
        print("First Name = ", row[2])
        print("Referral Code = ", row[3])
        print("NOOFREF = ", row[4])
        main()


def CLEARME():
    cur.execute('DELETE FROM TGMUSERS WHERE USERNAME = %s;', (myusername,))
    con.commit()
    print("deleted")
    main()


def DESTROYTABLE():
    cur.execute('TRUNCATE TABLE TGMUSERS;')
    con.commit()
    print("Table Cleared")
    main()


def GETREFERRER(a):
    cur.execute('SELECT USERNAME FROM TGMUSERS WHERE USERID = %s', (a,))
    rows = cur.fetchall()
    return rows[0]


def GETNOOFREF(a):
    cur.execute('SELECT NOOFREF FROM TGMUSERS WHERE USERID = %s', (a,))
    rows = cur.fetchall()
    return rows[0]


def main():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    print("\n\n****MANUAL MENU****\n1)Create Table\n2)New Entry\n3)Update No. of Referrals\n4)View Entries\n5)Clear Me\n6)Destroy Table\n")
    option = input("Enter your choice: ")
    if option == '1':
        CREATETABLE()
    elif option == '2':
        NEWENTRY()
    elif option == '3':
        UPDATE_NOOFREF()
    elif option == '4':
        VIEWENTRIES()
    elif option == '5':
        CLEARME()
    elif option == '6':
        DESTROYTABLE()
#main()
