import logging
import re
import uuid
from mailosaur import MailosaurClient
from mailosaur.models import SearchCriteria
from data.config import server_id, mailosaur_api_key

logger = logging.getLogger(__name__)
mailosaur = MailosaurClient(mailosaur_api_key)
server_id = server_id


def generate_email_address():
    """Generates a unique email address for testing."""
    return f"user-{uuid.uuid4()}@{server_id}.mailosaur.net"


def get_email(email_address):
    """Retrieves the latest email sent to a specific email address."""
    logger.info("Retrieving email for address: %s", email_address)
    criteria = SearchCriteria()
    criteria.sent_to = email_address
    return mailosaur.messages.get(server_id, criteria)


def extract_token_from_email(email):
    """Extracts a 6-digit token from the email body."""
    email_body = email.html.body
    match = re.search(r"<strong>(\d{6})</strong>", email_body)
    return match.group(1) if match else None


def verify_email_subject(email, expected_text):
    """Verifies the email subject contains expected text."""
    return expected_text in email.subject


def verify_email_body(email, expected_text):
    """Verifies the email body contains expected text."""
    return expected_text in email.text.body


def extract_link_from_email(email):
    """Extracts the first link from the email body."""
    return email.text.links[0].href


def delete_email(email):
    """Deletes an email from the Mailosaur server."""
    mailosaur.messages.delete(email.id)
