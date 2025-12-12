FROM  python:3.12-slim
WORKDIR /tests
COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests/ .
#Keep container running after it starts
CMD ["tail", "-f", "/dev/null"]