from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

# This will be maintained by register() as a global dictionary of
# condition_name: [list of functions], so we can have multiple conditions
# for a given name and they all must pass when checking.
CONDITIONS = {}


class RequiredForCondition(Exception):
    """ Raised when a kwarg that is required for a condition is not given """


def register(condition_name, fn=None):
    """ Register a condition to test for flag state. Can be decorator.
    Conditions can be any callable that takes a value and some number of
    required arguments (specified in 'requires') that were passed as kwargs
    when checking the flag state. """
    global CONDITIONS

    # Don't be a decorator, just register
    if fn is None:
        # Be a decorator
        def decorator(fn):
            register(condition_name, fn=fn)
            return fn
        return decorator

    if condition_name not in CONDITIONS:
        CONDITIONS[condition_name] = []

    CONDITIONS[condition_name].append(fn)


def get_conditions():
    """ Return the names of all available conditions """
    return CONDITIONS.keys()


def get_condition(condition_name):
    """ Generator to fetch condition checkers from the registry """
    if condition_name not in CONDITIONS:
        raise StopIteration
    for condition_fn in CONDITIONS[condition_name]:
        yield condition_fn


@register('boolean')
def boolean_condition(condition, **kwargs):
    """ Basic boolean check """
    try:
        if condition.lower() == 'true':
            return True
        return False
    except AttributeError:
        return bool(condition)


@register('user')
def user_condition(username, request=None, **kwargs):
    """ Does request.user match the expected username? """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'user'")

    User = apps.get_model('auth', 'User')
    try:
        return request.user == User.objects.get(username=username)
    except ObjectDoesNotExist:
        return False


@register('anonymous')
def anonymous_condition(boolean_value, request=None, **kwargs):
    """ request.user an anonymous user, true or false based on boolean_value
    """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'anonymous'")

    return bool(boolean_value) == bool(request.user.is_anonymous())


@register('parameter')
def parameter_condition(param_name, request=None, **kwargs):
    """ is the parameter name part of the GET parameters? """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'parameter'")

    return request.GET.get(param_name) == 'True'


@register('path')
def path_condition(path, request=None, **kwargs):
    """ Does the request's path match the given path? """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'path'")

    return request.path.startswith(path)


@register('site')
def site_condition(site_str, request=None, **kwargs):
    """ Does the requests's Wagtail Site match the given site?
    site_str should be 'hostname:port', or 'hostname [default]'. """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'site'")

    Site = apps.get_model('wagtailcore.Site')

    if '[default]' in site_str:
        # Wagtail Sites on the default port have [default] at the end of
        # their str() form.
        site_str = site_str.replace(' [default]', ':80')
    elif ':' not in site_str:
        # Add a default port if one isn't given
        site_str += ':80'

    hostname, port = site_str.split(':')
    try:
        conditional_site = Site.objects.get(hostname=hostname, port=port)
    except ObjectDoesNotExist:
        return False

    try:
        site = Site.find_for_request(request)
    except AttributeError:
        # We can't do anything with this
        return False

    return conditional_site == site
