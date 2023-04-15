FROM registry.papierpain.fr/docker/nextcord:latest

COPY . /bot
RUN SODIUM_INSTALL=system python3 -m pip install -r requirements.txt

CMD [ "python3", "./main.py" ]
