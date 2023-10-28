import markdown
import flask
import hashlib
import psycopg2
import os
import openai
import datetime


def signin(uname, pasa):
    url = os.environ.get("url")
    con = psycopg2.connect(url)
    curs = con.cursor()

    curs.execute("SELECT * FROM user_info WHERE username = %s AND password = %s", (uname,pasa))
    recs = list(curs.fetchall())
    
    if len(recs) == 0:
        return False
    else:
        flask.session["tokens"] = int(recs[0][3])
        return True
    

key = os.environ.get("apikey")

def adduser(uname, pasa):
    url = os.environ.get("url")
    con = psycopg2.connect(url)
    curs = con.cursor()

    log = datetime.datetime.now().date()
    curs.execute("INSERT INTO user_info (username, password, lastlog, tokens) VALUES (%s,%s,%s,%s)",(uname, pasa, log, 3))
    con.commit()
    con.close()

url = os.environ.get("url")
def check(uname):
    con = psycopg2.connect(url)
    curs = con.cursor()

    curs.execute("SELECT * FROM user_info WHERE password = %s", (uname,))
    recs = list(curs.fetchall())
    print(recs)
    if len(recs) == 0:
        return False
    else:
        return True
def grab(psw):
    con = psycopg2.connect(url)
    curs = con.cursor()


    curs.execute("SELECT * FROM user_info WHERE password = %s", (psw,))
    recs = list(curs.fetchall())
    if len(recs) == 0:
        return False
    else:
        return recs
def chatGPT(IdealCareer, Country, Age, interestsskills):
    if (flask.session.get("tokens")<=0):
        return "Not Enough Tokens!"
    openai.organization = os.environ.get("openaiorganization")
    openai.api_key = key


    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a career advisor trying to give career path advice. Someone will give you their age/grade, their country of residence (use this to get localized job information), their ideal career, and their skills. Use this to provide a comprehensive answer with courses, internships, books, resources that they can use"},
            {"role": "user", "content": "I am an 8th grader interested in math, my country is France, I want to be a software engineer, my skils are math and coding."},
            {"role": "assistant", "content": "Based on what you replied, you should take these courses, and use these resources, perhaps try to intern at these companies, and here is any other information that may be relevant to you "},
            {"role": "user", "content": "I am in the "+Age+"th grade, I live in "+Country+", My skills are"+interestsskills +"and my ideal job is a"+IdealCareer}
        ]
    )
    flask.session["tokens"]=flask.session.get("tokens")-1
    con = psycopg2.connect(url)
    curs = con.cursor()

    curs.execute("UPDATE user_info SET tokens = %s WHERE username=%s",(flask.session["tokens"], flask.session["username"]))
    con.commit()
    con.close()

    return response 


app = flask.Flask(__name__)
app.config["SECRET_KEY"]=os.environ.get("secretkey")
@app.route("/")
def index():
    print(os.environ["url"])
    return flask.render_template("index.html")

@app.route("/message", methods=["POST"])
def thing():
    if(flask.request.method=="POST"):
        IdealCareer = flask.request.form.get("IdealCareer")
        Country = flask.request.form.get("Country")
        Age = flask.request.form.get("Age")
        interestsskills = flask.request.form.get("interestsskills")
        har = chatGPT(IdealCareer, Country, Age, interestsskills)
        print(har)
        if(har == "Not Enough Tokens!"):
            return har
        rah = markdown.markdown(har["choices"][0]["message"]["content"])
        return flask.render_template("response.html", har=rah)
    
@app.route("/registration", methods=["POST", "GET"])
def registration():
     if(flask.request.method=="POST"):
        P = flask.request.form.get("Password")
        U = flask.request.form.get("RePassword")
        NU = flask.request.form.get("Username")
        if(P != U): 
            return "Passwords do not match!"
        else:
            bas = hashlib.sha256(P.encode('utf-8'))
            adduser(NU, bas.hexdigest())
            flask.session.clear()
        return flask.redirect("/user")
     else:
        return "Forbidden Input."
     
@app.route("/login", methods=["POST", "GET"])       
def login():
    if(flask.request.method=="POST"):
        print("hello world")
        P = flask.request.form.get("Password")
        U = flask.request.form.get("Username")
        print(P)
        if(signin(U, hashlib.sha256(P.encode('utf-8')).hexdigest()) == True):
            flask.session["username"]=U
            flask.session["isloggedin"] = True
            return flask.redirect("/user")
        else:
            flask.session["isloggedin"] = False
            return "Invalid login har har"
        return flask.jsonify(status=200)
    return "Forbidden Input."
     


 
@app.route("/user") 
def user():
   
    if (flask.session.get("isloggedin")):
        return flask.render_template("user.html", username = flask.session.get("username"),tokens =  flask.session.get("tokens"))
    return flask.redirect("/index.html")
    #return "something wrong"
