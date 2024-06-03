"""Erreurs retournées par le module screen
"""


class ScreenNotFoundError(Exception):
    """Erreur de screen inexistant

    Attributes
    ----------
    screen_name: str
        Nom du screen inexistant
    """

    def __init__(self, message: str, screen_name: str) -> None:
        """Initialisation de l'erreur

        Parameters
        ----------
        message: str
            Message d'erreur
        screen_name: str
            Nom du screen inexistant
        """

        message += " Screen \"{0}\" not found".format(screen_name)
        self.screen_name = screen_name
        super(ScreenNotFoundError, self).__init__(message)
