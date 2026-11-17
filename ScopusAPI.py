import csv
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus import init

init()

# Path for the collected Papers
path = input("Path to the folder where the new file should be saved: ").strip().strip('"')

# Define filters
#sm = 'TITLE-ABS ( "social media" ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'
#restSM = 'TITLE-ABS ( "online social network*" OR "social network* site*" OR "social network* service*" OR "social network* platform*" OR "social platform*" OR "online community" OR "online communities" ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'
facebook = 'TITLE-ABS ( Facebook ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'
insta = 'TITLE-ABS ( Instagram ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'
reddit = 'TITLE-ABS ( Reddit OR Subreddit ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'
telegram = 'TITLE-ABS ( Telegram ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'
wechat = 'TITLE-ABS ( Wechat OR Weixin ) AND PUBYEAR > 2017 AND PUBYEAR < 2026 AND NOT TITLE-ABS ( "literature review*" OR "systematic review*" )'

#all= [SM, RestSM, DataCollectTitle, DataCollectionAbs, facebook, insta, reddit, telegram, wechat]
platformFilter = [facebook, insta, reddit, telegram, wechat]
#fileName = ["SM", "restSM", "Facebook", "Insta", "Reddit", "Telegram", "Wechat"]
fileName = ["Facebook", "Insta", "Reddit", "Telegram", "Wechat"]
i = -1  # Use to create each platform a seperate file 

for filter in platformFilter:
    search = ScopusSearch(filter, refresh=True, verbose=True, download=True, subscriber=True)
    i += 1
    if search.results:
        # Create a csv file with the papers
        with open(f"{path}/{fileName[i]}.csv", 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            
            # Columns of the file
            writer.writerow(['id', 'title', 'summary', 'date'])
            
            # Write only specific information of the paper
            for paper in search.results:
                writer.writerow([paper.doi, paper.title, paper.description, paper.coverDate])
    else:
        print("No papers found")
