BUGZAP
======


Bugzilla Analysis Program is an analysis tool that uses some basic Natural Language Processing to extract descriptive information from bug reports.


Requirements
------------

Bugzap uses [Distiller](http://github.com/franciscocanas/Distiller):
Automated Keyword Extraction from Document Collections



Usage
-----

###Scraping Bugzilla

To start scraping bug reports for a Bugzilla instance, run:

    $ scrapy crawl query.bugzilla -a query=queryfile -o outfile -t json

The query file needs the domain of the Bugzilla instance in its first line, plus at least one search query URL to start the scrape from:

    mybugzillainstance.com
    https://issues.mybugzillainstance.com/buglist.cgi?email1=myemail%40email.com&emailassigned_to1=1&emailcc1=1&emailreporter1=1&emailtype1=exact&list_id=2581552

Scrapy will store all retrieved bug reports to outfile in json format.


###Processing Documents

To process the retrieved bug reports, run:

    $ python bugzap/main.py -j outfile -r bugzilla -b mylacklist -n mybugs

All reports will be saved to the bugzap/visualization/data/mybugs folder.

For further info, see:
    $ python buzap/main.py -h


###Viewing Statistics

The reports can be viewed from Mozilla by opening bugzap/visualization/freqDist.html file and entering the name
 of your data set:

    $ firefox bugzap/visualization/freqDist.html

