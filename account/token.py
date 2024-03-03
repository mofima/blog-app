from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six 

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    # purpose of this method is to define how the hash value for the token is generated
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

# This instance will be used to generate and check activation tokens.
account_activation_token = AccountActivationTokenGenerator()    