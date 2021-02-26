from flask import render_template_string, request, Response
from urllib.parse import urlparse
import socket, os, random, string

FLAG = ''.join(random.choice(string.ascii_letters) for i in range(30))
SECRET = random.randint(1000, 9999)

with open('flag-1/flag_1.py') as f:
  SOURCE = f.read()

def get_flag_1():
  return FLAG

def flag_1_route(app):

  @app.route('/secret-flag-1')
  def secret_flag_1():
    if request.remote_addr != "127.0.0.1":
      return "Access denied!"

    secret = request.headers.get("X-Secret", "???")

    if secret == "???":
      return "Cold."

    if secret != str(SECRET):
      return "Hot."

    return f"Nice Job! The flag is {FLAG}.\n"

  @app.route('/flag-1')
  def flag_1():
    with open('flag-1/flag-1.html') as f:
      template = f.read()
      return render_template_string(template, title="Flag 1", src=SOURCE)

  @app.route('/fetch-flag-1', methods=["POST"])
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