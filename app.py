from flask import Flask, render_template, request, send_file
from fpdf import FPDF

app = Flask(__name__)

ACCESS_CODE = "1234"


def analyze_resume(text):

    text_lower = text.lower()

    # SMART SKILL DETECTION
    skills = []

    if "python" in text_lower:
        skills.append("Python")

    if "html" in text_lower:
        skills.append("HTML")

    if "css" in text_lower:
        skills.append("CSS")

    if "flask" in text_lower:
        skills.append("Flask")

    if "java" in text_lower:
        skills.append("Java")

    # SCORE SYSTEM
    score = len(skills) * 20

    if score > 100:
        score = 100

    return skills, score


@app.route("/", methods=["GET", "POST"])
def home():

    response = ""

    if request.method == "POST":

        access_code = request.form.get("access_code")

        if access_code != ACCESS_CODE:
            return render_template("index.html", response="Wrong Access Code")

        user_input = request.form["user_input"]

        skills, score = analyze_resume(user_input)

        response = f"""
==============================
AI RESUME ANALYSIS REPORT
==============================

INPUT:
{user_input}

SKILLS DETECTED:
{', '.join(skills) if skills else 'No specific skills detected'}

RESUME SCORE:
{score}/100

FEEDBACK:
"""

        if score >= 80:
            response += "Excellent profile! Highly recommended candidate."

        elif score >= 50:
            response += "Good profile, needs minor improvements."

        else:
            response += "Needs skill development and more experience."

        # PDF GENERATE
        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=12)

        pdf.multi_cell(190, 10, response)

        pdf.output("resume.pdf")

    return render_template("index.html", response=response)


@app.route("/download")
def download():

    return send_file("resume.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)