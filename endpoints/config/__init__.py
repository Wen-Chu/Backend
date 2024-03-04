import os

if os.environ.get('FLASK_ENV') == 'production':
    from .production import *
elif os.environ.get('FLASK_ENV') == 'testing':
    from .testing import *
else:
    from .development import *