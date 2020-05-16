#!/usr/bin/python3
from flask import Flask, request, Response, render_template_string
from urllib.parse import urlparse
import socket, os, sys, random, string

app = Flask(__name__)
PORT =  os.environ.get('PORT', 3000)
FLAG = ''.join(random.choice(string.ascii_letters) for i in range(30))
SECRET = random.randint(1000, 9999)

with open(sys.argv[0]) as f:
  SOURCE = f.read()

@app.route('/secret')
def secret():
  if request.remote_addr != "127.0.0.1":
    return "Access denied!"

  secret = request.headers.get("X-Secret", "???")

  if secret == "???":
    return "Cold."

  if secret != SECRET:
    return "Hot."

  return f"Nice Job! Flag is {FLAG}"

@app.route('/')
def index():
  return render_template_string(
      """
      <html>
        <body style="background-color: #000;color: white">
          <h1>URL proxy with language preference!</h1>
          <form action="/fetch" method="POST">
            <p>URL: <input name="url" value="https://www.python.org/"></p>
            <p>Language code: <input name="lang" value="en-US"></p>
            <p><input type="submit"></p>
          </form>
          <pre style="font-size: 16px">
Task source:
{{ src }}
          </pre>
        </body>
      </html>
      """, src=SOURCE)

@app.route('/fetch', methods=["POST"])
def fetch():
  url = request.form.get("url", "")
  lang = request.form.get("lang", "en-US")

  if not url:
    return "URL must be provided"

  data = fetch_url(url, lang)
  if data is None:
    return "Failed."

  return Response(data, mimetype="text/plain;charset=utf-8")

def fetch_url(url, lang):
  o = urlparse(url)

  req = '\r\n'.join([
    f"GET {o.path} HTTP/1.1",
    f"Host: {o.netloc}",
    f"Connection: close",
    f"Accept-Language: {lang}",
    "",
    ""
  ])

  print(lang)
  print(req)

  res = o.netloc.split(':')
  if len(res) == 1:
    host = res[0]
    port = 80
  else:
    host = res[0]
    port = int(res[1])

  data = b""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(req.encode('utf-8'))
    while True:
      data_part = s.recv(1024)
      if not data_part:
        break
      data += data_part

  return data

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=PORT)