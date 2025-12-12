FROM node:18-alpine
COPY ./app/app.* ./app/agent/
COPY ./app/agent/ ./app/agent/
EXPOSE 9997
CMD ["tail", "-f", "/dev/null"]