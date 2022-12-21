
from webgoose.base_page_querier import BasePageQuerier


def test_add_default_metadata():

    # Initialise BasePageQuerier
    querier = BasePageQuerier()

    metadata = {'title': 'Title', 'description': ''}
    defaults = {'template': 'base.html', 'description': 'this is a description'}

    assert querier.add_default_metadata(metadata, defaults) == {'title': 'Title', 'description': '', 'template': 'base.html'}




