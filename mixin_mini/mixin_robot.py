from mixin_api import MIXIN_API
import json
import requests
import mixin_config as m_config
import uuid
import websocket
import time
import _thread
from io import BytesIO
import gzip

import base64

from flask import session
import random

m_robot = MIXIN_API()
m_robot.appid = m_config.mixin_client_id
m_robot.secret = m_config.mixin_client_secret
m_robot.sessionid = m_config.mixin_pay_sessionid
m_robot.private_key = m_config.private_key
m_robot.asset_pin = m_config.mixin_pay_pin
m_robot.pin_token = m_config.mixin_pin_token

#==transferTo，转账函数==
def transferTo(robot, config, to_user_id, to_asset_id,to_asset_amount,memo):

    encrypted_pin = robot.genEncrypedPin()
    encrypted_pin = encrypted_pin.decode()
    body = {'asset_id': to_asset_id, 'counter_user_id':to_user_id, 'amount':str(to_asset_amount), 'pin':encrypted_pin, 'trace_id':str(uuid.uuid1())}
    body_in_json = json.dumps(body)

    encoded = robot.genPOSTJwtToken('/transfers', body_in_json, config.mixin_client_id)
    r = requests.post('https://api.mixin.one/transfers', json = body, headers = {"Authorization":"Bearer " + str(encoded)[2:-1]})

    result_obj = r.json()
    print(result_obj)
    if 'error' in result_obj:
        error_body = result_obj['error']
        error_code = error_body['code']
        if error_code == 20119:
            print("to :" + to_user_id + " with asset:" + to_asset_id + " amount:" + to_asset_amount)
            print(result_obj)
        return False
    else:
        return True
#======== end =========

#encoded = m_robot.genGETJwtToken('/', "", str(uuid.uuid4()))
#transferTo(m_robot, m_config, userid, realAssetObj["asset_id"], "2", "pay 1 get 2")

#=websocket:error,close,and on_data==

def on_error(ws, error):
    print("error")

def on_close(ws):
    print("### closed ###")

def on_data(ws, readableString, dataType, continueFlag):
    return
#=======end============

#=get_msgs:外部接口===
def get_msgs_value():
    global msg_list
    return msg_list
#====end============
#=on_message==
the_state=""
def on_message(ws, message):
    #print(message)
    global the_state
    inbuffer=BytesIO(message)
    msg_data = gzip.GzipFile(mode="rb", fileobj=inbuffer).read()
    msg_data = str(msg_data,encoding="utf-8")
    msg_data = json.loads(msg_data)
    #print(msg_data)

    action = msg_data["action"]
    if action == "CREATE_MESSAGE" and 'error' not in msg_data and msg_data["data"]["conversation_id"]!="":

        msgid = msg_data["data"]["message_id"]
        data = msg_data["data"]
        typeindata = data["type"]
        categoryindata = data["category"]
        dataindata = data["data"]
        conversationid = data["conversation_id"]
        print("conversation id is:")
        print(conversationid)
        realData =str(base64.b64decode(dataindata),encoding = "utf-8")

        replayMessage(ws, msgid)
        #=====功能A：为MiXin点赞==================
        if realData == "hello":

            btn = "world!".encode('utf-8')
            params = {"conversation_id": data['conversation_id'], "recipient_id": data['user_id'],
                      "message_id": str(uuid.uuid4()), "category": "PLAIN_TEXT",
                      "data": base64.b64encode(btn).decode('utf-8')}
            writeMessage(ws, "CREATE_MESSAGE", params)

#===send btn===
def sendPayBtn(webSocketInstance, in_config, in_conversation_id, to_user_id, inAssetName, inAssetID, inPayAmount, linkColor = "#0CAAF5"):
    payLink = "https://mixin.one/pay?recipient=" + in_config.mixin_client_id + "&asset=" + inAssetID + "&amount=" + str(inPayAmount) + '&trace=' + str(uuid.uuid1()) + '&memo=money'
    print(type(str(inAssetName)))
    print(type(payLink))
    print(type(linkColor))
    btn = '[{"label":"' + str(inAssetName)[2:-1] + '","action":"' + payLink + '","color":"' + linkColor + '"}]'
    btn=btn.encode('utf-8')
    gameEntranceParams = {"conversation_id": in_conversation_id,"recipient_id":to_user_id,"message_id":str(uuid.uuid4()),"category":"APP_BUTTON_GROUP","data":base64.b64encode(btn).decode('utf-8')}
    writeMessage(webSocketInstance, "CREATE_MESSAGE",gameEntranceParams)
#======end===========
#===get asset lists==
def listAssets(robot, config):
    print(config.mixin_client_id)
    print(config.admin_uuid)
    encoded = robot.genGETJwtToken('/assets', "", config.mixin_client_id)


    r = requests.get('https://api.mixin.one/assets', headers = {"Authorization":"Bearer " + str(encoded)[2:-1], "Mixin-Device-Id":config.admin_uuid})
    print(r.status_code)
    if r.status_code != 200:
        result_obj = r.json()
        error_body = result_obj['error']
        print(error_body)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
    assets_info = result_obj["data"]
    asset_list = []
    for singleAsset in assets_info:
        if singleAsset["balance"] != "0":
            asset_list.append((singleAsset["symbol"], singleAsset["balance"]))
    print(asset_list)
    
    return asset_list


#==send user card ===
def sendUserContactCard(ws, in_conversation_id, to_user_id, to_share_userid):
    msgJson = (json.dumps({"user_id":to_share_userid})).encode('utf-8')
    print(msgJson)

    params = {"conversation_id": in_conversation_id,"recipient_id":to_user_id,
              "message_id":str(uuid.uuid4()),"category":"PLAIN_CONTACT","data":base64.b64encode(base64.b64encode(msgJson)).decode('utf-8')}
    #
    print(to_user_id)

    writeMessage(ws, "CREATE_MESSAGE",params)
#====== end =========
#==write and replay==
def replayMessage(websocketInstance, msgid):
    parameter4IncomingMsg = {"message_id":msgid, "status":"READ"}

    Message = {"id":str(uuid.uuid1()), "action":"ACKNOWLEDGE_MESSAGE_RECEIPT", "params":parameter4IncomingMsg}
    Message_instring = json.dumps(Message)
    Message_instring = bytes(Message_instring, encoding="utf-8")
    fgz = BytesIO()
    gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
    gzip_obj.write(Message_instring)
    gzip_obj.close()
    print('yep')
    websocketInstance.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)

def writeMessage(websocketInstance, action, params):
    Message = {"id":str(uuid.uuid1()), "action":action, "params":params}
    print(Message)

    Message_instring = json.dumps(Message)
    Message_instring = bytes(Message_instring, encoding="utf-8")
    fgz = BytesIO()
    gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
    gzip_obj.write(Message_instring)
    gzip_obj.close()
    websocketInstance.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
#===end==


def on_open(ws):
    def run(*args):
        print("run")

        #信息打个包~
        Message = {"id":str(uuid.uuid1()), "action":"LIST_PENDING_MESSAGES"}
        Message_instring = json.dumps(Message)
        Message_instring = bytes(Message_instring, encoding="utf-8")
        sth = BytesIO()
        gzip_obj= gzip.GzipFile(mode='wb', fileobj=sth)
        gzip_obj.write(Message_instring)
        gzip_obj.close()

        ws.send(sth.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
        while True:
            a = 1
            time.sleep(10)
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    while True:

        encoded = m_robot.genGETJwtToken('/', "", str(uuid.uuid4()))
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://blaze.mixin.one/",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_data=on_data,
                                    on_close=on_close,
                                    header = ["Authorization:Bearer " + encoded.decode('utf-8')],
                                    subprotocols = ["Mixin-Blaze-1"])
        ws.on_open=on_open
        ws.run_forever()
        print("run")