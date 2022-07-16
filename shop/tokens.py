from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.six import text_type
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,customer,timestamp):
        return (
        text_type(customer.pk) + text_type(timestamp)
        # text_type(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()