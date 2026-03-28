from unittest import TestCase

from django.core.exceptions import ValidationError

from forumApp.posts.validators import BadLanguageValidator


class TestBadLanguageValidator(TestCase):
    def test__bad_words_included__raises_validation_error(self):
        validator = BadLanguageValidator()

        with self.assertRaises(ValidationError) as v:
            validator('crap')

        self.assertEqual(str(v.exception), "['The text contains bad language!']")
