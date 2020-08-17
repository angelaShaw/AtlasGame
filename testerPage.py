import random

import psycopg2
from flask import render_template, Flask, request, url_for, session,jsonify
import datetime as dt
import json
from tester import insertMessages, get5

app = Flask(__name__)
app.secret_key = "Test_Secret_Key"
global activeUser

@app.route('/ajax' , methods=['POST'])
def getResponse():
    strInput = request.get_json()
    strResponse = "Hello "+str(strInput)
    strLink="<a href='https://en.wikipedia.org/wiki/Raniganj' target='myWiki'>Wiki</a>"
    return jsonify(message=strResponse, score=strLink)

@app.route('/')
def page():
    if 'HumanPoints' in session:
        session.clear()
        global activeUser
        activeUser =activeUser -1
        score = 3
        session['HumanPoints'] = score
        session['CompPoints'] = score
        name, time = get5()
        return render_template('firstPage.html', myX= "NO NAME", humanPoints = score, compPoints = score, names = name, times = time)
    else:
        logInTime = dt.datetime.now()
        session['LoggedInTime'] = str(logInTime)
        score =3
        session['HumanPoints'] = score
        session['CompPoints'] = score
        name, time = get5()
        return render_template('firstPage.html', myX= "NO NAME", humanPoints = score, compPoints = score, names = name, times = time)

@app.route('/getActiveUser',methods=['GET'])
def activeUser():
    global activeUser
    return jsonify(message = "NUMBER OF ACTIVE USERS: "+ str(activeUser))

def deductPoints(val):
    temp= int(val)
    return temp-1

@app.route('/getCountry', methods=['POST', 'GET'])
def getCountry():
    inputTxt = request.get_json()
    x = inputTxt["userInput"]
    humanFind = False
    if 'Login' in session:
        y = json.loads(str(session['MasterList']))
        z = json.loads(str(session['GameList']))
        start = ""
        endSentence = ""
        if(x.upper()[0] == str(session.get('LastLetter'))):
            if x.upper() in y:
                if x.upper() in z:
                    start = "THIS COUNTRY WAS ALREADY STATED-POINT DEDUCTION"
                    endSentence = session.get("LastLetter")
                    session['HumanPoints'] = deductPoints(session.get("HumanPoints"))
                else:
                    humanFind = True
                    start = x.upper()
                    session['Trans'] = int(session['Trans']) + 1
                    session['LastLetter'] = x.upper()[len(x) - 1]
                    z.append(x.upper())
                    endSentence = str(session.get('LastLetter'))
            else:
                start = "THIS IS NOT A VALID NAME-POINT DEDUCTION"
                endSentence = session.get("LastLetter")
                session['HumanPoints'] = deductPoints(session.get('HumanPoints'))
        else:
            start = "THIS COUNTRY DOES NOT START WITH THE RIGHT LETTER-POINT DEDUCTION"
            session['HumanPoints'] = deductPoints(session.get('HumanPoints'))

        if(humanFind == False):
            if(start == ""):
                start = "THIS COUNTRY DOES NOT START WITH THE RIGHT LETTER-POINT DEDUCTION"
        found = False
        compAnswer = ""
        w = (json.loads(session["CompList"]))
        for i in w:
            if (i[0] == session.get('LastLetter')):
                if (i in z):
                    continue
                else:
                    found = True
                    z.append(i)
                    session['LastLetter'] = i[len(i) - 1]
                    compAnswer = i
                    break
        if (found == False):
            compAnswer = "COMPUTER COULD NOT FIND A COUNTRY STARTING WITH THE LETTER POINT DEDUCTION  "
            endSentence2 =  session.get("LastLetter")
            session['CompPoints'] = deductPoints(session.get('CompPoints'))

        endSentence2 =  session.get("LastLetter")
        session['GameList'] = json.dumps(z)
        humanNot = False
        if(humanFind == True):
            start = "<a href='https://www.openstreetmap.org/search?query=" + start + "' target='_blank'>" + start + "</a>"

        if (found == True):
            compAnswer = "<a href='https://www.openstreetmap.org/search?query=" + compAnswer + "' target='_blank'>" + compAnswer + "</a>"

        session.update = True
        if(int(session['CompPoints']) == 0 or int(session['HumanPoints']) == 0):
            session['Out'] = str(dt.datetime.now())
            setNameTime()
        return jsonify(start=start, compValue=compAnswer, end=endSentence, end2=endSentence2, humanPoints = session.get("HumanPoints"), compPoints = session.get('CompPoints'))
    else:
        session['Trans'] = 0
        y = getCompList(getMaster())
        gameLst = []
        session['Login'] = True
        global activeUser
        activeUser = activeUser + 1
        session['Name'] = x.upper()
        session['MasterList'] = json.dumps(getMaster())
        session['CompList'] = json.dumps(y)

        session['LastLetter'] = 'A'
        session['StartOutput'] = 'COMPUTERS TURN START WITH THE LETTER A'
        nextWord = ""
        found = False
        endSentence = ""
        for i in y:
            if (i[0] == 'A'):
                nextWord = i
                found = True
                session['LastLetter'] = i[len(i) - 1]
                gameLst.append(i)
                endSentence = 'HUMANS TURN \n STARTING LETTER IS ' + session.get("LastLetter")
                break
        if (found == False):
            nextWord = "COMPUTER COULD NOT FIND THE RIGHT WORD TO START WITH THE GIVEN LETTER"
            endSentence = "COMPUTER POINT DEDUCTION"

        session['GameList'] = json.dumps(gameLst)
        session.update = True
        if (found == True):
            nextWord = "<a href='https://www.openstreetmap.org/search?query=" + nextWord + "' target='_blank'>" + nextWord + "</a>"
        return jsonify(start= 'X', compValue=nextWord, end = "X",  end2=str(session.get("LastLetter")), humanPoints = session.get("HumanPoints"), compPoints = session.get('CompPoints'))

@app.route('/test')
def test():
    return render_template('addCountry.html')

def getMaster():
    f = open("./countries", "r")
    x = f.read().split('\n')
    master = []
    for i in x:
        master.append(i.strip().upper())
    return master

def getCompList(master):
    comp = []
    counter = int(len(master) / 2)
    for i in range(counter):
        val = random.randint(0, len(master) - 1)
        str = master.pop(val)
        comp.append(str)
    return comp

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

def setter():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="mysecretpassword",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres_db")

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE mobile
              ( Name, Login, Logout ); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")
        # session['Name'].commmit()
        # session['In'].commmit()
        # session['Out'].commmit()
        "Angela".commit()

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
def setNameTime():

    insertMessages(session['Name'], int(session['Trans']))

if __name__ == '__main__':
    #global activeUser
    activeUser = 0
    app.run()
