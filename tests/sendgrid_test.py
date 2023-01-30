import os
import unittest

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class TestSendGridSetup(unittest.TestCase):
    def setUp(self):
        self.sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        self.sender = os.environ["SENDER_EMAIL"]
        self.message = Mail(
            from_email=self.sender,
            to_emails=self.sender,
            subject="Test",
            html_content="Testing sendgrid api config.",
        )

    def test_sendgrid_api_config(self):
        try:
            response = self.sg.send(self.message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

        self.assertEqual(response.status_code, 202)
