from enum import Enum

import jsonpickle


class JsonEnumHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    # Specify that when we encode enums, we simply put the numerical value
    def flatten(self, obj: Enum, data):
        return obj.value

