class Movie(object):

    def __init__(self):
        self.id = ''
        self.title = ''

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @id.setter
    def id(self, value):
        self._id = value

    @title.setter
    def title(self, value):
        self._title = value