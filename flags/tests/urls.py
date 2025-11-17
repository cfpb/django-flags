from django.urls import include, path

import debug_toolbar


urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
]
