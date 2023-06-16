FROM node:16-alpine


ENV PORT=8080
EXPOSE ${PORT}

WORKDIR /app

COPY package.json /app

# COPY vite.config.js /app

RUN npm install
COPY . /app

CMD ["npm", "run", "dev"]
