FROM mongo

WORKDIR /usr/src/app

COPY . .

CMD ["mongod"]
