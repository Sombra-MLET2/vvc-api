FROM python:3.12-slim-bookworm
LABEL authors="Sombra-MLET2 Team"

WORKDIR /app/

COPY . /app/

RUN apt-get update && apt-get install firefox-esr -y

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "8000"]