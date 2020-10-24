*Web Page Ranking Algrorithm*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

An Advanced Algorithm which crawls through href links from a particular website and gives each pages a rank depending upon the number of href links pointing back towards it using an algorithm and maps and stores it in a SQL database

Files:
crawl.py: This file asks for a start url and spiders through all the href links in the web page. In order to not deviate too much, i have restricted the program to go to links on the same base website and not another.(U will understand it better when i explain the page ranking algorithm). It saves all the links and their html data in a database "spider.sqlite"

rank.py: It goes through the spider database and gives ranks to each link depending on how many pages point to a single page. The more pages point to your page, the more value your page has

reset.py: It resets all the ranks to 1 so you could run th program again

Representation Of The data accumulated:
page_dump.py: You could run this file to get a basic output with all the ranks of links

json_rep.py: it creates a json output representation of the data.

force.html: After running json_rep.py, run this to open a html web page and represent the data with nodes and lines in a nice manner. Each nodes represent a link. Each line is a link pointing to another link.
