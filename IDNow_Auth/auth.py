import json
import requests
import base64
import cv2

class Auth:
    def __init__(self):
        self.api = IDNow()
        self.users = {}
        self.count = 0

    def liveness(self,ffi,lfi,rfi):
        #make sure the 3 images given belong to the same person
        ret = self.api.ldi(ffi,lfi,rfi)
        return ret['accepted'] == True 

    def match_with_id_document(self,id_pic,ffi):
        #make sure the given images belong to the provided id
        ret = self.api.fc(id_pic,ffi)
        return ret['accepted'] == True

    def auth_user(self,person):
        live = self.liveness(person.ffi,person.lfi,person.rfi)
        match = self.match_with_id_document(person.photo_id,person.ffi)
        if live or match :
            person.verify()
            self.users[person.id] = True

    def add_user(self):
        self.count+=1
        self.users[self.count] = False
        return self.count

    def Authenticate(self,person):
        try :   
            return self.users[person.id]
        except KeyError:
            return False
    


class Person:
    def __init__(self,id,name,photo_id,ffi,lfi,rfi):
        self.name = "New User"
        self.id = id
        self.photo_id = photo_id
        self.verified = False
        self.ffi = ffi
        self.lfi = lfi
        self.rfi = rfi

    def verify(self):
        self.verified = True
    

class IDNow:
    def __init__(self):
        self.url = 'https://hackathon-stuttgart-2019.test.idnow.de/'
        self.header = {'Content-type': 'application/json', 'Accept': 'application/json'}

    def vfi(self,image,mode):
        MODES = ['FACE_LOOK_LEFT', 'FACE_LOOK_RIGHT',  'FACE']
        img_b64 = base64.b64encode(image)
        payload = {"base64EncodedImage" : img_b64 ,
                        "faceTypes" : [MODES[mode]]
                }
        response = requests.request("POST", self.url + 'api/v1/verify_face_image?notMsgPacked=true', headers=self.header, json = payload)
        print(str(response.text.encode('utf8')))
        if str(response.text.encode('utf8')) == "b''":
            return {}
        return response.json()

    def ldi(self,ffi,lfi,rfi):
        ffi = base64.b64encode(ffi)
        lfi = base64.b64encode(lfi)
        rfi = base64.b64encode(rfi)
        payload = {"base64EncodedFrontalFaceImage": ffi ,
                    "base64EncodedLeftFaceImage": lfi,
                    "base64EncodedRightFaceImage": rfi
                }
        response = requests.request("POST", self.url + 'api/v1/live_detection?notMsgPacked=true', headers=self.header, json = payload)
        print(response.text.encode('utf8'))
        if str(response.text.encode('utf8')) == "b''":
            return {}
        return response.json()

    def fc(self,id_img,front_img):
        id_b64 = base64.b64encode(id_img)
        front_b64 = base64.b64encode(front_img)
        payload = {"base64EncodedDocumentFaceImage" : id_b64 ,
                        "base64EncodedFrontalFaceImage" : front_b64
                }
        
        response = requests.request("POST", self.url + 'api/v1/face_comparison?notMsgPacked=true', headers=self.header, json = payload)
        #{"result":0.8647528076171875,"accepted":true,"normalized_score":86.47528076171875,"threshold":30.0,"version":"4.38.0"}
        print(response.text.encode('utf8'))
        # return response.json()['accepted'] == True
        if str(response.text.encode('utf8')) == "b''":
            return {}
        return response.json()

    def ensure_front_image(self,img):
        ret = self.vfi(img,2)
        try :
            return ret["fullFrontalOk"] ==True and ret["nonOccluded"] == False
        except KeyError:
            return False

    def ensure_left_image(self,img):
        ret = self.vfi(img,0)
        try :
            return ret["lookRightOk"] ==True and ret["nonOccluded"] == False
        except KeyError:
            return False

    def ensure_right_image(self,img):
        ret = self.vfi(img,1)
        try :
            return ret["lookRightOk"] ==True and ret["nonOccluded"] == False
        except KeyError:
            return False

def imread(fn,scale=0.15):
    im = cv2.imread(fn)
    im = cv2.resize(im,None,fx=scale,fy=scale)
    __,im = cv2.imencode('.jpg', im) 
    return im   

def app():
    auth = Auth()
    api = IDNow()
    id = auth.add_user()
    photo_id = imread('id.jpg')
    ffi = imread('ffi.jpg',1)
    lfi = imread('lfi.jpg',1)
    rfi = imread('lfi.jpg',1)
    #user has filled in a form, time to verify
    print('Test Front')
    ffi_q = api.ensure_front_image(ffi)
    print('Test Left')
    lfi_q = api.ensure_left_image(lfi)
    print('Test Right')
    rfi_q = api.ensure_right_image(rfi)
    print('front : ', ffi_q,'\nLeft : ', lfi_q,'\nRight : ', ffi_q)
    #retake images?

    user = Person(id,"The Man",photo_id,ffi,lfi,rfi)
    auth.auth_user(user)
    print('Users : ')
    print(auth.users)

def test_fc():
    api = IDNow()

    id_img = imread('id.jpg')
    front_img = imread('ffi.jpg')
    r = api.fc(id_img, front_img) 
    print(r)

def test_vfi():
    api = IDNow()
    img = imread('cap.jpg',1)
    api.vfi(img,0)

def test_idi():
    api = IDNow()
    ffi = imread('sls.jpg',0.3)
    lfi = imread('sls.jpg',0.3)
    rfi = imread('sls.jpg',0.3)

    api.ldi(ffi,lfi,rfi)

if __name__ == "__main__":
    # 
    cap = cv2.VideoCapture(1)
    test_vfi()
    cap.read()
    __,im = cap.read()
    cv2.imwrite("cap2.jpg",im)
    cap.release()
   #app()
