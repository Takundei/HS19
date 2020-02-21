from flask import Flask, render_template, request
import requests
from flask_jsonpify import jsonify
from API.M2M_API import theHue
import threading
import time
app = Flask(__name__)

light = theHue()
LOG = ['','','','','','','','','','','','','']

dashboard = {"state": 'OFF',"status" : 'Available',"issues" : ['No messages'], "IOTA" : 10,"log" : []}
@app.route('/')
def suggestions():
    dashboard['state'] = light.status()
    dashboard["log"] = LOG[-11:]
    print(LOG)
    return render_template('page.html', suggestions=dashboard)

@app.route('/config', methods = ['POST','GET'])
def hire():
    ret = {"message" : '',"type" : '',"code" : 000}
    if request.method == 'POST':
        data = request.form
        if data["obj"] == "log":
            LOG.append(data["val"])
        elif data["obj"] == 'demo':
            ret = {"message" : 'demo',"type" : '',"code" : 222}
            t = threading.Thread(target=demo)
            t.start()
        else:
            dashboard[data["obj"]] = data["val"]
    return jsonify(ret)


def demo():
    
    LOG.append("Light Ready")
    time.sleep(1)

    LOG.append("Request from : AmigoBot ID: BOT1")
    time.sleep(0.5)

    LOG.append("Acknowledging : AmigoBot ID: BOT1")
    dashboard["status"] = "Busy"
    time.sleep(1.5)

    LOG.append("Recieved request for service : Light")
    time.sleep(0.8)

    LOG.append("Agree to execute service and price ")
    time.sleep(0.7)

    LOG.append("Execute transaction on IOTA ")
    time.sleep(5)
    LOG.append("Transaction of IOTA 10 comlete ")

    dashboard["IOTA"] = int(dashboard["IOTA"]) + 10
    dashboard["status"] = "In Use"

    LOG.append("Start Service ")
    time.sleep(0.5)

    light.turn_it_on()
    time.sleep(5)

    LOG.append("End Service ")
    dashboard["status"] = "Available soon"
    time.sleep(0.5)
    light.turn_it_off()

    dashboard["status"] = "Available"
    LOG.append(" ")
    LOG.append("Light Ready")



if __name__ == '__main__':
    app.run(debug=True,port=1234)