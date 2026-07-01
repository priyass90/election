from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

FILE = "results.xlsx"

# ---------------------------------------
# Candidate Details
# ---------------------------------------

houses = {

    "Phoenix": {

        "logo": "1.png",

        "captain":[
            "Jaivanth Raj",
            "Harshit"
        ],

        "vice":[
            "Amrutha",
            "Rakshan",
            "Rishab",
            "Muthukumaran"
        ]

    },

    "Raptor": {

        "logo":"2.png",

        "captain":[
            "Jayanth",
            "Smaran",
            "Sanchitha",
            "Nripesh",
            "Dhaksha"
        ],

        "vice":[
            "Saurav",
            "Hamsini",
            "Vijay",
            "Niranjan",
            "Shyam Sundar"
        ]

    },

    "Drakon":{

        "logo":"3.png",

        "captain":[
            "Manikandan",
            "Chathresh",
            "Mridhula",
            "Koshini",
            "Kavin"
        ],

        "vice":[
            "Akshitha",
            "Shakthi",
            "Pranav",
            "Kevin Karsten",
            "Viyan"
        ]

    },

    "Lykaris":{

        "logo":"4.png",

        "captain":[
            "Saai Rakshitha",
            "Meenakshi",
            "Bhavesh"
        ],

        "vice":[
            "Sai Akshar",
            "Roshan",
            "Thejesh",
            "Ruthvika",
            "Mansavika",
            "Dheera",
            "Sarvesh",
            "Panav",
            "Mohammed Rihab"
        ]

    }

}

# ---------------------------------------

if not os.path.exists(FILE):

    df = pd.DataFrame(columns=[
    "House",
    "House Captain",
    "House Vice Captain",
    "Time"
    ])

    df.to_excel(FILE,index=False)

# ---------------------------------------

@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/home")
def home():

    return render_template(
        "index.html",
        houses=houses
    )

# ---------------------------------------

@app.route("/vote/<house>")
def vote(house):

    return render_template(

        "vote.html",

        house=house,

        captains=houses[house]["captain"],

        vice=houses[house]["vice"]

    )

# ---------------------------------------

@app.route("/submit",methods=["POST"])
def submit():

    house=request.form["house"]

    captain=request.form["captain"]

    vice=request.form["vice"]

    df=pd.read_excel(FILE)

    new_vote = pd.DataFrame([{
    "House": house,
    "House Captain": captain,
    "House Vice Captain": vice,
    "Time": datetime.now()

    }])

    df=pd.concat([df,new_vote],ignore_index=True)

    df.to_excel(FILE,index=False)

    return render_template("thankyou.html")

# ---------------------------------------

@app.route("/admin")
def admin():

    password = request.args.get("password")

    if password != "ggn2026":
        return """
        <center style='font-family:Arial;margin-top:150px'>
        <h1>🔒 Access Denied</h1>
        <h2>Use:</h2>
        <h3>/admin?password=ggn2026</h3>
        </center>
        """

    df = pd.read_excel(FILE)

    total = len(df)

    houses_count = df["House"].value_counts().to_dict()

    return render_template(
        "admin.html",
        total=total,
        houses=houses_count
    )
# ---------------------------------------

@app.route("/results")
def results():

    if not os.path.exists(FILE):
        return "<h2>No votes have been cast yet.</h2>"

    df = pd.read_excel(FILE)

    house_results = {}

    for house in houses.keys():

        house_df = df[df["House"] == house]

        captain_votes = house_df["House Captain"].value_counts().to_dict()

        vice_votes = house_df["House Vice Captain"].value_counts().to_dict()

        house_results[house] = {
            "captain": captain_votes,
            "vice": vice_votes
        }

    return render_template(
        "results.html",
        results=house_results
    )
# ---------------------------------------

@app.route("/download")
def download():

    return send_file(

        FILE,

        as_attachment=True

    )

# ---------------------------------------

if __name__=="__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
