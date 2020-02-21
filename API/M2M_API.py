from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

app = Flask(__name__)
api = Api(app)


import requests
class theHue:
    def __init__(self):
        self.url = 'http://10.120.52.101/api/kKL6JrWB2Hawl9-zK99B9INwvWTULY2WfeCRH4oc/'

    def turn_it_off(self):
        payload = {"on" : False}
        requests.request('PUT',self.url+'lights/3/state',json=payload)


    def turn_it_on(self):
        payload = {"on" : True, "bri" : 5,"hue":189,"sat":20}
        requests.request('PUT',self.url+'lights/3/state',headers={},json=payload)

    def risky_biznis(self,obj,val):
        payload = {obj : val}
        response = requests.request('PUT',self.url+'lights/3/state',headers={},json=payload)
        print('RSK ->', response.json())

    def status(self):
        payload = {"on" : True, "bri" : 5,"hue":189,"sat":20}
        response = requests.request('GET',self.url+'lights/3',headers={},json=payload)
        print('RSK ->', response.json())
        if response.json()["state"]["on"]:
            return 'ON'
        else:
            return 'OFF' 

class Light_state(Resource):
    def __init__(self):
        self.api = theHue()
    
    def get(self,state):
        ret = {"message" : '',"type" : '',"code" : 000}
        if state == 'on':
            self.api.turn_it_on()
            ret = {"message" : 'Light_ON',"type" : 'success',"code" : 000}
        elif state == 'off':
            self.api.turn_it_off()
            ret = {"message" : 'Light_OFF',"type" : 'success',"code" : 000}
        else:
            ret = {"message" : 'Invalid',"type" : 'error',"code" : 123}

        return jsonify(ret)
            
class Light_config(Resource):
    def __init__(self):
        self.api = theHue()

    def get(self,obj):
        ret = {"message" : '',"type" : '',"code" : 000}
        if 'val' in request.args:
            val = request.args['val']
            self.api.risky_biznis(obj,int(val))
            ret = {"message" : 'Done',"type" : 'message',"code" : '--'}
        else :
            ret = {"message" : 'Invalid_risk',"type" : 'error',"code" : 123}

        return jsonify(ret)

        
@app.route('/api/light/hire', methods = ['POST','GET'])
def hire():
    if request.method == 'POST':
        ret = {"message" : '',"type" : '',"code" : 000}
        data = request.form
        print(data)
        return jsonify(ret)

@app.route('/api/light/demo', methods = ['GET'])
def demo():
    payload = {"obj" : "demo", "val" : 'ss'}
    response = requests.request('POST','http://127.0.0.1:1234/config',headers={},data=payload)
    print(response.json())
    return jsonify(payload)

api.add_resource(Light_config, '/api/light/config/<obj>')
# api.add_resource(Light_hire, '/api/light/hire/')
api.add_resource(Light_state, '/api/light/state/<state>')


    
if __name__ == "__main__":
    api = theHue()
    app.run(port='2630',host='10.120.51.145',debug=True) #0.0.0.0