# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "shipyard-googlesheets",
#     "shipyard-templates>=0.9.0"
# ]
# ///
import os
import sys

from shipyard_templates import ShipyardLogger

from ..googleslides import GoogleSlidesClient

logger = ShipyardLogger.get_logger()


def main():
    try:
        credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        credentials = credentials.replace("\n", "\\n")

        GoogleSlidesClient(service_account_json=credentials).connect()
        logger.authtest("Successfully connected to google slides")
        sys.exit(0)
    except Exception as e:
        logger.authtest(
            f"Could not connect to Google Slides with the Service Account provided due to {e}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
