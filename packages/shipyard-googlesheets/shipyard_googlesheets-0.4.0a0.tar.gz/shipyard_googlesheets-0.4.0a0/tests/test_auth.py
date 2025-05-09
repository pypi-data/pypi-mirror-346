import os
from shipyard_googlesheets import GoogleSheetsClient
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())


def conn_helper(client: GoogleSheetsClient) -> int:
    try:
        service, drive_service = client.connect()
        logging.info("Successfully connected to Google Sheets")
        return 0
    except Exception as e:
        logging.error("Could not connect to Google Sheets")
        return 1


def test_good_connection():
    client = GoogleSheetsClient(
        service_account=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )

    assert conn_helper(client) == 0


def test_bad_connection():
    client = GoogleSheetsClient(service_account="bad_credentials")

    assert conn_helper(client) == 1
