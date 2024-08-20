from flask import Flask, redirect, render_template, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

RESPONSES_LIST = "responses"

@app.route("/")
def start_page():
    return render_template("start_survey.html", survey = survey)

@app.route("/begin", methods = ["POST"])
def start_survey():
    session[RESPONSES_LIST] = []
    return redirect("/questions/0")

@app.route("/questions/<int:question_index>")
def show_questions(question_index):
    responses = session.get(RESPONSES_LIST)
    if (responses is None):
        # trying to get to questions too soon -- return them to home page 
        return redirect ("/")
    if (len(responses) == len(survey.questions)):
        # answered all questions, send them to completion page 
        return redirect("/complete")
    if (len(responses) != question_index):
        # trying to access questions out of order
        flash("Invalid question ID - Must access questions in order")
        return redirect (f"/questions/{len(responses)}")
    question = survey.questions[question_index]

    return render_template("question.html", question_number = question_index, question = question)

@app.route("/answer", methods = ["POST"])
def answer_questions():
    choice = request.form["answer"]
    responses = session[RESPONSES_LIST]
    responses.append(choice)
    session[RESPONSES_LIST] = responses

    if (len(responses) == len(survey.questions)):
        return redirect ("/complete")
    else: 
        return redirect(f"/questions/{len(responses)}")
    




@app.route("/complete")
def complete():
    return render_template("completion.html")


if __name__ == "__main__":
    app.run()