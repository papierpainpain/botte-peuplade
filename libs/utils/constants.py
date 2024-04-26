import os
from dotenv import load_dotenv
from os import environ


# class Guild:
#     load_dotenv()  # TODO: Trouver comment éviter cette duplication
#     id: int = int(environ.get("GUILD_ID"))


# class Minecraft:
#     load_dotenv()  # TODO: Trouver comment éviter cette duplication
#     host = environ.get("MINECRAFT_HOST")
#     port = int(environ.get("MINECRAFT_PORT"))
#     username = environ.get("MINECRAFT_USERNAME")
#     password = environ.get("MINECRAFT_PASSWORD")


# class Blagues:
#     load_dotenv()  # TODO: Trouver comment éviter cette duplication
#     token = environ.get("BLAGUE_API_TOKEN")


# class Nuage:
#     load_dotenv()  # TODO: Trouver comment éviter cette duplication
#     token = environ.get("PLP_API_TOKEN")


# class Colors:
#     info = 0x00ccb2
#     error = 0xf23f42
#     warning = 0xffaa00
#     success = 0x00cc66


load_dotenv()


class Bot:
    __slots__ = ()
    TOKEN: str = os.getenv("BOTTE_TOKEN")
    PREFIX: str = os.getenv("BOTTE_PREFIX")
    GUILDS: list = [int(os.getenv("GUILD_ID"))]


class Blagues:
    __slots__ = ()
    TOKEN: str = os.getenv("BLAGUE_API_TOKEN")


class Nuage:
    __slots__ = ()
    TOKEN: str = os.getenv("PLP_API_TOKEN")


class Minecraft:
    __slots__ = ()
    HOST: str = os.getenv("MINECRAFT_HOST")
    PORT: int = int(os.getenv("MINECRAFT_PORT"))
    USERNAME: str = os.getenv("MINECRAFT_USERNAME")
    PASSWORD: str = os.getenv("MINECRAFT_PASSWORD")


class Colors:
    __slots__ = ()
    INFO: int = 0x00ccb2
    ERROR: int = 0xf23f42
    WARNING: int = 0xffaa00
    SUCCESS: int = 0x00cc66
