FROM registry.papierpain.fr/docker/nextcord:v1.1.0

LABEL Maintainer="PapierPain"
LABEL Description="Discord container with Nextcord and lavalink"

WORKDIR /bot

COPY . /bot

RUN SODIUM_INSTALL=system python3 -m pip install -r /bot/requirements.txt && \
    chmod a+x /bot/ci/entrypoint.sh

ENTRYPOINT ["/bot/ci/entrypoint.sh"]
CMD ["python3", "./main.py"]
