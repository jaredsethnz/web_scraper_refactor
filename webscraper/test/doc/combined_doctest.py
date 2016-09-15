"""
>>> from webscraper.cli.command import Command
>>> cmd_test_2 = Command()

# ----------Test command or data input errors...----------

>>> cmd_test_2.onecmd('request f')
fetching html from .....
data fetch error.....

>>> cmd_test_2.onecmd('request rf')
no recursive urls set.....

>>> cmd_test_2.onecmd('request u--mightyape.co.nz')
please enter a valid url.....

>>> cmd_test_2.onecmd('request up--mightyape.co.nz')
please enter a valid url.....

>>> cmd_test_2.onecmd('request ur--mightyape.co.nz')
please enter a valid url.....

>>> cmd_test_2.onecmd('data g--div:class:product')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data gr--div:class:productDetails')

>>> cmd_test_2.onecmd('data cd--kw:0:0|child:0:0')

>>> cmd_test_2.onecmd('data wo')
displaying web data objects.....
----------------------------------------------------------------

>>> cmd_test_2.onecmd('graph d--format')
gathering data.....

>>> cmd_test_2.onecmd('request')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('request p--blah')

>>> cmd_test_2.onecmd('request u')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('request up')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('request f--')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('request rf--test')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('request u')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('data')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('data p--hmmmmm')

>>> cmd_test_2.onecmd('data l--')
loading saved data.....
File  not found.....

>>> cmd_test_2.onecmd('data s')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('data g--nothing')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data gr--norecursive')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data cf--extra')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('data fu--a:blah')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data dk--a:blah|div:class:test')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data rdk--a:blah:place|div:test')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data cd--hmm:place|div:test')
command error, run help command for command details.....

>>> cmd_test_2.onecmd('data ds--files')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('graph')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('graph d')
*** Unknown syntax: command error, run help command for command details.....

>>> cmd_test_2.onecmd('graph g')
*** Unknown syntax: command error, run help command for command details.....

>>> from webscraper.cli.command import Command
>>> cmd_test_1 = Command()

# ----------Test Happy Day Scenario----------

>>> cmd_test_1.onecmd('request u--https://www.mightyape.co.nz'\
'/games/best-sellers')
setting url.....

>>> cmd_test_1.onecmd('request f')
fetching html from https://www.mightyape.co.nz/games/best-sellers.....

>>> cmd_test_1.onecmd('request up--http://www.mightyape.co.nz')
setting url padding.....

>>> cmd_test_1.onecmd('data g--div:class:product')  # doctest: +ELLIPSIS
filtering data.....

>>> cmd_test_1.onecmd('data fu--a:class:title')  # doctest: +ELLIPSIS
filtering urls.....
adding url.....

>>> cmd_test_1.onecmd('request rf')  # doctest: +ELLIPSIS
fetching recursive html.....

>>> cmd_test_1.onecmd('data gr--div:class:product'\
'Details')  # doctest: +ELLIPSIS
filtering recursive data.....

>>> cmd_test_1.onecmd('data dk--a:class:title|span:class:price|'\
'div:class:format')  # doctest: +ELLIPSIS
adding tag, class pair: ['a', 'class', 'title']
adding tag, class pair: ['span', 'class', 'price']
adding tag, class pair: ['div', 'class', 'format']

>>> cmd_test_1.onecmd('data cd--kw:0:0|child:0:0')  # doctest: +ELLIPSIS
creating object.....

>>> cmd_test_1.onecmd('data s--best_selling_gaming.pickle')
saving data to disk.....

>>> cmd_test_1.onecmd('data ds')
displaying file save locations.....
-----------------------------------------------------------------
<BLANKLINE>
/Users/Seth/GitHub/web_scraper_refactor/best_selling_gaming.pickle
<BLANKLINE>
-----------------------------------------------------------------
<BLANKLINE>

>>> cmd_test_1.onecmd('data cf')
clearing filtered data.....

>>> cmd_test_1.onecmd('data wo')
displaying web data objects.....
----------------------------------------------------------------

>>> cmd_test_1.onecmd('data l--best_selling_gaming.pickle')
loading saved data.....

>>> cmd_test_1.onecmd('graph d--format')
gathering data.....

>>> cmd_test_1.onecmd('graph g--format')
displaying graph.....

>>> cmd_test_1.onecmd('data rs--best_selling_gaming.pickle')
removing file best_selling_gaming.pickle.....
"""


def test_combined():
    import doctest
    import sys
    sys.path.insert(0, sys.path[0] + '/../../..')
    return doctest.testmod(verbose=True)


if __name__ == "__main__":
    test_combined()
