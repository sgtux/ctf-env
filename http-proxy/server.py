#!/usr/bin/python3
from flask import Flask, render_template_string
import socket, os, sys, random, string
from flag_1 import flag_1_route

app = Flask(__name__)
PORT =  os.environ.get('PORT', 3000)

flag_1_route(app)

@app.route('/')
def index():
  return render_template_string(
    """
    <html>
        <body style="background-color: #000;color: #0F0">
          <h1>CTF Proxy HTTP!</h1>
          <a href="/flag-1">Flag 1</a>
        </body>
      </html>
    """)

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=PORT)