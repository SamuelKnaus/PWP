"""
    The mason builder class
"""

from mason.user_mason_builder import UserMasonBuilder
from mason.movie_mason_builder import MovieMasonBuilder
from mason.category_mason_builder import CategoryMasonBuilder
from mason.review_mason_builder import ReviewMasonBuilder


class MasonBuilder(
    UserMasonBuilder,
    ReviewMasonBuilder,
    MovieMasonBuilder,
    CategoryMasonBuilder
):
    """
        A single mason builder class which combines all the single mason builders
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        UserMasonBuilder.__init__(self)
        MovieMasonBuilder.__init__(self)
        CategoryMasonBuilder.__init__(self)
        ReviewMasonBuilder.__init__(self)
