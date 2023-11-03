# Сбилдить образ
docker build -t gpt_uber .

# Запустить контейнер
docker run -it --rm --name gpt_uber --env-file .env -v ${PWD}/share:/app/share gpt_uber python3 -u main.py

# Запустить консоль контейнера
docker run -it --rm --name gpt_uber --env-file .env gpt_uber sh

# Подсоединиться к консоли контейнера
docker exec -it gpt_uber sh

# Создать миграцию
alembic revision --autogenerate -m "Init structure"
