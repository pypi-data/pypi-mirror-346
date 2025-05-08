from abc import ABC, abstractmethod

class Presentations(ABC):
    EXIT_CODE_INVALID_TOKEN = 300
    EXIT_CODE_INVALID_PRESENTATION_ID = 301
    EXIT_CODE_UPLOAD_ERROR = 302
    EXIT_CODE_DOWNLOAD_ERROR = 303
    EXIT_CODE_CREATE_ERROR = 304
    EXIT_CODE_BAD_REQUEST = 305
    EXIT_CODE_FILE_NOT_FOUND = 306
    EXIT_CODE_UNKNOWN_ERROR = 349
    EXIT_CODE_RATE_LIMIT = 350
    EXIT_CODE_INVALID_INPUT = 351

    @abstractmethod
    def connect(self):
        """Establish connection to the Google Slides and Drive services."""
        pass

    @abstractmethod
    def create(self, title: str) -> str:
        """Create a new presentation and return the presentation ID."""
        pass

    @abstractmethod
    def upload(self, presentation_id: str, slides_data: list):
        """Add slides to the specified presentation."""
        pass

    @abstractmethod
    def share(self, presentation_id: str) -> str:
        """Make the presentation shareable and return the shareable link."""
        pass
