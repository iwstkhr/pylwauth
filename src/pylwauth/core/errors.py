class NoneValueError(Exception):
    def __init__(self, key):
        super(NoneValueError, self).__init__(f'{key} must not be None.')
