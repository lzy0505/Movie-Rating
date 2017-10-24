class Movie(object):

    def __init__(self):
        self.id = ''
        self.title = ''
        self.cover_url = ''
        self.giant_cover_url = ''
        self.genres = ''
        self.color_info = ''
        self.director = ''
        self.cast_1st = ''
        self.cast_2nd = ''
        self.cast_3rd = ''
        self.countries = ''
        self.languages = ''
        self.writer = ''
        self.editor = ''
        self.cinematographer = ''
        self.art_director = ''
        self.costume_designer = ''
        self.original_music = ''
        self.sound_mix = ''
        self.production_companies = ''
        self.year = 1900
        self.runtimes = 60
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
    def director(self):
        return self._director

    @property
    def cast_1st(self):
        return self._cast_1st

    @property
    def cast_2nd(self):
        return self._cast_2nd

    @property
    def cast_3rd(self):
        return self._cast_3rd

    @property
    def countries(self):
        return self._countries

    @property
    def languages(self):
        return self._languages

    @property
    def writer(self):
        return self._writer

    @property
    def editor(self):
        return self._editor

    @property
    def cinematographer(self):
        return self._cinematographer
    
    @property
    def art_director(self):
        return self._art_director

    @property
    def costume_designer(self):
        return self._costume_designer

    @property
    def original_music(self):
        return self._original_music

    @property
    def sound_mix(self):
        return self._sound_mix

    @property
    def production_companies(self):
        return self._production_companies

    @property
    def year(self):
        return self._year

    @property
    def runtimes(self):
        return self._runtimes

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

    @director.setter
    def director(self, value):
        self._director = value

    @cast_1st.setter
    def cast_1st(self, value):
        self._cast_1st = value

    @cast_2nd.setter
    def cast_2nd(self, value):
        self._cast_2nd = value

    @cast_3rd.setter
    def cast_3rd(self, value):
        self._cast_3rd = value

    @countries.setter
    def countries(self, value):
        self._countries = value

    @languages.setter
    def languages(self, value):
        self._languages = value

    @writer.setter
    def writer(self, value):
        self._writer = value

    @editor.setter
    def editor(self, value):
        self._editor = value

    @cinematographer.setter
    def cinematographer(self, value):
        self._cinematographer = value

    @art_director.setter
    def art_director(self, value):
        self._art_director = value

    @costume_designer.setter
    def costume_designer(self, value):
        self._costume_designer = value

    @original_music.setter
    def original_music(self, value):
        self._original_music = value

    @sound_mix.setter
    def sound_mix(self, value):
        self._sound_mix = value

    @production_companies.setter
    def production_companies(self, value):
        self._production_companies = value

    @year.setter
    def year(self, value):
        self._year = value

    @runtimes.setter
    def runtimes(self, value):
        self._runtimes = value

    # @budget.setter
    # def budget(self, value):
    #     self._budget = value

    @number_of_votes.setter
    def number_of_votes(self, value):
        self._number_of_votes = value
