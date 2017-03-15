# -*- coding: utf-8 -*-

from django.conf import settings
from django.test.utils import override_settings
from django.urls.base import reverse

from survey.tests.base_test import BaseTest


class TestSurveyAuthRequired(BaseTest):

    """ Permit to check if SURVEY_AUTH_REQUIRED is working as intended. """

    URLS = [
        reverse("home"),
        reverse("survey_detail", kwargs={"id": 1}),
        reverse("survey_detail", kwargs={"id": 2}),
    ]

    def assert_accessible(self, url):
        """ Assert that everything is accessible. """
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.login()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.logout()

    @override_settings(SURVEY_AUTH_REQUIRED=True)
    def test_true(self):
        """ If SURVEY_AUTH_REQUIRED=True user need to authenticate. """
        for url in TestSurveyAuthRequired.URLS:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(settings.LOGIN_URL in response["location"])
                self.login()
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.logout()

    @override_settings(SURVEY_AUTH_REQUIRED=False)
    def test_false(self):
        """ If SURVEY_AUTH_REQUIRED=False user do not need to authenticate. """
        for url in TestSurveyAuthRequired.URLS:
            self.assert_accessible(url)

    @override_settings()
    def test_undefined(self):
        """ If nothing is configurated users do not need to authenticate."""
        del settings.SURVEY_AUTH_REQUIRED
        for url in TestSurveyAuthRequired.URLS:
            self.assert_accessible(url)
