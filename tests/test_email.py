import unittest

from app import create_app
from app import email


class EmailTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_content = self.app.app_context()
        self.app_content.push()

    def test_send_email(self):
        email.send_email("qcymkxyc@163.com", "Test Send Email", "mail/test")


if __name__ == '__main__':
    unittest.main()
