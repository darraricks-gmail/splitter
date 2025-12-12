FROM node:18-alpine
COPY ./app.* ./agent/
COPY ./agent/ ./agent/
EXPOSE 9997
CMD ["tail", "-f", "/dev/null"]