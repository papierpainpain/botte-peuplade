import os
from dotenv import load_dotenv

load_dotenv()


class Bot:
    """Classe des constantes du Botte

    Attributes
    ----------
    TOKEN (str): Token du bot
    PREFIX (str): Préfixe des commandes
    GUILDS (list): Liste des guilds autorisées
    """

    __slots__ = ()
    TOKEN: str = os.getenv("BOTTE_TOKEN")
    PREFIX: str = os.getenv("BOTTE_PREFIX")
    GUILDS: list = [int(os.getenv("GUILD_ID"))]


class Blagues:
    """Classe des constantes de l'API de blagues

    Attributes
    ----------
    TOKEN (str): Token de l'API de blagues
    """

    __slots__ = ()
    TOKEN: str = os.getenv("BLAGUE_API_TOKEN")


class ZorblortAPI:
    """Classe des constantes de l'API de Zorblort

    Attributes
    ----------
    HOST (str): URL de l'API de Zorblort
    """

    __slots__ = ()
    HOST: str = os.getenv("ZORBLORT_API")


class Minecraft:
    """Classe des constantes de Minecraft

    Attributes
    ----------
    HOST (str): Host du serveur Minecraft
    PORT (int): Port du serveur Minecraft
    USERNAME (str): Nom d'utilisateur du serveur Minecraft
    PASSWORD (str): Mot de passe du serveur Minecraft
    """

    __slots__ = ()
    HOST: str = os.getenv("MINECRAFT_HOST")
    PORT: int = int(os.getenv("MINECRAFT_PORT"))
    USERNAME: str = os.getenv("MINECRAFT_USERNAME")
    PASSWORD: str = os.getenv("MINECRAFT_PASSWORD")


class Colors:
    """Classe des couleurs

    Attributes
    ----------
    INFO (int): Couleur bleue
    ERROR (int): Couleur rouge
    WARNING (int): Couleur orange
    SUCCESS (int): Couleur verte
    """

    __slots__ = ()
    INFO: int = 0x00ccb2
    ERROR: int = 0xf23f42
    WARNING: int = 0xffaa00
    SUCCESS: int = 0x00cc66
