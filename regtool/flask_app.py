# A website scraper from mycarcheck/donedeal.ie for UK/IE registrations
from regdecoder import cablecheck

from flask import Flask, request, session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Generate the chrome selenium browser to avoid the recaptcha/rate limiting
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=chrome_options)

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "9d8g7a09sdf8vya08s7"

@app.route("/", methods=["GET", "POST"])

def adder_page():
    #Create a session so two users lists do not merge if sent at same time
    if "regs" not in session:
        session["regs"] = []
    else:
        session["regs"].clear() #if a session exists, clear it here properly

    errors = ""
    if request.method == "POST":
        try:
            session["regs"].append(request.form["reg1"]) #store the regs in session
            regs = (request.form["reg1"]) #capture the regs to send to worker thread
            session.modified = True
            #print (session)
            if session["regs"] is not None:
                result = cablecheck(regs,browser) #send regs to cablecheck function
                #print ("in loop")
                #generate the result table HTML
                if result:
                    htmlresult="<p> The result is: </p> <table> <tr> <th>Reg - Cable</th> </tr>"
                    for res in result:
                        htmlresult+= "<tr><td>"+res+"</td></tr>"
                    htmlresult+="</table>"
                    #print (htmlresult)
            session["regs"].clear() #clear the session as complete
            session.modified = True
            return '''
                <html>
                    <body>
                        {htmlresult}
                        <p><a href="/">Click here to check more cables</a>
                    </body>
                </html>
            '''.format(htmlresult=htmlresult)
        except:
            errors += "<p>{!r} is not a valid registration or has caused an error.  Please re-check and make sure regs are accurate and seperated by a new line</p>\n".format(request.form["reg1"])
        #finally:
            #browser.quit()
            #browser.quit()
    return '''
        <html>
                <body>
                    {errors}
                    <p><h1>Enter your vehicle registrations - UK & IE ONLY (seperated by new line):</h1></p>
                    <form method="post" action=".">
                        <textarea name="reg1" cols="40" rows="5"></textarea>
                        <p><input type="submit" value="Generate Cable List" /></p>
                    </form>
                </body>
        </html>
    '''.format(errors=errors)