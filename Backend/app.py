from flask import Flask, request, render_template, Response
from flaskext.mysql import MySQL
from flask_cors import CORS

import pandas as pd
import numpy as np
import random
import time
import json
import sys
import re

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

# App Config
voting_started = False

def reset_db():
    sql_file = '../DB/sec_elec.sql'
    print(f"[INFO] Executing SQL script file: {sql_file}")
    statement = ""

    for line in open(sql_file):
        line = line.strip()
        # p_rint(f'[LINE] {line}')
        # p_rint('[--]',re.match(r'--', line))
        if re.match(r'--', line):
            continue
        # p_rint('[/*/]',re.match(r'/*/', line))
        if re.match(r'/', line):
            continue
        # p_rint('[HERE]')
        if not re.search(r';', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            # p_rint(f"[DEBUG] Executing SQL statement:\n{statement}")
            try:
                cursor.execute(statement)
            except Exception as e:
                # p_rint(f"[ERROR] Failed to execute SQL statement:\n{statement}")
                # p_rint(f"[WARN] MySQLError during execute statement \n\tArgs: {str(e.args)}")
                pass
            statement = ""

args = sys.argv[1:]
if len(args) > 0 and args[0] == "reset_db":
    print(f"[INFO] Resetting database...")
    conn = mysql.connect()
    cursor = conn.cursor()
    reset_db()
    time.sleep(1)
    reset_db()
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[INFO] Database reset complete.")
    exit(0)

# cursor.execute("SELECT * from USER")
# data = cursor.fetchone()
# p_rint(data)

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
    
    # p_rint(res)
    
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
    # p_rint(data)

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
    # p_rint(data)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        if authenticate_user(cursor, data['uname'], data['token']) == False:
            conn.close()
            resp = {'error': 'USER_NOT_AUTHORIZED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')

        if not voting_started:
            conn.close()
            resp = {'error': 'VOTING_NOT_STARTED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')

        cursor.execute("SELECT VOTED FROM USER WHERE ROLLNO=%s",(data['uname']))
        res = cursor.fetchone()

        if res[0] == 0:

            cursor.execute("UPDATE USER SET VOTED = 1 WHERE ROLLNO=%s",(data['uname']))

            for key in data.keys():
                if key != 'token':
                    cursor.execute("UPDATE CANDIDATES SET VOTES = VOTES + 1 WHERE ROLLNO=%s AND POSITION=%s",(data[key], key))

            # cursor.execute("UPDATE GENSEC SET VOTES = VOTES + 1 WHERE ROLLNO=%s",(data['gensec']))
            # cursor.execute("UPDATE SPORTSEC SET VOTES = VOTES + 1 WHERE ROLLNO=%s",(data['sportsec']))

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

@app.route('/togglevoting', methods=['POST'])
def toggle_voting():
    global voting_started

    data = json.loads(request.data)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        if authenticate_user(cursor, data['uname'], data['token']) == False:
            resp = {'error': 'USER_NOT_AUTHORIZED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')
        if not data['uname'] == 'admin' :
            resp = {'error': 'USER_NOT_AUTHORIZED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')
        conn.close()
        voting_started = not voting_started
        return Response("{'success': 'VOTING_TOGGLED'}", status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        resp = {'error': 'ERROR_OCCURED'}
        return Response(json.dumps(resp), status=401, mimetype='application/json')

@app.route('/getvotestatus', methods=['POST'])
def get_vote_status():
    data = json.loads(request.data)
    # p_rint(data)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        if authenticate_user(cursor, data['uname'], data['token']) == False:
            conn.close()
            resp = {'error': 'USER_NOT_AUTHORIZED'}
            return Response(json.dumps(resp), status=401, mimetype='application/json')
        conn.close()
        resp = {'voting_started': voting_started}
        return Response(json.dumps(resp), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        resp = {'error': 'ERROR_OCCURED'}
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

    # p_rint(formData)
    # uname = formData.uname
    # token = formData.token
    # p_rint(uname, token)
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

    candidates = {}

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG FROM CANDIDATES")
    res = cursor.fetchall()
    for cand in res:
        try:
            candidates[cand[3]].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4]})
        except:
            candidates[cand[3]] = []
            candidates[cand[3]].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4]})

    # cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG FROM GENSEC")
    # res = cursor.fetchall()
    # for cand in res:
    #     candidates['gensec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4]})

    # cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG FROM SPORTSEC")
    # res = cursor.fetchall()
    # for cand in res:
    #     candidates['sportsec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4]})

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

        results = {}

        cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG, VOTES  FROM CANDIDATES ORDER BY VOTES DESC")
        res = cursor.fetchall()

        for cand in res:
            try:
                results[cand[3]].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4], 'votes': cand[5]})
            except:
                results[cand[3]] = []
                results[cand[3]].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4], 'votes': cand[5]})
        # cursor.execute("SELECT ROLLNO, NAME, DEPT, POSITION, PROG, VOTES FROM SPORTSEC ORDER BY VOTES DESC")
        # res = cursor.fetchall()
        # for cand in res:
        #     results['sportsec'].append({'rollno': cand[0],'name':cand[1], 'dept':cand[2], 'position':cand[3], 'program':cand[4], 'votes': cand[5]})

        return Response(json.dumps(results), status=200, mimetype='application/json')
    except:
        resp = {'error': 'FETCH_FAILED'}
        return Response(json.dumps(resp), status=503, mimetype='application/json')

app.run(port=1234, debug=True)