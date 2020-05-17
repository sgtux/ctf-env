from flask import render_template_string, request, Response
from urllib.parse import urlparse
import socket, os, random, string

FLAG = ''.join(random.choice(string.ascii_letters) for i in range(30))
SECRET = random.randint(1000, 9999)

with open('flag_1.py') as f:
  SOURCE = f.read()

def flag_1_route(app):

  @app.route('/secret-flag-1')
  def secret():
    if request.remote_addr != "127.0.0.1":
      return "Access denied!"

    secret = request.headers.get("X-Secret", "???")

    if secret == "???":
      return "Cold."

    if secret != str(SECRET):
      return "Hot."

    return f"Nice Job! Flag is {FLAG}"

  @app.route('/flag-1')
  def flag_1():
    return render_template_string(
      """
      <html>
        <body style="background-color: #000;color: #0F0">
          <h1>URL proxy with language preference!</h1>
          <form action="/fetch-flag-1" method="POST">
            <p>URL: <input name="url" value="https://www.python.org/"></p>
            <p>Language code: <input name="lang" value="en-US"></p>
            <p><input type="submit"></p>
          </form>
          <pre style="font-size: 14px">
Source Code:
{{ src }}
          </pre>
        </body>
      </html>
      """, src=SOURCE)

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