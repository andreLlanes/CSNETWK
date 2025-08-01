import unittest
from core.messages import parse_message, create_profile_message, create_post_message

class TestMessageFormat(unittest.TestCase):

    def test_parse_message(self):
        message = "TYPE: PROFILE\nUSER_ID: andre@192.168.1.8\nDISPLAY_NAME: Andre\nSTATUS: Active"
        parsed_message = parse_message(message)
        self.assertEqual(parsed_message['TYPE'], 'PROFILE')
        self.assertEqual(parsed_message['USER_ID'], 'andre@192.168.1.8')
        self.assertEqual(parsed_message['STATUS'], 'Active')

    def test_create_profile_message(self):
        message = create_profile_message('andre@192.168.1.8', 'Andre', 'Active')
        self.assertIn("TYPE: PROFILE", message)
        self.assertIn("USER_ID: andre@192.168.1.8", message)

    def test_create_post_message(self):
        message = create_post_message('andre@192.168.1.8', 'Hello, po!', 3600)
        self.assertIn("TYPE: POST", message)
        self.assertIn("USER_ID: andre@192.168.1.8", message)
        self.assertIn("CONTENT: Hello, po!", message)

if __name__ == "__main__":
    unittest.main()
