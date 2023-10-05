import markdown
import flask
import hashlib
import psycopg2
import datetime
    

key = "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"
import os
import openai

def adduser(uname, pasa):
    url = "postgres://Ishanyjha:ZNE8fMIz9pxj@ep-damp-limit-31626814.us-west-2.aws.neon.tech/user_info"
    con = psycopg2.connect(url)
    curs = con.cursor()

    log = datetime.datetime.now().date()
    curs.execute("INSERT INTO user_info (username, password, lastlog) VALUES (%s,%s,%s)",(uname, pasa, log))
    con.commit()
    con.close()

url = "postgres://Ishanyjha:ZNE8fMIz9pxj@ep-damp-limit-31626814.us-west-2.aws.neon.tech/user_info"
def check(uname):
    con = psycopg2.connect(url)
    curs = con.cursor()

    curs.execute("SELECT * FROM user_info WHERE password = %s", (uname,))
    recs = list(curs.fetchall())
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
    openai.organization = "org-zEVby4wZJTLdgnqziKKA6Uwi"
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

    return response

app = flask.Flask(__name__)
app.config["SECRET KEY"]="ishan"
@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/message", methods=["POST"])
def thing():
    if(flask.request.method=="POST"):
        IdealCareer = flask.request.form.get("IdealCareer")
        Country = flask.request.form.get("Country")
        Age = flask.request.form.get("Age")
        interestsskills = flask.request.form.get("interestsskills")
        har = chatGPT(IdealCareer, Country, Age, interestsskills)
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
        print(P)
        harhar = flask.make_response(flask.redirect("/user"))
        harhar.set_cookie("password", bas.hexdigest())
        return harhar
     else:
        return "Forbidden Input."


@app.route("/user")
def user():
    harharhar = flask.request.cookies.get("password")
    print(harharhar)
    if check(harharhar):
        return flask.render_template("user.html", username = grab(harharhar)[0][0])
    return "nan"
