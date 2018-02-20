class Movie(object):

    def __init__(self):
        self.id = ''
        self.title = ''
        self.cover_url = ''
        self.giant_cover_url = ''
        self.genres = ''
        self.color_info = ''
        self.crews = {}
        self.casts = []
        self.countries = ''
        self.languages = ''
        self.production_companies = ''
        self.year = 1900
        self.runtimes = 60
        self.casts_ranking = 1.1
        self.number_of_votes = []
        # self.budget = 0

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def cover_url(self):
        return self._cover_url

    @property
    def giant_cover_url(self):
        return self._giant_cover_url

    @property
    def genres(self):
        return self._genres

    @property
    def color_info(self):
        return self._color_info

    @property
    def crews(self):
        return self._crews

    @property
    def casts(self):
        return self._casts

    @property
    def countries(self):
        return self._countries

    @property
    def languages(self):
        return self._languages

    @property
    def production_companies(self):
        return self._production_companies

    @property
    def year(self):
        return self._year

    @property
    def runtimes(self):
        return self._runtimes

    @property
    def casts_ranking(self):
        return self._casts_ranking

    # @property
    # def budget(self):
    #     return self._budget

    @property
    def number_of_votes(self):
        return self._number_of_votes
 
    @id.setter
    def id(self, value):
        self._id = value

    @title.setter
    def title(self, value):
        self._title = value

    @cover_url.setter
    def cover_url(self, value):
        self._cover_url = value

    @giant_cover_url.setter
    def giant_cover_url(self, value):
        self._giant_cover_url = value

    @genres.setter
    def genres(self, value):
        self._genres = value

    @color_info.setter
    def color_info(self, value):
        self._color_info = value

    @crews.setter
    def crews(self, value):
        self._crews = value

    @casts.setter
    def casts(self, value):
        self._casts = value

    @countries.setter
    def countries(self, value):
        self._countries = value

    @languages.setter
    def languages(self, value):
        self._languages = value

    @production_companies.setter
    def production_companies(self, value):
        self._production_companies = value

    @year.setter
    def year(self, value):
        self._year = value

    @runtimes.setter
    def runtimes(self, value):
        self._runtimes = value

    @casts_ranking.setter
    def casts_ranking(self, value):
        self._casts_ranking = value

    # @budget.setter
    # def budget(self, value):
    #     self._budget = value

    @number_of_votes.setter
    def number_of_votes(self, value):
        self._number_of_votes = value
