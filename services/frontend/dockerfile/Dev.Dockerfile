# используем базовый образ node
FROM node:24-alpine

WORKDIR /app

# копируем файлы с зависимостями
COPY package.json package-lock.json ./

# устанавливаем зависимости
RUN npm install

# указываем путь до бинарников в папке с зависимостями
ENV PATH /app/node_modules/.bin:$PATH

