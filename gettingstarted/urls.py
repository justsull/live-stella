from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^stella/', hello.views.predict, name='predict'),
    url(r'^slack/', hello.views.slack_predict, name='slack_predict'),
    path('admin/', admin.site.urls),
]
