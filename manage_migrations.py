import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamline_be.settings")
django.setup()

from django.core.management import call_command
from django.apps import apps


def make_and_apply_migrations():
    for app in apps.get_app_configs():
        migrations_dir = os.path.join(app.path, 'migrations')
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
            init_file = os.path.join(migrations_dir, '__init__.py')
            open(init_file, 'a').close()

        try:
            call_command('makemigrations', app.label)
            print(f"Created migrations for {app.label}")
        except Exception as e:
            print(f"Failed to create migrations for {app.label}: {str(e)}")

        try:
            call_command('migrate', app.label)
            print(f"Applied migrations for {app.label}")
        except Exception as e:
            print(f"Failed to apply migrations for {app.label}: {str(e)}")


if __name__ == '__main__':
    make_and_apply_migrations()
