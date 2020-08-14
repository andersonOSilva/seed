from django.db import models

import crypt


class User(models.Model):
    """
    Model de usuários.
    """
    class Meta:

        db_table = 'user'

    username = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    def check_password(self, password):
        if self.password == crypt.crypt(password,"$6$salt$"):
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        # codifica password
        self.password = crypt.crypt(self.password,"$6$salt$")
        super(User, self).save(*args, **kwargs)
