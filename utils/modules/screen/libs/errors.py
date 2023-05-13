"""Erreurs retournées par le module screen"""


class ScreenNotFoundError(Exception):
    """Erreur de screen inexistant"""

    def __init__(self, message, screen_name):
        message += " Screen \"{0}\" not found".format(screen_name)
        self.screen_name = screen_name
        super(ScreenNotFoundError, self).__init__(message)
