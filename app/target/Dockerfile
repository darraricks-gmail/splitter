FROM node:18-alpine
COPY ./app/app.* ./app/target/
COPY ./app/target/ ./app/target/
EXPOSE 9997
CMD ["node", "./app/target/app.js","./app/target"]
