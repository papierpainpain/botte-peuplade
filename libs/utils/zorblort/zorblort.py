
import os
from ollama import Client
import ollama
from pathlib import Path

from libs.utils.logger import create_logger


class Zorblort():
    """Intéraction avec l'API du grand et magnifique Zorblort.

    Parameters
    ----------
    """

    def __init__(self, api_host: str, load_all_models: bool = False) -> None:
        """Initialisation de la classe.
        """

        self._logger = create_logger(self.__class__.__name__)
        self.client = Client(host=api_host)
        self.models_loaded = False
        self.context_history = {}

        self._logger.info(
            f"{self.__class__.__name__} loaded: {api_host} (models loaded: {load_all_models})")

        if load_all_models:
            self.load_all_models()

    def load_all_models(self) -> None:
        """Charge tous les modèles disponibles.
        """

        self._logger.debug(
            f"API Zorblort called {self.load_all_models.__name__}")

        # Get model files from the current directory (in models folder)
        models_path = Path(__file__).parent / "models"

        self._logger.info(f"Loading all models from: {models_path}")

        if not os.path.exists(models_path):
            self._logger.error(f"Models folder not found: {models_path}")
        else:
            # Get all files in the models folder
            models_files = os.listdir(models_path)

            for model_file in models_files:
                if model_file.endswith(".Modelfile"):
                    model = model_file.replace(".Modelfile", "")
                    self._logger.debug(
                        f"Loading model: {model} ({model_file})")

                    with open(models_path / model_file, "r", encoding="utf-8") as f:
                        model_content = f.read()

                    self._logger.debug(
                        f"Model content: {model_content}")

                    self._logger.debug(
                        f"Model full path: {models_path / model_file}")
                    self._logger.debug(f"Model content: {model_content}")

                    self.client.create(model=model, modelfile=model_content)
                    self._logger.info(f"Model loaded: {model} ({model_file})")

        self.models_loaded = True

    def _load_model(self, model: str) -> None:
        """Charge un modèle.

        Parameters
        ----------
        model: str
            Nom du modèle à charger.
        """

        self._logger.debug(f"API Zorblort called {self._load_model.__name__}")

        modelfile = f"{model}.Modelfile"
        fullpath = Path(__file__).parent / "models" / modelfile

        self._logger.info(f"Loading model: {model} ({fullpath})")

        if not os.path.exists(fullpath):
            self._logger.error(f"Model file not found: {modelfile}")
            raise FileNotFoundError(f"Model file not found: {modelfile}")

        # Get file content in utf-8
        with open(fullpath, "r", encoding="utf-8") as f:
            model_content = f.read()

        self.client.create(model=model, modelfile=model_content)

    def message(self, message: str, model: str = "llama3", history: bool = False) -> dict:
        """Envoie un message à Zorblort.

        Parameters
        ----------
        message: str
            Message à envoyer à Zorblort.
        model: str
            Modèle à utiliser.
        history: bool
            Historique des échanges.

        Returns
        -------
        dict
            Réponse de Zorblort.
        """

        self._logger.debug(f"Method called {self.message.__name__}")
        self._logger.info(f"Zorblort API request [model: {model}]: {message}")

        response = None
        context = None

        if history and model in self.context_history:
            context = self.context_history[model]

        try:
            if not self.models_loaded and model != "llama3":
                self._load_model(model)

            return_data = self.client.generate(
                model=model, prompt=message, context=context)

            self._logger.debug(f"Zorblort API response: {return_data}")

            response = {
                "message": return_data['response'],
                "duration": return_data['total_duration'] / 1_000_000_000
            }

            if history:
                self.context_history[model] = return_data['context']

        except ollama.ResponseError as e:
            self._logger.error(
                f"Error while chatting with Zorblort: {e.error}")

        return response

    def clean_history(self, model: str = "llama3") -> None:
        """Nettoie l'historique des échanges.

        Parameters
        ----------
        model: str
            Modèle à nettoyer.
        """

        self._logger.debug(f"Method called {self.clean_history.__name__}")

        if model in self.context_history:
            self.context_history.pop(model)
            self._logger.info(f"History cleaned for model: {model}")
        else:
            self._logger.error(f"Model not found in history: {model}")
            raise ValueError(f"Model not found in history: {model}")
