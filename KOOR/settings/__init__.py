from .local import Local
from .development import Development
from .production import Production

# To make the setting variable accessible in the project.
DJANGO_CONFIGURATION = Local