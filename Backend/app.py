import random
import pandas as pd
import numpy as np
import json
from flask import Flask, request, render_template, Response
from flask_cors import CORS
from flaskext.mysql import MySQL

from config import *
from enroll import *
from auth import *

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = db_config['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db_config['password']
app.config['MYSQL_DATABASE_DB'] = db_config['dbname']
app.config['MYSQL_DATABASE_HOST'] = db_config['host']
mysql.init_app(app)

cors = CORS(app, origins=["http://localhost:3000"])
app.config['CORS_HEADERS'] = 'Content-Type'

# cursor.execute("SELECT * from USER")
# data = cursor.fetchone()
# print(data)

@app.route('/', methods=['GET'])
def hello():
    return render_template('upload.html')

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    uname = data['uname']
    pwd = data['pwd']
    hashed_pwd = hashlib.sha512(pwd.encode()).hexdigest()

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM USER WHERE ROLLNO = %s AND PWD = %s",(uname, hashed_pwd))
    res = cursor.fetchone()
    
    
    if res[0] == 1:
        token = str(random.randint(100000, 999999)) + uname
        token = hashlib.sha512(token.encode()).hexdigest()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO SESSION (ROLLNO, TOKEN) VALUES (%s,%s)",(uname, token))
            conn.commit()
            conn.close()
            resp = {"token": token}
            return Response(json.dumps(resp), status=200, mimetype='application/json') 
        except:
            conn.close()
            return Response("{'error': 'USER_SESSION_ACTIVE'}", status=401, mimetype='application/json')

    else:
        conn.close()
        return Response("{'error': 'LOGIN_FAILED'}", status=401, mimetype='application/json')

@app.route('/logout', methods=['POST'])
def logout():
    data = json.loads(request.data)
    print(data)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SESSION WHERE ROLLNO = %s",(data['uname']))
        conn.commit()
        conn.close()
        resp = {'success': 'LOGGED_OUT'}
        return Response(json.dumps(resp), status=200, mimetype='application/json')
    except:
        conn.close()
        resp = {'error': 'LOGOUT_ERROR'}
        return Response(json.dumps(resp), status=500, mimetype='application/json')

@app.route('/castvote', methods=['POST'])
def cast_vote():
    data = json.loads(request.data)
    print(data)    

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        if authenticate_user(cursor, data['uname'], data['token']) == False:
            conn.close()
            resp = {'error': 'USER_NOT_AUTHORIZED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')

        cursor.execute("SELECT VOTED FROM USER WHERE ROLLNO=%s",(data['uname']))
        res = cursor.fetchone()

        if res[0] == 0:

            cursor.execute("UPDATE USER SET VOTED = 1 WHERE ROLLNO=%s",(data['uname']))

            cursor.execute("UPDATE GENSEC SET VOTES = VOTES + 1 WHERE ROLLNO=%s",(data['gensec']))
            cursor.execute("UPDATE SPORTSEC SET VOTES = VOTES + 1 WHERE ROLLNO=%s",(data['sportsec']))

            conn.commit()
            conn.close()
            resp = {'success': 'VOTE_COMPLETE'}
            return Response(json.dumps(resp), status=200, mimetype='application/json')
        else:
            resp = {"error": "ALREADY_VOTED"}
            return Response(json.dumps(resp), status=403, mimetype='application/json')
    
    except:
        conn.close()
        resp = {'error': 'VOTE_FAILED'}
        return Response(json.dumps(resp), status=401, mimetype='application/json')

@app.route('/voteruploader', methods = ['POST'])
def upload_voterfile():

    try:
       
       f = request.files['file']
       f.save('voterList.xlsx')
       
       voterList = np.array(pd.read_excel('voterList.xlsx'))

       conn = mysql.connect()
       enroll_voter(voterList,conn)
       conn.close()

       resp = {'success':'OK'}
       return Response(json.dumps(resp), status=201, mimetype='application/json')
       
    except:
        conn.close()
        resp = {'error': 'FILE_UPLOAD_ERROR'}
        return Response(json.dumps(resp), status=500, mimetype='application/json')
    
@app.route('/candidateuploader', methods = ['POST'])
def upload_candidatefile():
    
    formData = str(request.form.to_dict())

    print(formData)
    # uname = formData.uname
    # token = formData.token
    #print(uname, token)
    try:    
        f = request.files['file']
        f.save('candidateList.xlsx')
       
        candidateList = np.array(pd.read_excel('candidateList.xlsx'))

        conn = mysql.connect()
        enroll_candidate(candidateList,conn)
        conn.close()
        resp = {'success':'OK'}
        return Response(json.dumps(resp), status=201, mimetype='application/json')
       
    except:
        resp = {'error': 'FILE_UPLOAD_ERROR'}
        return Response(json.dumps(resp), status=500, mimetype='application/json')
      
@app.route('/fetchcandidates', methods=['POST'])
def fetch_candidates():
    candidates = {'gensec': [], 'sportsec' : []}

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG FROM GENSEC")
    res = cursor.fetchall()
    for cand in res:
        candidates['gensec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4]})

    cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG FROM SPORTSEC")
    res = cursor.fetchall()
    for cand in res:
        candidates['sportsec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4]})

    return Response(json.dumps(candidates), status=200, mimetype='application/json')

@app.route('/fetchresults', methods=['POST'])
def fetch_results():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        data = json.loads(request.data)

        if 'token' not in data or 'uname' not in data or authenticate_user(cursor, data['uname'], data['token']) == False:
            conn.close()
            resp = {'error': 'USER_NOT_AUTHORIZED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')

        results = {'gensec': [], 'sportsec' : []}

        cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG, VOTES  FROM GENSEC ORDER BY VOTES DESC")
        res = cursor.fetchall()
        for cand in res:
            results['gensec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4], 'votes': cand[5]})

        cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG, VOTES FROM SPORTSEC ORDER BY VOTES DESC")
        res = cursor.fetchall()
        for cand in res:
            results['sportsec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4], 'votes': cand[5]})

        return Response(json.dumps(results), status=200, mimetype='application/json')
    except:
        resp = {'error': 'FETCH_FAILED'}
        return Response(json.dumps(resp), status=503, mimetype='application/json')

app.run(port=1234, debug=True)