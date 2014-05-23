class Model(object):

    def __init__(self, properties):
        self.properties = properties

    def get(self, prop):
        if prop in self.properties:
            return self.properties[prop]
        elif "defaultmodel" in self.properties:
            return self.get("defaultmodel").get(prop)
        else:
            return None

    def set(self, prop, value):
        self.properties[prop] = value
