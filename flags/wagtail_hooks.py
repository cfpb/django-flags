from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from flags import views


@hooks.register('register_settings_menu_item')
def register_flags_menu():
    return MenuItem('Flags', reverse('flagadmin:list'),
                    classnames='icon icon-tag', order=10000)


@hooks.register('register_admin_urls')
def register_flag_admin_urls():
    return [
        url(r'^flags/',
            include([
                url(r'^$', views.index, name='list'),
                url(r'^(\d+)/delete/$', views.delete,
                    name='delete'),
                url(r'^create/$', views.create, name='create'),
            ], namespace='flagadmin'))
    ]
