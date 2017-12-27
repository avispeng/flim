CREATE DATABASE IF NOT EXISTS flim;
USE flim;

CREATE TABLE IF NOT EXISTS users
(
userid INT NOT NULL AUTO_INCREMENT,
username CHAR(20) NOT NULL,
hashed_pwd CHAR(64) NOT NULL,
salt CHAR(8) NOT NULL,
email CHAR(254) NULL, # max length of email address is 254
location CHAR(30) NULL,
user_profile JSON NULL,
PRIMARY KEY (userid)
);

CREATE TABLE IF NOT EXISTS movies
(
movie_no INT NOT NULL AUTO_INCREMENT, # unique id for the movie
imdb_id CHAR(9) NOT NULL, # tt0123456
movie_title CHAR(100) NOT NULL,
rating FLOAT NULL,
movie_profile JSON NULL, # JSON object, like a python dictionary
release_date CHAR(10) NULL, # 2017-12-26
genres JSON NULL, # JSON array, like a python list
poster CHAR(15) NULL, # imdb_id + extension
PRIMARY KEY (movie_no)
);

CREATE TABLE IF NOT EXISTS reviews
(
review_no INT NOT NULL AUTO_INCREMENT,
movie_no INT NOT NULL,
username CHAR(20) NOT NULL,
review_title CHAR(100) NULL,
review VARCHAR(10000) NOT NULL,
thumb_up INT NOT NULL,
time_stamp CHAR(26) NOT NULL, # 2017-12-26 21:59:00.138372
PRIMARY KEY (review_no)
);

CREATE TABLE IF NOT EXISTS comments
(
comment_no INT NOT NULL AUTO_INCREMENT,
review_no INT NOT NULL,
floor INT NOT NULL,
reply_to INT NULL,
username CHAR(20) NOT NULL,
content VARCHAR(2000) NOT NULL,
thumb_up INT NOT NULL,
time_stamp CHAR(26) NOT NULL,
PRIMARY KEY (comment_no)
);

CREATE TABLE IF NOT EXISTS ratings
(
rating_no INT NOT NULL AUTO_INCREMENT,
movie_no INT NOT NULL,
username CHAR(20) NOT NULL,
rating FLOAT NULL,
tags JSON NULL,
PRIMARY KEY (rating_no)
);