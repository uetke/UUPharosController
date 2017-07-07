class device(object):
    def __init__(self, dict):
        for key in dict:
            self.__setattr__(key, dict[key])