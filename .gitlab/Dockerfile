FROM registry.papierpain.fr/docker/nextcord:1.2.0

LABEL Maintainer="PapierPain"
LABEL Description="Discord container for Botte Peuplade"

WORKDIR /bot

COPY . /bot

RUN SODIUM_INSTALL=system python3 -m pip install -r /bot/requirements.txt

CMD ["python3", "./main.py"]
