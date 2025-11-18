import sys
import os
sys.path.insert(0, os.getcwd())
from fastapi.testclient import TestClient
import main

def run():
    client = TestClient(main.app)
    resp = client.get('/admin/consult')
    print('STATUS:', resp.status_code)
    print('CONTENT-TYPE:', resp.headers.get('content-type'))
    body = resp.text
    print('BODY (first 2000 chars):')
    print(body[:2000])

if __name__ == '__main__':
    run()
