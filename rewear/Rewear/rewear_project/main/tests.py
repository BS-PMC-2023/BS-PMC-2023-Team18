from django.test import TestCase


# Create your tests here.
# make me tests for the project

class Test(TestCase):
    def test_home(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_areyousure(self):
        response = self.client.get('/areyousure/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_myprofile(self):
        response = self.client.get('/myprofile/')
        self.assertEqual(response.status_code, 200)

    def test_messagetouser(self):
        response = self.client.get('/messagetouser/')
        self.assertEqual(response.status_code, 200)

    def test_sendmessage(self):
        response = self.client.get('/sendmessage/')
        self.assertEqual(response.status_code, 200)

    def test_editabout(self):
        response = self.client.get('/editabout/')
        self.assertEqual(response.status_code, 200)

    def test_saveabout(self):
        response = self.client.get('/saveabout/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        response = self.client.get('/search_page/')
        self.assertEqual(response.status_code, 200)

    def test_market_page(self):
        response = self.client.get('/market_page/')
        self.assertEqual(response.status_code, 200)

    def test_update_market(self):
        response = self.client.get('/update_market/')
        self.assertEqual(response.status_code, 200)

    def test_submissions(self):
        response = self.client.get('/submissions/')
        self.assertEqual(response.status_code, 200)

    def test_submit_request(self):
        response = self.client.get('/submit_request/')
        self.assertEqual(response.status_code, 200)

    def test_feedback(self):
        response = self.client.get('/feedback/')
        self.assertEqual(response.status_code, 200)

    def test_update_profilepic(self):
        response = self.client.get('/update_profilepic/')
        self.assertEqual(response.status_code, 200)

    def test_getUserProfileInfo(self):
        response = self.client.get('/getUserProfileInfo/')
        self.assertEqual(response.status_code, 200)

    def test_toggle_active(self):
        response = self.client.get('/toggle_active/')
        self.assertEqual(response.status_code, 200)