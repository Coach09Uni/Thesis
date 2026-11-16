"""
This code creates datasets via the API of arXiv.
It sends multiple requests and creates multiple datasets during one execution
"""

import ssl
import urllib.request as libreq
import urllib.parse as parsing
import time

context = ssl._create_unverified_context()

def paging(search, partUrl):
    # Number of papers for each request is limited. Therefore, a new file contains only 100 papers  
    start = 0
    page_size = 100
    staticUrl = partUrl 
    # Collect all papers
    while True:
        time.sleep(4)
        # The url to which the request is sent
        url = f'ANDNOT+%28ti:%22literature+review%22+OR+ti:%22systematic+review%22+OR+abs:%22literature+review%22+OR+abs:%22systematic+review%22%29&start={start}&max_results={page_size}'

        fileName = "results/arxiv_" + search + "_" + str(start) + ".xml"
        fullURL= staticUrl + url
        # Request
        with libreq.urlopen(fullURL, context=context) as papers:
            response = papers.read().decode("utf-8")
        # Copy the response to the specific file
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(response)

        # Check if the request contains papers
        if "<entry>" not in response:
            break

        start += page_size
        print(start)

# The words to filter the papers/modifying the request
# 'ti' stands for title, and 'abs' for abstract
filterTiSM = ['ti:"social media" ', 'ti:"online social network*" ', 'ti:"social network* site*" ',
          'ti:"social network* service*" ', 'ti:"social platform*" ', 'ti:"social network* platform*" ',
          'ti:"online community" ', 'ti:"online communities" ']
filterAbsSM = ['abs:"social media" ', 'abs:"online social network*" ', 'abs:"social network* site*" ',
          'abs:"social network* service*" ', 'abs:"social platform*" ', 'abs:"social network* platform*" ',
          'abs:"online community" ', 'abs:"online communities" ']
searchSM = ["SM", "OSN", "SNS", "SNService", "SP", "SNP", "OC", "OCs"]

filterTiPlatform = ['ti:"facebook" ', 'ti:"instagram" ', 'ti:"reddit" ',
                    'ti:"subreddit" ', 'ti:"telegram" ', 'ti:"wechat" ', 'ti:"weixin" ']
filterAbsPlatform = ['abs:"facebook" ', 'abs:"instagram" ', 'abs:"reddit" ',
                    'abs:"subreddit" ', 'abs:"telegram" ', 'abs:"wechat" ', 'abs:"weixin" ']
searchPlatform = ["Facebook", "Insta", "Reddit", "Subreddit", "Tele", "We", "Weixin"]

filterTiDataFormat = '(ti:"data" OR ti:"information" OR ti:"content" OR ti:"dataset*") '
filterAbsDataFormat = '(abs:"data" OR abs:"information" OR abs:"content" OR abs:"dataset*") '
filterTiData = ['ti:"collect*" ', 'ti:"mine*" ', 'ti:"scrap*" ', 'ti:"crawl*" ', 'ti:"extract*" ', 'ti:"api" ', 'ti:"apis" ']
filterAbsData = ['abs:"collect*" ', 'abs:"mine*" ', 'abs:"scrap*" ', 'abs:"crawl*" ', 'abs:"extract*" ', 'abs:"api" ', 'abs:"apis" ']
searchTiData = ["CollectTitle", "MineTitle", "ScrapTitle", "CrawlTitle", "ExtractTitle", "APITitle", "APIsTitle"]
searchAbsData = ["CollectAbstract", "MineAbstract", "ScrapAbstract", "CrawlAbstract", "ExtractAbstract", "APIAbstract", "APIsAbstract"]


url = "https://export.arxiv.org/api/query?search_query="

# Search for all papers that contain a word from 'filterTiSM' or 'filterAbsSM'
i = 0
for x in filterTiSM:
    query = parsing.quote_plus(x + "OR " + filterAbsSM[i])
    paging(searchSM[i], url + query)
    i += 1

# Search for all papers that contain a platform
i = 0
for x in filterTiPlatform:
    query = parsing.quote_plus(x + "OR " + filterAbsPlatform[i])
    paging(searchPlatform[i], url + query)
    i += 1