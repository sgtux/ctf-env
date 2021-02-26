# Basic authentication

from flask import render_template_string, request, Response
from urllib.parse import urlparse
import socket, os, random, string
import base64
import re

FLAG = ''.join(random.choice(string.ascii_letters) for i in range(30))

users = ['hermes', 'zeus', 'hera', 'athena', 'poseidon', 'afrodite', 'appolo', 'artemis']

user = users[random.randint(0,7)]
password = user + str(random.randint(10,99))

basicAuth = base64.b64encode((user + ':' + password).encode('ascii')).decode('utf-8')

def get_flag_2():
  return FLAG

def flag_2_route(app):

  @app.route('/secret-flag-2')
  def secret_flag_2():

    basicHeader = re.sub(r'(B|b)asic ', '', request.headers.get("Authorization", "???"))
    if basicHeader == basicAuth:
        return f"Nice Job! The flag is {FLAG}.\n"
    else:
        return "Nice Try! :("

  @app.route('/flag-2')
  def flag_2(): 
    with open('flag-2/flag-2.html') as f:
      template = f.read()
      return render_template_string(template, title="Flag 2", users = ','.join(users))