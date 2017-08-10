class Movie(object):

    def __init__(self):
        self.id = ''
        self.title = ''
        self.cover_url = ''
        self.genres = ''
        self.color_info = ''
        self.director = ''
        self.cast_1 = ''
        self.cast_2 = ''
        self.cast_3 = ''
        self.countries = ''
        self.languages = ''
        self.writer = ''
        self.editor = ''
        self.cinematographer = ''
        self.art_direction = ''
        self.costume_designer = ''
        self.original_music = ''
        self.sound_mix = ''
        self.production_companies = ''
        self.year = 1900
        self.runtimes = 60

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
    def genres(self):
        return self._genres

    @property
    def color_info(self):
        return self._color_info

    @property
    def director(self):
        return self._director

    @property
    def cast_1(self):
        return self._cast_1

    @property
    def cast_2(self):
        return self._cast_2

    @property
    def cast_3(self):
        return self._cast_3

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
    def art_direction(self):
        return self._art_direction

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

    @genres.setter
    def genres(self, value):
        self._genres = value

    @color_info.setter
    def color_info(self, value):
        self._color_info = value

    @director.setter
    def director(self, value):
        self._director = value

    @cast_1.setter
    def cast_1(self, value):
        self._cast_1 = value

    @cast_2.setter
    def cast_2(self, value):
        self._cast_2 = value

    @cast_3.setter
    def cast_3(self, value):
        self._cast_3 = value

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

    @art_direction.setter
    def art_direction(self, value):
        self._art_direction = value

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

    @number_of_votes.setter
    def number_of_votes(self, value):
        self._number_of_votes = value
