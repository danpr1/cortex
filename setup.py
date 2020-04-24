import json

from websocket import create_connection
import ssl
import serial

receivedData = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})
ser = serial.Serial('COM5', 9600)
global Sensor2af4
global Sensor1


def setup():
    receivedData.send(json.dumps({

        "id": 1,
        "jsonrpc": "2.0",
        "method": "getUserLogin"

    }))
    print(receivedData.recv())

    receivedData.send(json.dumps(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {

                "clientId": "8oYqAvSTezaO9kjzmHoydufEULof6wR4lmEAWnJ8",
                "clientSecret": "YFMZZlEdeOJvWNYna8f4u2ZaVpz5QYAURpbnaQLcl5KWqxITJt2ZPfNOIqxHPOiomP8OkUXZ1iXbDUrCMbaKNt7drLRpAU7qaEWalxCyLmahoTSDkrale7iryDZRqkCe",
                "license": "b4a8b9af-a5b8-4e76-98d9-278925616b69",
                "debit": 10
            }

        }))
    token = receivedData.recv()[49:-3]
    print(token)

    receivedData.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "queryHeadsets"
    }))

    print(receivedData.recv())

    receivedData.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "createSession",
        "params": {
            "cortexToken": str(token),
            "headset": "EPOCPLUS-4A2C1294",
            "status": "active",
        },
        "id": 1

    }))
    session = receivedData.recv()[438:-193]
    print(session)

    receivedData.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": {
            "cortexToken": str(token),
            "session": str(session),
            "streams": ["eeg"],
        },
        "id": 1

    }))
    global X
    X = 2
    while True:

        print(receivedData.recv())

        if (X > 1):
            break

    data = json.loads(receivedData.recv())
    if 'eeg' in data:
        value = data['eeg']
        AF3 = value[2]
        global Sensor2af4
        Sensor2af4 = value[15]
        print(AF3, Sensor2af4)
        return value
    else:
        return -1
    while True:
        print(receivedData.recv())
        if Sensor2af4 >= 5000:
            ser.write(b'A')
        elif Sensor2af4 >= 6000:
            ser.write(b'B')


setup()
ser.close()
