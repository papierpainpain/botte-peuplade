import requests

API_NUAGE_REPO = "https://nuage.papierpain.fr/api/v2.1/via-repo-token"


class NuageRepo:
    """API pour l'accès à un repo sur nuage.papierpain.fr

    Methods
    ----------
    list_items_in_directory(path)
        Liste les fichiers d'un répertoire

    get_download_link(path)
        Récupère le lien de téléchargement d'un fichier
    """

    def __init__(self, repo_id, api_token) -> None:
        self.repo_id = repo_id
        self.headers = {
            "accept": "application/json",
            "authorization": f"Token {api_token}"
        }

    def list_items_in_directory(self, path: str) -> dict:
        """Liste les fichiers d'un répertoire

        Parameters
        ----------
        path : str
            Chemin du répertoire

        Returns
        -------
        dict
            Liste des fichiers du répertoire
        """

        # Replace spaces with %20 and slashes with %2F
        path = path.replace(" ", "%20").replace("/", "%2F")

        url = f"{API_NUAGE_REPO}/dir/?path={path}&type=f"
        response = requests.get(url, headers=self.headers)
        print(response)

        if response.status_code == 401:
            raise ValueError(f"Unauthorized access: {response.json()}")
        elif response.status_code // 100 == 2:
            return response.json()["dirent_list"]
        else:
            raise FileNotFoundError("Directory not found")

    def get_download_link(self, path) -> str:
        """Récupère le lien de téléchargement d'un fichier

        Parameters
        ----------
        path : str
            Chemin du fichier

        Returns
        -------
        str
            Lien de téléchargement du fichier
        """

        # Replace spaces with %20 and slashes with %2F
        path = path.replace(" ", "%20").replace("/", "%2F")

        url = f"{API_NUAGE_REPO}/download-link/?path={path}"

        return requests.get(url, headers=self.headers).json()
