from shipyard_templates import ExitCodeException, Presentations

# Custom Exit Codes specific to Google Slides
EXIT_CODE_INVALID_PRESENTATION_TITLE = 301
EXIT_CODE_SLIDE_CREATION_FAILED = 302
EXIT_CODE_BATCH_UPDATE_FAILED = 303
EXIT_CODE_PERMISSION_FAILED = 304
EXIT_CODE_SAVE_FAILED = 305


class InvalidPresentationTitleError(ExitCodeException):
    def __init__(self, title):
        self.message = f"The presentation title '{title}' is invalid or empty."
        super().__init__(self.message, EXIT_CODE_INVALID_PRESENTATION_TITLE)


class SlideCreationError(ExitCodeException):
    def __init__(self, slide_index):
        self.message = f"Failed to create slide at index {slide_index}."
        super().__init__(self.message, EXIT_CODE_SLIDE_CREATION_FAILED)


class BatchUpdateError(ExitCodeException):
    def __init__(self, details=None):
        self.message = "Slides API batchUpdate failed."
        if details:
            self.message += f" Details: {details}"
        super().__init__(self.message, EXIT_CODE_BATCH_UPDATE_FAILED)


class SharePermissionError(ExitCodeException):
    def __init__(self, presentation_id):
        self.message = (
            f"Failed to update sharing permissions for presentation {presentation_id}."
        )
        super().__init__(self.message, EXIT_CODE_PERMISSION_FAILED)


class PresentationSaveError(ExitCodeException):
    def __init__(self, path):
        self.message = f"Failed to save presentation to path: {path}."
        super().__init__(self.message, EXIT_CODE_SAVE_FAILED)
