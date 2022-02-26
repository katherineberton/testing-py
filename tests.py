"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        #does route"/" contain "Please RSVP" in the body anywhere if no rsvp has been submitted?
        result = self.client.get("/")
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)


    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        #does the resultant page have RSVP in it? we want the answer to be no
        #does ther resultant page have party deatils in it? we want the answer to be yes
        self.assertNotIn(b'Please RSVP', result.data)
        self.assertIn(b'Party Details', result.data)


    def test_rsvp_mel(self):
        """Can we keep Mel out?"""


        #possibly use the is_mel() fct to trigger when true on a rewrite


        rsvp_info = {'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"}
        rsvp_info_2 = {'name': "Mel Melitpolski"}
        rsvp_info_3 = {'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertNotIn(b'Party Details', result.data)

        result = self.client.post("/rsvp", data=rsvp_info_2,
                                  follow_redirects=True)

        self.assertNotIn(b'Party Details', result.data)

        result = self.client.post("/rsvp", data=rsvp_info_3,
                                  follow_redirects=True)

        self.assertNotIn(b'Party Details', result.data)


if __name__ == "__main__":

    unittest.main(verbosity=2)
