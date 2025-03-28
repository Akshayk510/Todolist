from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Sets up the database by applying migrations and creating necessary tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database setup...'))
        
        # Apply migrations
        self.stdout.write('Applying migrations...')
        call_command('migrate')
        
        # Check if priority column exists
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(todo_task)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'priority' not in columns:
                self.stdout.write(self.style.WARNING('Priority column not found. Make sure to run migrations.'))
            else:
                self.stdout.write(self.style.SUCCESS('Priority column exists.'))
                
            if 'category' not in columns:
                self.stdout.write(self.style.WARNING('Category column not found. Make sure to run migrations.'))
            else:
                self.stdout.write(self.style.SUCCESS('Category column exists.'))
        
        self.stdout.write(self.style.SUCCESS('Database setup complete!'))