 USE mv;
 DROP TABLE IF EXISTS new_movies;
 CREATE TABLE new_movies (id VARCHAR(10) NOT NULL,title VARCHAR(100) NOT NULL);
 
 alter table new_movies add COLUMN cover_url VARCHAR(200) NOT NULL;
 alter table new_movies add COLUMN genres VARCHAR(100) NOT NULL;
 alter table new_movies add COLUMN color_info VARCHAR(100) DEFAULT NULL;
 alter table new_movies add COLUMN director VARCHAR(100) NOT NULL;
 alter table new_movies add COLUMN cast_1 VARCHAR(50) NOT NULL;
 alter table new_movies add COLUMN cast_2 VARCHAR(50) DEFAULT NULL;
 alter table new_movies add COLUMN cast_3 VARCHAR(50) DEFAULT NULL;
 alter table new_movies add COLUMN countries VARCHAR(200) NOT NULL;
 alter table new_movies add COLUMN languages VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN writer VARCHAR(300) DEFAULT NULL;
 alter table new_movies add COLUMN editor VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN cinematographer VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN art_director VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN costume_designer VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN composer VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN sound_mix VARCHAR(200) DEFAULT NULL;
 alter table new_movies add COLUMN production_companies VARCHAR(200) NOT NULL;
 alter table new_movies add COLUMN year YEAR NOT NULL;
 alter table new_movies add COLUMN runtimes SMALLINT NOT NULL;
 
 alter table new_movies add COLUMN number_of_votes_1 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_2 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_3 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_4 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_5 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_6 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_7 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_8 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_9 SMALLINT NOT NULL;
 alter table new_movies add COLUMN number_of_votes_10 SMALLINT NOT NULL;
  
describe new_movies;
          
 
 
 
 