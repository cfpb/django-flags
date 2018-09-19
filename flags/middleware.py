from __future__ import absolute_import

from flags.settings import get_flags


class FlagConditionsMiddleware(object):
    """
    Simple middleware that adds all available feature flag conditions to the
    request so that flag state can be checked.
    """

    def process_request(self, request):
        request.FLAG_CONDITIONS = get_flags()
