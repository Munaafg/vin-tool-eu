# A website scraper for vin
import vindecoder
from vindecoder import cablecheck

from flask import Flask, request, session

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "98gh9er8hwerfjsa908vweerrv"

cableNames = vindecoder.cableNames


@app.route("/", methods=["GET", "POST"])
def adder_page():
    #Create a session so two users lists do not merge if sent at same time
    if "vins" not in session:
        session["vins"] = []
    else:
        session["vins"].clear() #if a session exists, clear it here properly

    errors = ""
    if request.method == "POST":
        try:
            session["vins"].append(request.form["vin1"]) #store the vins in session
            vins = (request.form["vin1"]) #capture the vins to send to worker thread
            session.modified = True
            #print (session)
            if session["vins"] is not None:
                result = None #Re init the variable again to remove chance of stale data.
                cables = None #Re init cables again to remove chance of stale data
                backupCables = None #Re init backup Cables again to remove chance of stale data
                #print (vins)
                result = cablecheck(vins) #send vins to cablecheck function
                #generate the result table HTML
                if result:

                    ###generate HTML for summary table
                    countresultHeader="<p><b> Primary Cable Count</b> </p> <table border=\"1\"> <tr>"
                    countresultVals = "<tr>"
                    ### Generate the table headers based on the contents
                    if result[1]:
                        cables = result[1]
                        print (cables)
                        print (cableNames)
                        #change to for loop which checks and validates all the cable types from a list of cableTypes
                        for cableName in cableNames:
                            #print (cableName)
                            if cables.count(cableName):
                                #print ("HERE")
                                ##generate some html string here
                                countresultHeader+= "<td>"+cableName+"</td>"
                                #print ("countresultheade")
                                countresultVals+= "<td>"+str(cables.count(cableName))+"</td>"
                                #print ("countresultvals")

                        #print ("past for loop")
                        countresultHeader+= "</tr>"
                        countresultVals+= "</tr></table>"
                        countresult = countresultHeader+countresultVals
                    #print ("HTML: " + countresult)

                    try:
                        if result[2]:
                            backupCountResultHeader="<p><b> Backup/Additional Cable Count</b> </p> (these may be needed based on results or region. See full results below for information)  <table border=\"1\"> <tr>"
                            backupCountResultVals = "<tr>"
                            backupCables = result[2]
                            print (backupCables)
                            for cableName in cableNames:
                                #print (cableName)
                                if backupCables.count(cableName):
                                    backupCountResultHeader+= "<td>"+cableName+"</td>"
                                    backupCountResultVals+= "<td>"+str(backupCables.count(cableName))+"</td>"

                            backupCountResultHeader+= "</tr>"
                            backupCountResultVals+= "</tr></table>"

                        if backupCountResultHeader:
                            countresult+= backupCountResultHeader+backupCountResultVals
                    except:
                        print("no backup cables found")
                    finally:
                        htmlresult=countresult+"<p></p> <table> <tr> <th>VIN - Cable</th> </tr>"
                        for res in result[0]:
                            htmlresult+= "<tr><td>"+res+"</td></tr>"
                        htmlresult+="</table>"
                        #print (htmlresult)
            session["vins"].clear() #clear the session as complete
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
            errors += "<p>{!r} is not a valid VIN or has caused an error.  Please re-check and make sure VINS are accurate and seperated by a new line</p>\n".format(request.form["vin1"])

    return '''
        <html>
            <body>
                {errors}
                <p><h1>Enter your VINs (separated by new line):</h1></p>
                <form method="post" action=".">
                    <textarea name="vin1" cols="40" rows="5"></textarea>
                    <p><input type="submit" value="Generate Cable List" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)