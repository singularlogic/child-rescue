# #!/usr/bin/env python
# import os
# import sys
#
# from dotenv import load_dotenv
#
# if __name__ == "__main__":
#     env_path = "../.envs/.local/.django.env"
#     load_dotenv(dotenv_path=env_path)
#
#     try:
#         # Check if settings are set through environment var.
#         os.environ["DJANGO_SETTINGS_MODULE"]
#     except KeyError:
#         staging = (
#             (len(sys.argv) > 1)
#             and (sys.argv[1] is not None)
#             and (sys.argv[1].startswith("staging"))
#         )
#         if staging:
#             os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings.staging")
#         else:
#             os.environ.setdefault(
#                 "DJANGO_SETTINGS_MODULE", "Backend.settings.development"
#             )
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError:
#         # The above import may fail for some other reason. Ensure that the
#         # issue is really that Django is missing to avoid masking other
#         # exceptions on Python 2.
#         try:
#             import django
#         except ImportError:
#             raise ImportError(
#                 "Couldn't import Django. Are you sure it's installed and "
#                 "available on your PYTHONPATH environment variable? Did you "
#                 "forget to activate a virtual environment?"
#             )
#         raise
#     execute_from_command_line(sys.argv)

#!/usr/bin/env python
import os
import sys

from dotenv import load_dotenv

if __name__ == "__main__":
    env_path = "../.envs/.local/.django.env"
    load_dotenv(dotenv_path=env_path)

    try:
        # Check if settings are set through environment var.
        os.environ["DJANGO_SETTINGS_MODULE"]
    except KeyError:
        testing = (len(sys.argv) > 1) and (sys.argv[1] is not None) and (sys.argv[1].startswith("test"))
        if testing:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings.test")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings.production")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    execute_from_command_line(sys.argv)
