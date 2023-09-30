import markdown
import flask

key = "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"
import os
import openai


def chatGPT(IdealCareer, Country, Age, interestsskills):
    openai.organization = "org-zEVby4wZJTLdgnqziKKA6Uwi"
    openai.api_key = key


    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a career advisor trying to give career path advice. Someone will give you their age/grade, their country of residence (use this to get localized job information), their ideal career, and their skills. Use this to provide a comprehensive answer with courses, internships, books, resources that they can use"},
            {"role": "user", "content": "I am an 8th grader interested in math, my country is France, I want to be a software engineer, my skils are math and coding."},
            {"role": "assistant", "content": "Based on what you replied, you should take these courses, and use these resources, perhaps try to intern at these companies, and here is any other information that may be relevant to you"},
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



