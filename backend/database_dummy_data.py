"""
This module is used to set up a dummy database
It uses the definitions of the api module and adds dummy data to the database
"""

import datetime
import api
from database.models import Category, Movie, Review

DB = api.DB

# set up the environment
DB.create_all()
DB.session.rollback()

# create the categories
CATEGORY_1 = Category(
    title="Thriller"
)

CATEGORY_2 = Category(
    title="War"
)

CATEGORY_3 = Category(
    title="Adventure"
)

CATEGORY_4 = Category(
    title="Animation"
)

CATEGORY_5 = Category(
    title="Action"
)

CATEGORY_6 = Category(
    title="Kids & Family"
)

DB.session.add(CATEGORY_1)
DB.session.add(CATEGORY_2)
DB.session.add(CATEGORY_3)
DB.session.add(CATEGORY_4)
DB.session.add(CATEGORY_5)
DB.session.add(CATEGORY_6)
DB.session.commit()

# create the movies
MOVIE_1 = Movie(
    title="Léon: The professional",
    director="Luc Besson",
    length=6600,
    release_date=datetime.datetime(1999, 9, 14),
    category_id=CATEGORY_1.id
)

MOVIE_2 = Movie(
    title="Apocalypse Now",
    director="Francis Coppola",
    length=7380,
    release_date=datetime.datetime(1997, 8, 15),
    category_id=CATEGORY_2.id
)

MOVIE_3 = Movie(
    title="Spider-Man: No Way Home",
    director="Jon Watts",
    length=8880,
    release_date=datetime.datetime(2021, 12, 13),
    category_id=CATEGORY_3.id
)

MOVIE_4 = Movie(
    title="Frozen",
    director="Chris Buck",
    length=6120,
    release_date=datetime.datetime(2013, 11, 19),
    category_id=CATEGORY_4.id
)

MOVIE_5 = Movie(
    title="Red Notice",
    director="Rawson Marshall Thurber",
    length=7080,
    release_date=datetime.datetime(2021, 11, 5),
    category_id=CATEGORY_5.id
)

MOVIE_6 = Movie(
    title="Encanto",
    director="Jared Bush, Bryon Howard",
    length=5940,
    release_date=datetime.datetime(2021, 11, 24),
    category_id=CATEGORY_5.id
)



DB.session.add(MOVIE_1)
DB.session.add(MOVIE_2)
DB.session.add(MOVIE_3)
DB.session.add(MOVIE_4)
DB.session.add(MOVIE_5)
DB.session.add(MOVIE_6)
DB.session.commit()

# create the reviews
REVIEW_1 = Review(
    rating=4,
    comment="The film is almost perfect but I don’t like Natalie Portman",
    date=datetime.datetime(2016, 9, 10),
    author="dummyGuy",
    movie_id=MOVIE_1.id
)

REVIEW_2 = Review(
    rating=5,
    comment="Such a masterpiece! I love helicopters",
    date=datetime.datetime(2018, 5, 23),
    author="dummyGuy",
    movie_id=MOVIE_2.id
)

REVIEW_3 = Review(
    rating=5,
    comment="Amazing movie! This movie was amazing! Both me and my kids loved it! "
            "There is a little more brutal action than the other movies so be prepared for that.",
    date=datetime.datetime(2021, 12, 20),
    author="grantorinohurricane",
    movie_id=MOVIE_3.id
)

REVIEW_4 = Review(
    rating=4,
    comment="Will melt the iciest of hearts, the best animated film of 2013 by "
            "a mile and one of Disney's best in recent years.",
    date=datetime.datetime(2014, 3, 15),
    author="grantorinohurricane",
    movie_id=MOVIE_4.id
)

REVIEW_5 = Review(
    rating=5,
    comment="My girls totally love it! Been watching with them every weekend now "
            "(seems boring now), yet my kids every time feel rejuvenated after watching it.",
    date=datetime.datetime(2015, 5, 31),
    author="lightningbasketball",
    movie_id=MOVIE_4.id
)

REVIEW_6 = Review(
    rating=2,
    comment="I think this movie was the best of 2021. When I left the cinema I was speechless. I laughed, cried and  "
            "was shocked by the reveals in this movie. The actors in this movie all are individual amazing (pun "
            "intended). This movie is a typical Marvel Blockbuster. The Russo brothers have outdone themselves again. "
            "The fact that this trilogy now has come to an end is sad, I feel like the story is not over yet.",
    date=datetime.datetime(2021, 12, 1),
    author="johnkennedy",
    movie_id=MOVIE_3.id
)

REVIEW_7 = Review(
    rating=5,
    comment="I think this movie was the best of 2021. When I left the cinema I was speechless. I laughed, cried and  "
            "was shocked by the reveals in this movie. The actors in this movie all are individual amazing (pun "
            "intended). This movie is a typical Marvel Blockbuster. The Russo brothers have outdone themselves again. "
            "The fact that this trilogy now has come to an end is sad, I feel like the story is not over yet.",
    date=datetime.datetime(2022, 4, 12),
    author="sannelily",
    movie_id=MOVIE_3.id
)

REVIEW_8 = Review(
    rating=5,
    comment="This movie is about the family Madrigal. Whitin this family there is magic. All the kids will get a "
            "special power when grow older. The music in this film is beautiful and Lin Manual Miranda is such a good "
            "director. The movie has incredible colors and cinematic images. Even if you are an adult you will enjoy "
            "this movie a lot. It is family-friendly and I promise you, your kids will blast along with all the "
            "songs. Remember; We don’t talk about Bruno!",
    date=datetime.datetime(2022, 4, 18),
    author="sannelily",
    movie_id=MOVIE_6.id
)

DB.session.add(REVIEW_1)
DB.session.add(REVIEW_2)
DB.session.add(REVIEW_3)
DB.session.add(REVIEW_4)
DB.session.add(REVIEW_5)
DB.session.add(REVIEW_6)
DB.session.add(REVIEW_7)
DB.session.add(REVIEW_8)
DB.session.commit()
