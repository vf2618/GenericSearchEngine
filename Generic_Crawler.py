from Functions_of_Generic_Crawler import crawler
    
    

####################
####################
## RUN !
####################
####################

limit = 10
domain_id = 1
default_crawl_delay = 0.3
sitemap_limit = 1
database = "database_sample_10.db"  
crawler(database, limit, domain_id , default_crawl_delay, sitemap_limit)


# when prompted enter these three columns
# title, description, document
# then enter a starting URL starting with https://

# you can adapt what data to be scraped in function #access_cusomdata_from_URL
# to find more URLs, uncomment the bottom parts in function #obtain_newURLs_fromURL

####################
####################
#    AFTER CRAWLER() finished, convert to virtual table 
####################
####################


#update_to_virtual_table(database)

