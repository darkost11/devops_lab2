# указываем базовый образ, который будет использоваться
# для установки зависимостей
FROM node:24-alpine AS vite-builder

# ARG - это аргумент, который необходимо
# передавать при сборке образа
# обратите внимание на docker-compose.yaml файл
ARG vite_api_url
ENV VITE_API_URL=${vite_api_url}

WORKDIR /app

# копируем файлы с зависимостями
COPY package.json .
COPY package-lock.json .
# устанавливаем зависимости
RUN npm install

# указываем путь до бинарников в папке с зависимостями
# без этого сборка не пройдёт
ENV PATH /app/node_modules/.bin:$PATH

# копируем весь набор исходных файлов
COPY public/ ./public
COPY index.html .
COPY tsconfig* ./
COPY vite.config.ts .
COPY src/ ./src

# данная команда запускает сборку проекта.
# код typescript транспилируется в код JS
# обработанный код записывается в директорию /app/dist
RUN npm run build

# указываем образ для исполнения: nginx раздаёт статику и проксирует запросы
FROM nginx:latest

# создаём директорию для записи логов
RUN mkdir /var/www \
  && mkdir /var/www/logs

# копируем собранный код из слоя сборки в папку nginx
COPY --from=vite-builder /app/dist/ /usr/share/nginx/html/

