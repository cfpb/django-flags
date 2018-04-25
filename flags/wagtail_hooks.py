from django.conf.urls import include, url

from flags import views


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

try:
    from wagtail.admin.menu import MenuItem
    from wagtail.core import hooks
except ImportError:
    from wagtail.wagtailadmin.menu import MenuItem
    from wagtail.wagtailcore import hooks


@hooks.register('register_settings_menu_item')
def register_flags_menu():
    return MenuItem('Flags', reverse('flagadmin:list'),
                    classnames='icon icon-tag', order=10000)


@hooks.register('register_admin_urls')
def register_flag_admin_urls():
    return [
        url(r'^flags/',
            include(([
                url(r'^$', views.index, name='list'),
                url(r'^(\d+)/delete/$', views.delete,
                    name='delete'),
                url(r'^create/$', views.create, name='create'),
            ], 'flags'), namespace='flagadmin'))
    ]
