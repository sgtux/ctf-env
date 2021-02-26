#!/usr/bin/python3
from flask import Flask, render_template_string, request
import socket, os, sys, random, string

sys.path.insert(0, './flag-1')
sys.path.insert(0, './flag-2')

from flag_1 import flag_1_route, get_flag_1
from flag_2 import flag_2_route, get_flag_2

app = Flask(__name__)
PORT =  os.environ.get('PORT', 3000)

flags = {'1': get_flag_1(), '2': get_flag_2()}

flag_1_route(app)
flag_2_route(app)

solved_flags = []

@app.route('/')
def index():
  solved = ''
  for i in range(1, 3):
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
    return "Invalid id or flag parameters."

  if id not in flags:
    return "Invalid id."

  if id in solved_flags:
    return "This flag has already been scored."

  print({'sent-flag':flag, 'server-flag': flags[id]})

  if flag == flags[id]:
    solved_flags.append(id)
    return "Success."
  else:
      return "Invalid flag."

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=PORT)