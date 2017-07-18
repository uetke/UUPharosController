class device(object):
    def __init__(self, properties):
       self.properties = properties

    def __str__(self):
        if 'name' in self.properties:
            return self.properties['name']
        else:
            return "Device with no name"