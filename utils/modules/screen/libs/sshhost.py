import paramiko

from utils.constants import Minecraft


def getoutput(command):
    """Run the command and return its output as a string.

    Parameters
    ----------
    command: str
        The command to run

    Returns
    -------
    str
        The output of the command
    """

    client = _connect_to_host(
        Minecraft.host, Minecraft.username, Minecraft.password, Minecraft.port)
    _, stdout, _ = client.exec_command(command)
    _close_host(client)

    return stdout.read().decode()


def execute(command):
    """Run the command.

    Parameters
    ----------
    command: str
        The command to run
    """

    client = _connect_to_host(
        Minecraft.host, Minecraft.username, Minecraft.password, Minecraft.port)
    client.exec_command(command)
    _close_host(client)


def _connect_to_host(host, username, password, port):
    """Connect to a host using SSH and return the client object.

    Parameters
    ----------
    host: str
        The host to connect to
    username: str
        The username to use
    password: str
        The password to use
    port: int
        The port to use

    Returns
    -------
    paramiko.client.SSHClient
        The SSH client object
    """

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port=port)

    return client


def _close_host(client):
    """Close the connection to a host.

    Parameters
    ----------
    client: paramiko.client.SSHClient
        The SSH client object
    """

    client.close()
