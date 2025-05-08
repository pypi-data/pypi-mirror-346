from googleslides.googleslides import GoogleSlidesClient
import os
import logging


def conn_helper(client: GoogleSlidesClient) -> int:
    try:
        service, drive_service = client.connect()
        logging.info("Successfully connected to Google Sheets")
        return 0
    except Exception as e:
        logging.error("Could not connect to Google Sheets")
        logging.error(e)
        return 1


def test_good_connection():
    client = GoogleSlidesClient(
        service_account_json=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )

    assert conn_helper(client) == 0


def test_bad_connection():
    client = GoogleSlidesClient(service_account_json="bad_credentials")

    assert conn_helper(client) == 1
