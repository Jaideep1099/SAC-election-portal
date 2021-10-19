import random
import hashlib
import pandas as pd

def enroll_voter(voterList, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM USER WHERE ROLLNO != 'admin';")

    passwordList = []
    for voter in voterList:
        pwd = str(random.randint(10000000, 99999999))
        # p_rint(pwd)
        passwordList.append([voter[1],pwd])

        hashed_pwd = hashlib.sha512(pwd.encode()).hexdigest()
        cursor.execute("INSERT INTO USER (ROLLNO, EMAIL, PWD) VALUES (%s,%s,%s)",(voter[0],voter[1], hashed_pwd))
    
    conn.commit()

    pwdFile = pd.DataFrame(passwordList)
    pwdFile.to_excel('pwdFile.xlsx')


def enroll_candidate(candidateList, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CANDIDATES")

    for candidate in candidateList:
        cursor.execute("INSERT INTO CANDIDATES (ROLLNO, NAME, DEPT, PROG, POSITION) VALUES (%s,%s,%s,%s,%s)",(candidate[0], candidate[1], candidate[2], candidate[3], candidate[4]))
    
    conn.commit()
