import os
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from shipyard_templates import Presentations


class GoogleSlidesClient(Presentations):
    """
    A client for connecting to the Google Slides and Drive APIs using a service account.

    This class sets up authentication using a raw service account JSON string,
    writes it to a temporary file, and uses that to authenticate with Google's APIs.

    Methods:
        connect(): Authenticates and returns the Google Slides and Drive API clients.
    """

    def __init__(self, service_account_json: str) -> None:
        """
        Initialize the client with a raw service account JSON string.

        Args:
            service_account_json (str): The raw JSON string of the Google service account.
        """
        self.service_account = service_account_json

    def _set_env_vars(self) -> str:
        """
        Writes the service account JSON to a temporary file and sets
        the GOOGLE_APPLICATION_CREDENTIALS environment variable.

        Returns:
            str: Path to the temporary credentials file.
        """
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "w") as tmp:
            tmp.write(self.service_account)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
        return path

    def connect(self):
        """
        Authenticate with Google APIs and return both Slides and Drive service clients.

        Returns:
            tuple: (slides_service, drive_service), both built using the authenticated credentials.
        """
        path = self._set_env_vars()
        creds = service_account.Credentials.from_service_account_file(
            path,
            scopes=[
                "https://www.googleapis.com/auth/presentations",
                "https://www.googleapis.com/auth/drive.file",
            ],
        )
        slides_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
        return slides_service, drive_service

    def upload(self, presentation_id: str, slides_data: list):
        pass

    def share(self, presentation_id: str) -> str:
        pass

    def create(self, title: str) -> str:
        pass
