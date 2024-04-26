# from threading import Thread
from time import sleep

# For remote client (ssh)
import paramiko

# For local client
from subprocess import getoutput
from os import system

from libs.utils.screen.errors import ScreenNotFoundError


class Screen():
    """
    Represents a GNU Screen object.

    Attributes
    ----------
    name: str
        The screen name
    _id: str
        The identifier of the screen
    _status: str
        State of the screen
    logs: file
        The log file of the screen
    _logfilename: str
        The log filename of the screen

    Methods
    -------
    enable_logs(filename=None)
        Enable the logs of the screen session.
    disable_logs(remove_logfile=False)
        Disable the logs of the screen session.
    initialize()
        Initialize a screen, if does not exists yet.
    interrupt()
        Insert CTRL+C in the screen session.
    kill()
        Kill the screen applications then close the screen.
    detach()
        Detach the screen.
    send_commands(*commands)
        Send commands to the active GNU Screen.
    add_user_access(unix_user_name)
        Allow to share your session with an other unix user.
    _screen_commands(*commands)
        Allow to insert generic screen specific commands.
    _check_exists(message="Error code: 404.")
        Check whereas the screen exist. if not, raise an exception.
    _set_screen_infos()
        Set the screen information related parameters.
    """

    def __init__(self, name, initialize=False, host=None, username=None, password=None, port=None):
        """
        Parameters
        ----------
        name: str
            The screen name
        initialize: bool (optional)
            Create the screen or not (default is False)
        host: str (optional)
            The host of the remote client (default is None)
        username: str (optional)
            The username of the remote client (default is None)
        password: str (optional)
            The password of the remote client (default is None)
        port: int (optional)
            The port of the remote client (default is None)
        """

        self.name = name
        self._id = None
        self._status = None
        self.logs = None
        self._logfilename = None

        self.client = None
        if host:
            self.client = paramiko.client.SSHClient()
            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.client.connect(host, username=username,
                                password=password, port=port)

        if initialize:
            self.initialize()

    @property
    def id(self):
        """Get the identifier of the screen.

        Returns
        -------
        str
            The screen id
        """

        if not self._id:
            self._set_screen_infos()
        return self._id

    @property
    def status(self):
        """Get the status of the screen.

        Returns
        -------
        str
            The status of the screen (eg. : 'Up', 'Down')
        """

        self._set_screen_infos()
        return self._status

    @property
    def exists(self):
        """Tell if the screen session exists or not.

        Parse the screen -ls call, to find if the screen exists or not (eg. : '	28062.G.Terminal	(Detached)')

        Returns
        -------
        bool
            The status
        """

        output = self._getoutput_commands('screen -ls').split('\n')

        # Check if the screen exists in the output
        for line in output:
            if line.startswith('\t') and self.name in line and self.name == ".".join(line.split('\t')[1].split('.')[1:]):
                return True
        return False

    def initialize(self):
        """Initialize a screen, if does not exists yet."""

        if not self.exists:
            self._id = None

            # Create detached screen
            self._host_commands('screen -dmS ' + self.name)

    def interrupt(self):
        """Insert CTRL+C in the screen session."""

        self._screen_commands('eval "stuff \\003"')

    def kill(self):
        """Kill the screen applications then close the screen"""
        self._screen_commands(f'stuff "exit" ', 'eval "stuff \\015"')

    def send_commands(self, *commands):
        """Send commands to the active GNU Screen.

        Parameters
        ----------
        *commands: str
            The commands to send

        Examples
        --------
        >>> screen = Screen('test')
        >>> screen.send_commands('ls', 'pwd')
        """

        self._check_exists()
        for command in commands:
            self._screen_commands(f'stuff "{command}" ', 'eval "stuff \\015"')

    def _screen_commands(self, *commands):
        """Allow to insert generic screen specific commands.

        A glossary of the existing screen command in `man screen`.
        """

        self._check_exists()

        for command in commands:
            self._host_commands('screen -x ' + self.id + ' -X ' + command)
            sleep(0.02)

    def _host_commands(self, *commands):
        """Allow to insert generic host specific commands."""

        if not self.client:
            for command in commands:
                system(command)

        else:
            for command in commands:
                self.client.exec_command(command)

    def _getoutput_commands(self, commands):
        """Allow to insert generic host specific commands."""

        if not self.client:
            return getoutput(commands)

        else:
            _, output, _ = self.client.exec_command(commands)
            return output.read().decode()

    def _check_exists(self, message="Error code: 404."):
        """Check whereas the screen exist. if not, raise an exception."""

        if not self.exists:
            raise ScreenNotFoundError(message, self.name)

    def _set_screen_infos(self):
        """Set the screen information related parameters."""

        if self.exists:
            line = ""

            output = self._getoutput_commands(f"screen -ls {self.name}")

            for l in output.split('\n'):
                if (l.startswith('\t') and self.name in l and self.name == ".".join(l.split('\t')[1].split('.')[1:]) in l):
                    line = l
            if not line:
                raise ScreenNotFoundError("While getting info.", self.name)

            infos = line.split('\t')[1:]
            self._id = infos[0].split('.')[0]

            if len(infos) == 3:
                self._status = infos[2][1:-1]
            else:
                self._status = infos[1][1:-1]

    def __repr__(self):
        """Return the representation of the screen."""

        return "<%s '%s'>" % (self.__class__.__name__, self.name)

    @staticmethod
    def list(host=None, username=None, password=None, port=None):
        """List all the screens.

        Parameters
        ----------
        host: str (optional)
            The host where the screen is running
        username: str (optional)
            The username to connect to the host
        password: str (optional)
            The password to connect to the host
        port: int (optional)
            The port to connect to the host

        Returns
        -------
        list
            The list of the screens
        """

        output = None

        if host is None:
            output = getoutput('screen -ls').split('\n')

            screen_list = [Screen(".".join(l.split('\t')[1].split('.')[1:]))
                           for l in output if l.startswith('\t')]
        else:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=username,
                           password=password, port=port)

            _, output, _ = client.exec_command('screen -ls')
            output = output.read().decode().split('\n')

            screen_list = [Screen(".".join(l.split('\t')[1].split('.')[1:]), False, host=host,
                                  username=username, password=password, port=port) for l in output if l.startswith('\t')]
            client.close()

        return screen_list
