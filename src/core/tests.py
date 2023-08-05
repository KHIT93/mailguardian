from django.test import TestCase
from faker import Faker
from core.models import User, MailScannerHost, ApplicationNotification

# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()

    def generate_user_values(self, defaults:dict={}) -> User:
        """ Abstraction of the process for providing fake values for
        a new user
        Provide the `defaults` argument for setting specific values for oe or more fields
        """
        values = {
            'first_name': defaults.get('first_name', self.faker.first_name()),
            'last_name': defaults.get('last_name', self.faker.last_name()),
            'email': defaults.get('email', self.faker.email()),
            'date_joined': defaults.get('date_joined', self.faker.date_time()),
            'custom_spam_score': defaults.get('custom_spam_score', self.faker.random_int(min=0, max=10)),
            'custom_spam_highscore': defaults.get('custom_spam_highscore', self.faker.random_int(min=11, max=50)),
        }
        return values

    def test_create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.faker.email()
        date_joined = self.faker.date_time()
        custom_spam_score = self.faker.random_int(min=0, max=10)
        custom_spam_highscore = self.faker.random_int(min=11, max=50)
        
        user = User.objects.create(**{
            'first_name' : first_name,
            'last_name' : last_name,
            'email' : email,
            'date_joined' : date_joined,
            'custom_spam_score' : custom_spam_score,
            'custom_spam_highscore' : custom_spam_highscore,
        })

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.date_joined, date_joined)
        self.assertEqual(user.custom_spam_score, custom_spam_score)
        self.assertEqual(user.custom_spam_highscore, custom_spam_highscore)

    def test_user_has_full_name(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        user = User.objects.create(**self.generate_user_values({
            'first_name': first_name,
            'last_name': last_name
        }))

        self.assertEqual(user.get_full_name(), '%s %s' % (first_name, last_name))

    def test_set_user_password(self):
        pass