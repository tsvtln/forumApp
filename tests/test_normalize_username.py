"""
Test suite for normalize_username functionality in AppUser model.

This tests the Unicode NFKC normalization that prevents homograph attacks
and ensures consistent username storage across different systems.
"""
import unicodedata
from django.test import TestCase
from forumApp.accounts.models import AppUser


class NormalizeUsernameTests(TestCase):
    """Test cases for the normalize_username classmethod."""

    def test_normalize_username_method_exists(self):
        """Test that the normalize_username method exists on AppUser."""
        self.assertTrue(
            hasattr(AppUser, 'normalize_username'),
            "AppUser should have normalize_username method"
        )

    def test_normalize_username_simple_string(self):
        """Test normalization of a simple ASCII string."""
        username = 'testuser'
        normalized = AppUser.normalize_username(username)
        self.assertEqual(normalized, 'testuser')

    def test_normalize_username_with_accents(self):
        """Test normalization of usernames with accented characters."""
        username = 'café'
        normalized = AppUser.normalize_username(username)
        # Verify it returns a normalized form
        self.assertEqual(normalized, unicodedata.normalize('NFKC', 'café'))

    def test_normalize_username_empty_string(self):
        """Test that empty string is handled correctly."""
        normalized = AppUser.normalize_username('')
        self.assertEqual(normalized, '')

    def test_normalize_username_none(self):
        """Test that None is handled correctly."""
        normalized = AppUser.normalize_username(None)
        self.assertIsNone(normalized)

    def test_normalize_username_unicode_characters(self):
        """Test normalization of various Unicode characters."""
        test_cases = [
            ('café', unicodedata.normalize('NFKC', 'café')),
            ('naïve', unicodedata.normalize('NFKC', 'naïve')),
            ('José', unicodedata.normalize('NFKC', 'José')),
        ]

        for original, expected in test_cases:
            with self.subTest(username=original):
                normalized = AppUser.normalize_username(original)
                self.assertEqual(normalized, expected)

    def test_normalize_username_homograph_prevention(self):
        """Test that homograph characters remain distinct after normalization.

        Note: NFKC normalization ensures consistent Unicode representation but does NOT
        transliterate between scripts (e.g., Cyrillic to Latin). This test verifies that
        the normalization is applied consistently, which is the first step in preventing
        homograph attacks. Application-level validation should additionally check for
        mixed-script usernames if needed.
        """
        # Cyrillic 'а' (U+0430) looks like Latin 'a' (U+0061)
        cyrillic_a = '\u0430'  # Cyrillic small letter a
        latin_a = 'a'  # Latin small letter a

        # Each should be normalized consistently with itself
        normalized_cyrillic = AppUser.normalize_username(f'{cyrillic_a}dmin')
        normalized_latin = AppUser.normalize_username(f'{latin_a}dmin')

        # They remain distinct (NFKC doesn't transliterate)
        self.assertNotEqual(normalized_cyrillic, normalized_latin)

        # But each normalizes consistently with itself
        self.assertEqual(
            AppUser.normalize_username(f'{cyrillic_a}dmin'),
            AppUser.normalize_username(f'{cyrillic_a}dmin')
        )
        self.assertEqual(
            AppUser.normalize_username(f'{latin_a}dmin'),
            AppUser.normalize_username(f'{latin_a}dmin')
        )


class UserCreationWithNormalizationTests(TestCase):
    """Test cases for user creation with username normalization."""

    def test_manager_exists(self):
        """Test that the custom manager is properly configured."""
        self.assertTrue(
            hasattr(AppUser, 'objects'),
            "AppUser should have objects manager"
        )
        self.assertEqual(
            type(AppUser.objects).__name__,
            'AppUserManager',
            "Manager should be AppUserManager"
        )

    def test_create_user_with_simple_username(self):
        """Test creating a user with a simple ASCII username."""
        user = AppUser.objects.create_user(
            username='john_doe',
            email='john@example.com',
            password='securepass123'
        )

        self.assertEqual(user.username, 'john_doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertTrue(user.has_usable_password())

    def test_create_user_with_unicode_username(self):
        """Test creating a user with Unicode characters in username."""
        user = AppUser.objects.create_user(
            username='café_user',
            email='cafe@example.com',
            password='testpass'
        )

        # Username should be stored in normalized form
        expected_normalized = unicodedata.normalize('NFKC', 'café_user')
        self.assertEqual(user.username, expected_normalized)
        self.assertEqual(user.email, 'cafe@example.com')

    def test_password_is_hashed(self):
        """Test that passwords are properly hashed, not stored in plain text."""
        password = 'securepass123'
        user = AppUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=password
        )

        # Password should not be stored as plain text
        self.assertNotEqual(user.password, password)
        # Password should be hashed (starts with algorithm identifier)
        self.assertTrue(user.password.startswith('pbkdf2_'))
        # Check password should work
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Test creating a superuser with normalized username."""
        superuser = AppUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )

        self.assertEqual(superuser.username, 'admin')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_authentication(self):
        """Test that user authentication works with normalized usernames."""
        password = 'testpass123'
        user = AppUser.objects.create_user(
            username='authuser',
            email='auth@example.com',
            password=password
        )

        # Test correct password
        self.assertTrue(user.check_password(password))

        # Test incorrect password
        self.assertFalse(user.check_password('wrongpass'))

    def test_user_str_method(self):
        """Test that __str__ returns the email address."""
        user = AppUser.objects.create_user(
            username='strtest',
            email='strtest@example.com',
            password='pass123'
        )

        self.assertEqual(str(user), 'strtest@example.com')


class UnicodeNormalizationSecurityTests(TestCase):
    """Test cases for security aspects of Unicode normalization."""

    def test_nfkc_normalization_applied(self):
        """Test that NFKC normalization is specifically applied."""
        # Test characters that differ between NFC and NFKC
        test_string = 'ﬁle'  # Contains ligature fi (U+FB01)
        normalized = AppUser.normalize_username(test_string)

        # NFKC should decompose the ligature
        nfkc_result = unicodedata.normalize('NFKC', test_string)
        self.assertEqual(normalized, nfkc_result)

    def test_combining_characters_normalized(self):
        """Test that combining characters are properly normalized."""
        # e + combining acute accent vs precomposed é
        combining = 'e\u0301'  # e + combining acute
        precomposed = 'é'       # precomposed é

        norm_combining = AppUser.normalize_username(combining)
        norm_precomposed = AppUser.normalize_username(precomposed)

        # Both should normalize to the same form
        self.assertEqual(norm_combining, norm_precomposed)

    def test_whitespace_normalization(self):
        """Test that different whitespace characters are normalized."""
        # Non-breaking space (U+00A0) should be normalized
        username_with_nbsp = 'user\u00A0name'
        normalized = AppUser.normalize_username(username_with_nbsp)

        # NFKC should normalize non-breaking space
        expected = unicodedata.normalize('NFKC', username_with_nbsp)
        self.assertEqual(normalized, expected)


class ManagerIntegrationTests(TestCase):
    """Test the integration between manager and normalize_username."""

    def test_manager_calls_normalize_username(self):
        """Test that the manager actually uses normalize_username."""
        # Create user with Unicode username
        username = 'tëst_üser'
        user = AppUser.objects.create_user(
            username=username,
            email='test@example.com',
            password='pass123'
        )

        # Username should be normalized
        expected = unicodedata.normalize('NFKC', username)
        self.assertEqual(user.username, expected)

    def test_multiple_users_with_similar_unicode(self):
        """Test that similar-looking Unicode usernames are handled correctly."""
        # Create first user
        user1 = AppUser.objects.create_user(
            username='café1',
            email='cafe1@example.com',
            password='pass123'
        )

        # Create second user with different Unicode representation
        user2 = AppUser.objects.create_user(
            username='café2',
            email='cafe2@example.com',
            password='pass123'
        )

        # Both usernames should be normalized
        self.assertEqual(
            user1.username,
            unicodedata.normalize('NFKC', 'café1')
        )
        self.assertEqual(
            user2.username,
            unicodedata.normalize('NFKC', 'café2')
        )
