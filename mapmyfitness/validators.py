class BaseValidator(object):
    def __init__(self, obj):
        self.data = obj
        self.errors = {}
        self.items = {}
        self.validate()

    def add_error(self, key, data_name, error):
        if key in self.errors:
            self.errors[key].setdefault(data_name, []).append(error)
        else:
            self.errors[key] = {}
            self.errors[key][data_name] = [error]

    @property
    def valid(self):
        return len(self.errors) == 0

    def __repr__(self):
        if len(self.errors):
            printable_errors = []
            for key in self.errors:
                if isinstance(self.errors[key], list):
                    for error in self.errors[key]:
                        error_sentence = '{0} {1}.'.format(key, error)
                        printable_errors.append(error_sentence)
                else:
                    for data_name in self.errors[key]:
                        for error in self.errors[key][data_name]:
                            error_sentence = '{0} {1} {2}.'.format(key, data_name, error)
                            printable_errors.append(error_sentence)
            return ' '.join(printable_errors)


class RouteValidator(BaseValidator):
    def validate(self):
        pass