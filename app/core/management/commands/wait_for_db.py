import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """django command to pause execution until database is available"""
    def handle(self,*args,**options):
        self.stdout.write('waiting for database to available')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('database connection not available')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('database connection available'))
