import os
from django.db import models


class UserError(Exception):
    pass


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=254, unique=True)

    def do_something_complicated(self):
        self.name += '-complicated' #is breaking, rollback will nuke change
        if 'ADDRESS_BREAK' in os.environ:
            raise UserError('Address domain breakage')
        else:
            print('Doing something complicated')