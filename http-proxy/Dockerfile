FROM alpine:latest
RUN mkdir /app && apk add --update python3 && pip3 install flask
WORKDIR /app
COPY app/* /app/
ENV PORT 80
CMD ["python3", "server.py"]