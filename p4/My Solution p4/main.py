# project: p3
# submitter: kfharrison
# partner: none
# hours: 4



# comment about where I  got my data tablr from: # https://nces.ed.gov/programs/digest/d21/tables/dt21_323.10.asp

import pandas as pd
from flask import Flask, request, jsonify
import re


app = Flask(__name__ )


data_frame = pd.read_csv("main.csv")



#print("hello")


@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()

    return html



@app.route("/browse.html")
def browsing():
    global data_frame
    
    with open("browse.html") as f:
        html = f.read()

    return ''' <html>
  <body>
    <h1>Welcome this is the browser page!</h1>
    
    <p>Enjoy the data.</p>
    {}
  </body>
</html>'''.format(data_frame.to_html())


num_subscribed = 0

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    # regex vaild email code taken from https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
    if len(re.findall(r'^[a-zA-Z0-9-_.]+@[a-z]+\.[a-x]{2,3}$', email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        global num_subscribed
        num_subscribed += 1
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    else:
        return jsonify(f"ERROR you are breaking European Law!! No cookies for you :( ")
    return jsonify(f) # 3


#need a better statement

#2. I need to figure out how to get my data frame on the browser page

# @app.route("/browse")
# def add_data():
#     data_frame = df.iloc[:35,:10]
#     return data_frame.to_html()





@app.route("/donate.html")
def donations():
    with open("donate.html") as f:
        html = f.read()

    return ''' <html>
  <body>
    <h1>this is the donations page!</h1>
    
    <p>please consider donating to the cause</p>
    {}
  </body>
</html>'''





if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.



        
        