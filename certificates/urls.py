"""Certificate routes: the downloadable PDF, and the public verification page.

The verify route is deliberately constrained to the CYB-XXXX-XXXX-XXXX serial
format with a regex. This app is included ahead of authentication in the root
URLconf, and authentication owns the more general `verify/<token>/`; matching
only real serial shapes here means registration-verification links (whose tokens
never look like a serial) fall straight through to the auth view.
"""

from django.urls import path, re_path

from . import views

app_name = "certificates"

_SERIAL = r"(?i:CYB)-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}"

urlpatterns = [
    path("certificate/download/", views.download, name="download"),
    re_path(rf"^verify/(?P<serial>{_SERIAL})/$", views.verify, name="verify"),
]
