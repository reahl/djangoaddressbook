import os
from django.db import models


class UserError(Exception):
    pass


class ConcurrencyError(Exception):
    pass


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=254, unique=True)
    _version = models.IntegerField(default=0)

    def do_something_complicated(self):
        self.name += '-complicated' #is breaking, rollback will nuke change
        if 'ADDRESS_BREAK' in os.environ:
            raise UserError('Address domain breakage')
        else:
            print('Doing something complicated')

    def save(self, *args, **kwargs):
        cls = self.__class__
        if self.id:
            update = cls.objects.filter(
                id=self.id, _version=self._version).update(_version=self._version + 1)
            if not update:
                raise ConcurrencyError('The item you are editing has changed. Please refresh.')
            self._version += 1
        super().save(*args, **kwargs)
