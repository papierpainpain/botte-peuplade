from dotenv import load_dotenv
from os import environ

class Bot:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    name = environ.get("BOTTE_NAME")
    version = environ.get("BOTTE_VERSION")
    token = environ.get("BOTTE_TOKEN")
    prefix = environ.get("BOTTE_PREFIX")

class Guild:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    id: int = int(environ.get("GUILD_ID"))

class Minecraft:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    host = environ.get("MINECRAFT_HOST")
    port = int(environ.get("MINECRAFT_PORT"))
    username = environ.get("MINECRAFT_USERNAME")
    password = environ.get("MINECRAFT_PASSWORD")

class Blagues:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    token = environ.get("BLAGUE_API_TOKEN")

class Colors:
    info = 0x00ccb2
    error = 0xf23f42
    warning = 0xffaa00
    success = 0x00cc66
