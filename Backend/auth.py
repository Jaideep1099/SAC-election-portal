def authenticate_user(cursor, uname, token):
    
    cursor.execute("SELECT COUNT(*) FROM SESSION WHERE ROLLNO=%s AND TOKEN=%s", (uname, token))
    res = cursor.fetchone()
    # p_rint(res) 
    
    return res[0]==1