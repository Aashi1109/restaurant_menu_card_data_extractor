FROM node:20-alpine

LABEL author ="Ashish Pal"

LABEL maintainer="Ashish Pal"

LABEL version="1.0.0"

RUN addgroup app && adduser -S -G app app

USER app

WORKDIR /app

COPY package*.json .

USER root

RUN chown -R app:app .

USER app

RUN npm ci

COPY . /app

EXPOSE 3000

CMD ["npm start"]
