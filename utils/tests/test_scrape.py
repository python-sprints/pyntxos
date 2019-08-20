import utils.scrape


def test_scrape():
    data = utils.scrape.scrape(dummy_flag=True)
    assert data == utils.scrape.dummy
    data = utils.scrape.scrape()
    print('blah')
