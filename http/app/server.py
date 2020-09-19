#!/usr/bin/python3
from flask import Flask, render_template_string, request
import socket, os, sys, random, string
from flag_1 import flag_1_route, get_flag_1

app = Flask(__name__)
PORT =  os.environ.get('PORT', 3000)

flag_1_route(app)

solved_flags = []

@app.route('/')
def index():
  solved = ''
  for i in range(1, 2):
    solved += f'<a href="/flag-{i}" style="color:white">Flag {i}</a>'
    if str(i) in solved_flags:
      solved += '<span style="margin-left:20px">Completed!</span>'
    solved += '</br>'

  return render_template_string(
    """
    <html>
      <body style="background-color: #000;color: #0F0">
        <h1>CTF Proxy HTTP!</h1>
        %s
        </br></br>
        <span>Post your found flags to /send-flag.</span>
      </body>
    </html>
    """ % solved)

@app.route('/send-flag', methods=["POST"])
def send_flag():
  id = request.form.get("id", "")
  flag = request.form.get("flag", "")

  if id == "" or flag == "":
    return "Invalid id or flag parameters"

  if id == "1":
    if flag == get_flag_1():
      solved_flags.append(id)
      return "Success"
    else:
      return "Invalid flag"
  else:
    return "Invalid id"

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=PORT)