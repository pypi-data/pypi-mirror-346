import argparse
import os
import yaml

from shipyard_templates import ShipyardLogger, Presentations, ExitCodeException
from ..googleslides import GoogleSlidesClient
from ..exceptions import (
    InvalidPresentationTitleError,
    BatchUpdateError,
    SharePermissionError,
)

logger = ShipyardLogger.get_logger()


def load_yaml_from_txt(filepath: str) -> dict:
    """
    Load a YAML-structured file with a .txt extension.

    Args:
        filepath (str): Path to the .txt file containing YAML-formatted slide content.

    Returns:
        dict: Parsed content including the presentation title and slide definitions.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        yaml.YAMLError: If the file content is not valid YAML.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def create_presentation_from_yaml(yaml_file: str, service_account: str):
    """
    Create a new blank Google Slides presentation and populate it with GPT-generated content
    based on a YAML-formatted .txt file.

    Args:
        yaml_file (str): Path to the YAML-formatted .txt file.
        service_account (str): Raw JSON string or environment variable with service account credentials.
    """
    client = GoogleSlidesClient(service_account)
    slides_service, drive_service = client.connect()

    # Load YAML content
    data = load_yaml_from_txt(yaml_file)
    title = data.get("title", "Untitled Presentation")
    slides_data = data.get("slides", [])

    # Step 1: Create a blank presentation
    try:
        presentation = (
            slides_service.presentations()
            .create(body={"title": "Alli Generated: " + title})
            .execute()
        )
        presentation_id = presentation["presentationId"]
    except Exception:
        raise InvalidPresentationTitleError(title)

    # Step 2: Create a blank slide for each content block
    create_slide_requests = []
    for _ in slides_data:
        create_slide_requests.append(
            {
                "createSlide": {
                    "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"}
                }
            }
        )

    try:
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": create_slide_requests}
        ).execute()
    except Exception as e:
        raise BatchUpdateError(f"Failed to create slides: {str(e)}")

    # Step 3: Refetch the presentation to get shape IDs to insert content into
    presentation = (
        slides_service.presentations().get(presentationId=presentation_id).execute()
    )
    all_slides = presentation.get("slides", [])
    title_slide = all_slides[0] if all_slides else None
    slides = all_slides[1:]  # content slides
    text_requests = []

    # Step 4: Populate the title slide with presentation title
    if title_slide:
        title_shape_id = None
        subtitle_shape_id = None

        for element in title_slide.get("pageElements", []):
            shape = element.get("shape")
            if not shape:
                continue
            shape_type = shape.get("shapeType", "").lower()
            object_id = element.get("objectId")

            if shape_type == "title" and not title_shape_id:
                title_shape_id = object_id
            elif shape_type == "subtitle" and not subtitle_shape_id:
                subtitle_shape_id = object_id
            elif shape_type == "text_box":
                if not title_shape_id:
                    title_shape_id = object_id
                elif not subtitle_shape_id:
                    subtitle_shape_id = object_id

        if title_shape_id:
            text_requests.append(
                {
                    "insertText": {
                        "objectId": title_shape_id,
                        "text": " ",
                        "insertionIndex": 0,
                    }
                }
            )
            text_requests.append(
                {
                    "insertText": {
                        "objectId": title_shape_id,
                        "text": title,
                        "insertionIndex": 0,
                    }
                }
            )

    # Step 5: Popoulate individual slides with necessary shapes
    for idx, (slide, slide_data) in enumerate(zip(slides, slides_data)):
        title_shape_id = None
        body_shape_id = None

        print(f"\nSlide {idx} elements:")
        for element in slide.get("pageElements", []):
            shape = element.get("shape")
            if not shape:
                continue
            shape_type = shape.get("shapeType", "").lower()
            object_id = element.get("objectId")
            print(f"- objectId: {object_id}, shapeType: {shape_type}")

            if shape_type == "title" and not title_shape_id:
                title_shape_id = object_id
            elif shape_type == "body" and not body_shape_id:
                body_shape_id = object_id
            elif shape_type == "text_box":
                if not title_shape_id:
                    title_shape_id = object_id
                elif not body_shape_id:
                    body_shape_id = object_id

        if title_shape_id and slide_data.get("title"):
            text_requests.append(
                {
                    "insertText": {
                        "objectId": title_shape_id,
                        "text": " ",
                        "insertionIndex": 0,
                    }
                }
            )
            text_requests.append(
                {
                    "insertText": {
                        "objectId": title_shape_id,
                        "text": slide_data["title"],
                        "insertionIndex": 0,
                    }
                }
            )
        else:
            print(f"Slide {idx}: No valid title shape found — skipping title.")

        if body_shape_id and slide_data.get("body"):
            text_requests.append(
                {
                    "insertText": {
                        "objectId": body_shape_id,
                        "text": " ",
                        "insertionIndex": 0,
                    }
                }
            )
            text_requests.append(
                {
                    "insertText": {
                        "objectId": body_shape_id,
                        "text": slide_data["body"],
                        "insertionIndex": 0,
                    }
                }
            )
        else:
            print(f"Slide {idx}: No valid body shape found — skipping body.")

    # Step 6: Insert text
    if text_requests:
        try:
            slides_service.presentations().batchUpdate(
                presentationId=presentation_id, body={"requests": text_requests}
            ).execute()
        except Exception as e:
            raise BatchUpdateError(f"Failed to insert text: {str(e)}")
    else:
        print("No insertText requests generated. The slides may be blank.")

    # Step 7: Make the preso shareable
    try:
        drive_service.permissions().create(
            fileId=presentation_id, body={"type": "anyone", "role": "writer"}
        ).execute()
    except Exception:
        print("Warning: Failed to update sharing permissions.")

    print(
        f"Created presentation: https://docs.google.com/presentation/d/{presentation_id}/edit"
    )


def get_args():
    """
    Parse command-line arguments for the presentation creation process.

    Returns:
        Namespace: Parsed arguments object.
    """
    parser = argparse.ArgumentParser(
        description="Create Google Slides from YAML in TXT format"
    )
    parser.add_argument(
        "--file-name", required=True, help="YAML-formatted .txt file with slide content"
    )
    parser.add_argument(
        "--service-account",
        dest="gcp_application_credentials",
        default=None,
        required=False,
    )
    return parser.parse_args()


def main():
    """
    Entrypoint for the Google Slides creation pipeline.

    Handles:
    - Argument parsing
    - Service account loading
    - Calling the core presentation creation logic
    - Error handling with proper exit codes
    """
    try:
        args = get_args()
        service_account = os.getenv(
            args.gcp_application_credentials, args.gcp_application_credentials
        )
        create_presentation_from_yaml(args.file_name, service_account)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        exit(Presentations.EXIT_CODE_FILE_NOT_FOUND)
    except ExitCodeException as e:
        print(f"Error: {e}")
        exit(e.exit_code)
    except Exception as e:
        print(f"Unknown error: {e}")
        exit(Presentations.EXIT_CODE_UNKNOWN_ERROR)


if __name__ == "__main__":
    main()
