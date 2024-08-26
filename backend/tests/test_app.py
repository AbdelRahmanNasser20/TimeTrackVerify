# import unittest
# from app import create_app

# class AppTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.client = self.app.test_client()
#         self.app.config['TESTING'] = True

#     def test_get_message(self):
#         response = self.client.get('/api/message')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Hello from Flask!', response.get_data(as_text=True))

#     def test_get_time(self):
#         response = self.client.get('/api/time')
#         self.assertEqual(response.status_code, 200)

#     def test_get_status(self):
#         response = self.client.get('/api/status')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Everything is running smoothly!', response.get_data(as_text=True))

# if __name__ == '__main__':
#     unittest.main()


