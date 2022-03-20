import json

def byte2json(body):
    decoded = body.decode('utf-8')
    return json.loads(decoded)