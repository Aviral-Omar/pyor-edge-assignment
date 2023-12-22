# syntax=docker/dockerfile:1

FROM node:slim

WORKDIR /pyor-client

COPY package*.json ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
