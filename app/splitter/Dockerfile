FROM node:18-alpine
COPY ./app/app.* ./app/splitter/
COPY ./app/splitter/ ./app/splitter/
EXPOSE 9997
CMD ["node", "./app/splitter/app.js","./app/splitter"]
