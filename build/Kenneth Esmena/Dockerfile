
FROM python:3.11-slim
WORKDIR /app
COPY handler.py .

CMD ["python","-c","import handler,sys,json;print(json.dumps(handler.handler(json.loads(sys.stdin.read()))))"]
