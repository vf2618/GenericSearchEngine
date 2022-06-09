


####################
####################
#    Install required packages: sqlite3, flask, bs4
####################
####################

# Then go to bottom of file and uncomment the function #crawler()



###################
# Flow from Process A-B
# requires (a) for the implementation of a database
###################
##################################################################################################################
# (a) SQL Database: Implement a searchable database that can store data from webpages
##################################################################################################################


def initiate_db(set_database):

    # 3 tables exist: "domains", "new_URLs", and "webpage_data"
    # domains:      domain_id , domain_URL, domain_accessed, crawl_delay, disallowed
    # new_URLs:     URL_id, domain_id, URL, URL_accessed
    # webpage_data: URL_id, domain_id, *** data ***

    # For each *** data *** a column is needed. 
    # For example: title, description, course, cuisnine, ... ea


    import sqlite3
    if set_database:
        database = set_database

    else:
        database = input("Connect to database in form of databasename.db: ")

    conn = sqlite3.connect(database)
    c = conn.cursor()

    #########################
    # Step 2: Accessing the database to check if it is new:
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = c.fetchall()

        ##### Existing database:
    # if the result is not empty, Tables already exist, 
    # let the user know what tables exist and how many entries they have
    if result !=[] and len(result) > 2:
        print("You successfully connected to the existing database: "+ str(database))
        print("The existing database has the following tables and number of entries:")
        for i in result:
            print(i[0] + ": " + str((c.execute('''SELECT COUNT(*) FROM {} '''.format(i[0])).fetchone()[0])))
        
        return database
    
    if result !=[] and len(result) == 2:
        print("You successfully connected to the existing database: "+ str(database))
        print("The existing database has the following tables and number of entries:")
        for i in result:
            print(i[0] + ": " + str((c.execute('''SELECT COUNT(*) FROM {} '''.format(i[0])).fetchone()[0])))
        
        print("The database existed but is missing TABLE webpage_data")
        database = add_table_webpage_data(database)
        return database

        ##### New database:
    if result == []:
        print("You successfully created and connected to the new database: "+ str(database))
        
        ##############################
        # TABLE domains
        c.execute('''CREATE TABLE domains(domain_id INT , domain_URL TEXT, domain_accessed INT, crawl_delay INT, disallowed TEXT, PRIMARY KEY (domain_id))''')
        ##############################
        # TABLE new_URLs
        c.execute('''CREATE TABLE new_URLs(URL_id INT, domain_id INT , URL TEXT, URL_accessed INT, PRIMARY KEY (URL_id))''')
        ##############################
        # TABLE webpage_data
        database = add_table_webpage_data(database)
        return database

def add_table_webpage_data(database):
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # add the table webpage data which depends on the data
    meta_columns =  access_metadata_from_URL("return_number_of_columns")
    custom_columns = access_customdata_from_URL("return_number_of_columns")
    columns_needed = meta_columns + custom_columns
    print("Please add one column for each data saved, specified in functions:")
    print("access_meta_data_from_URL() and access_customdata_from_URL()")
    print(f"You need to add a total of: ")
    print(f"{columns_needed} columns")

    #### USER INPUT
    #splits the list by common seperator, ", "
    columns_input = input("Add columns in the format: column_1, column2, column3: ").split(", ")
    
    #common error to add a comma and space at end
    if "" in columns_input:
        print("WRONG FORMAT, do not add ', ' at the end of the last column")
        print("It is recommended to delete the newly created database and try again")
        return False
    if columns_input[len(columns_input)-1][-1] == ",":
        print("WRONG FORMAT, do not add ',' at the end of the last column")
        print("It is recommended to delete the newly created database and try again")
        return False
    
    # Looping over the user input to receive a string like: "column1 TEXT, column2 TEXT"
    # implies that all columns are type TEXT
    additional_columns = ""
    for i in columns_input:
        additional_columns += i
        additional_columns += " TEXT, "
    #print("** info **   The SQL command to add the table webpage_data:")
    #print("             CREATE TABLE webpage_data(URL_id INT, domain_id INT, " + additional_columns +" PRIMARY KEY (link_id))")
    c.execute("CREATE TABLE webpage_data(URL_id INT, domain_id INT, " + additional_columns +" PRIMARY KEY (URL_id))")

    
    ##############################
    #check if the implemented tables exist:
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = c.fetchall()
    if result != []:
        print("The newly created database has the following tables and number of entries:")
        for i in result:
            print(i[0] + ": " + str((c.execute('''SELECT COUNT(*) FROM {} '''.format(i[0])).fetchone()[0])))

    return database

def set_new_ids(database):
    # receives the name of the database then retrieves the ids used as primary indexes for URLs and domain_URLs
    # (new_domain_id, new_URL_id)
    # (1,1) if tables are empty, ie database exists
    # (maxvalue(domain_id)+1, maxvalue(URL_id)+1): it finds the largest primary keys and adds 1

    #connect to database
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()

    #accesses the table "new_URLs" and orders the results by URL_id in descending order so that largest appears on top, then retrieves it
    new_URL_id = c.execute('''SELECT URL_id FROM new_URLs ORDER BY URL_id DESC LIMIT 1''').fetchone()
    new_domain_id = c.execute('''SELECT domain_id FROM domains ORDER BY domain_id DESC LIMIT 1''').fetchone()

    # if the fetched id is not equal to one, add one ready to be used to associate a new domain
    if new_domain_id != None:
        new_domain_id = new_domain_id[0] +1
    # otherwise, start at zero
    else:
        new_domain_id = 1

    # if the fetched id is not equal to one, add one ready to be used to associate a new URL
    if new_URL_id != None:
        new_URL_id = new_URL_id[0] +1
    # otherwise, start at zero
    else:
        new_URL_id = 1

    return new_domain_id, new_URL_id

def wrong():
    
    # # if it doesn't exist yet, create the table and add the links to the table
    # if ('virtual_data_table',) not in result:
    #     c.execute('CREATE VIRTUAL TABLE virtual_data_table USING fts5 (link,heading,description,document, category, cuisine, rating, rating_number, chef, prep, keywords, image_link, domain_id)')
    #     conn.commit()
    #     c.execute('''
    #                 INSERT INTO link_data_virtual_fts5
    #                 SELECT links_from_sitemap.link, link_data.heading, link_data.description, link_data.document, link_data.category, link_data.cuisine, link_data.rating, link_data.rating_number, link_data.chef, link_data.prep, link_data.keywords, link_data.image_link ,link_data.domain_id
    #                 FROM link_data 
    #                 INNER JOIN links_from_sitemap ON link_data.link_id = links_from_sitemap.link_id''')
    #     conn.commit()

    # #else don't add
    # else:
    #     c.execute('DROP TABLE link_data_virtual_fts5')
    #     conn.commit()
        
    #     c.execute('CREATE VIRTUAL TABLE link_data_virtual_fts5 USING fts5 (link,heading,description, document, category, cuisine, rating, rating_number, chef, prep, keywords, image_link, domain_id)')
    #     conn.commit()
    #     c.execute('''
    #                 INSERT INTO link_data_virtual_fts5
    #                 SELECT links_from_sitemap.link, link_data.heading, link_data.description, link_data.document, link_data.category, link_data.cuisine, link_data.rating, link_data.rating_number, link_data.chef, link_data.prep, link_data.keywords, link_data.image_link ,link_data.domain_id
    #                 FROM link_data 
    #                 INNER JOIN links_from_sitemap ON link_data.link_id = links_from_sitemap.link_id''')
    #     conn.commit()
        
    #     print("Virtual table already exists")
    return 1

def update_to_virtual_table(database):
    
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = c.fetchall()
    #print (table_names)

    if ('virtual_data_table',) in table_names:
        c.execute('DROP TABLE virtual_data_table')
        conn.commit()
        # obtain table data without the virtual data tables:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = c.fetchall()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = c.fetchall()

    webpage_data_table_name = table_names[2][0]
    #print(webpage_data_table_name)
    #essentially this would be enough:
    #webpage_data_table_name = "webpage_data"
    c.execute("SELECT * FROM pragma_table_info(?)", [webpage_data_table_name])


    # to insert data:
    column_names = "(URL, domain_URL, "
    data_string = "new_URLs.URL, domains.domain_URL"
    results = c.fetchall()
    for i in range(2, len(results)):
        data_string += ", webpage_data."
        data_string += results[i][1]
        column_names += results[i][1]
        column_names += ", "
    column_names += ")"

    c.execute("CREATE VIRTUAL TABLE virtual_data_table USING fts5 " + column_names)
    conn.commit()

    webpage_data_table_name = table_names[2][0]
    #print(webpage_data_table_name)
    c.execute("INSERT INTO virtual_data_table SELECT " + data_string + " FROM webpage_data INNER JOIN new_URLs ON webpage_data.URL_id = new_URLs.URL_id INNER JOIN domains on webpage_data.domain_id = domains.domain_id")
    conn.commit()
    
    ### return some text to show that the table is done!
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = c.fetchall()
    print("The database was converted to a virtual table: ")
    print("The existing database has the following tables and number of entries:")
    
    for i in range(0, 4):
        i = result[i]
        print(i[0] + ": " + str((c.execute('''SELECT COUNT(*) FROM {} '''.format(i[0])).fetchone()[0])))

##################################################################################################################
##################################################################################################################
##################################################################################################################
################################# Generic Crawler ################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
def access_any_URL(URL, crawl_delay=0, default_timeout=2):
    # Access any URL receives the URL and returns
    #   either the html
    #   or False and the HTTP status code
    #   or False and 999 (the latter indicating that timeout occured)
    from urllib.request import urlopen
    import urllib.error
    from time import sleep
    sleep(crawl_delay)
    try:
        html = urlopen(URL, timeout = default_timeout)
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception as e:
        return False, 999
    return True, html

def parse_html(html, parser = "lxml"):
    #libraries needed:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, parser)
    return soup

def obtain_newURLs_from_URL(soup, domain_id):
    storage={}

    # access all href attributes within the a tag
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if len(url) != 0:
            if url[0:8] == "https://":
                storage.update({url:1})
            
            elif url[0:7] == "http://":
                storage.update({url:1})

            # This can access up to 5x more links, within a webpage. May want to disable by:
            # leaving default domain_url = "" to prevent storage being accessed
            # here one could find the domain_URL from the database
            # to then add it to the front, in case the href found actually only
            #   contains a reference to the local, domain specific page!
            # requires!!!: => domain_URL = c.execute (SELECT domain_URL .....)
            # then:

            # elif url[0] == "/":
            #     import sqlite3
            #     conn = sqlite3.connect(database)
            #     c = conn.cursor()
            #     result = c.execute("SELECT domain_URL FROM domains WHERE domain_id=:domain_id",{"domain_id": domain_id})
            #     domain_url = result.fetchone()[0]
            #     if url[0:2] == "//":
            #         combined_url = "https:" + url
            #         storage.update({combined_url:1})
            #     else:
            #         combined_url = domain_url + url
            #         storage.update({combined_url:1})
            
        #could implement something for the links on eg:
        #https://www.planecheck.com

    new_URLs = list(storage.keys()) if storage else []
    return new_URLs

def access_metadata_from_URL(soup):
    
    number_of_data_columns = 2
    if soup == "return_number_of_columns":
        return number_of_data_columns

    #######
    # TITLE
    title = soup.find("title")
    if title:
        title = title.getText()
    else:
        try:
            title = soup.find_all("meta")
            title = title["content"] if title else None
        except Exception as e:
            title = None

    #######
    # DESCRIPTION
    description = soup.find("meta", property = "og:description")
    try:
        description = description["content"] if description else None
    except Exception as e:
        description = None
    
    #I do not get this to work, accessing <meta name="description">
    #description = soup.find_all(lambda tag:tag.name == 'meta' and 'description' in tag.get_text())
    meta_data = [title, description] ### CHANGE THE ON TOP!!!
    return meta_data

def access_customdata_from_URL(soup):
    number_of_data_columns = 1
    if soup == "return_number_of_columns":
        return number_of_data_columns
    
    #######
    # ALL TEXT FROM THE DOCUMENT
    # https://towardsdatascience.com/create-a-simple-search-engine-using-python-412587619ff5
    all_text = soup.get_text()
    import re
    document = re.sub(r'\s{2,}', ' ', all_text)
    
    custom_data = [document] 
    #custom_data = []
    return custom_data

##################################################################################################################
#Process A: Define how new URLs from the database should be selected
##################################################################################################################
def URL_input():
    input_new_URL = input("Please enter a new URL to be added to TABLE new_URLs: ")
    if input_new_URL[0:8] == "https://":
        return input_new_URL

    elif input_new_URL[0:7] == "http://":
        return input_new_URL

    else:
        print("WRONG FORMAT")
        print("Try adding a URL either with https:// or http:// at the beginning.")
        return URL_input()

def select_new_URL_to_access(database, requested_domain_id):
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    #initiate a variable
    new_selected_URL = None
    new_selected_URL_id = None
    #obtain the largest domain_id within the database 

    # c.execute('''SELECT domain_id FROM domains ORDER BY domain_id DESC LIMIT 1''')
    # data = c.fetchone()
    # if data != None:
    #     domain_id = requested_domain_id
    # if data == None:
    #     return 

    # as long as the the selected URL is empty, increment the domain id.
    c.execute('''SELECT URL, URL_id, domain_id FROM new_URLs WHERE domain_id=:domain_id AND URL_accessed=:URL_accessed ORDER BY URL_id ASC LIMIT 1''', {"domain_id":requested_domain_id, 'URL_accessed' : 0, })
    data = c.fetchone()

    # if no link is found with the requested domain_id, set it to 1, so the crawler can access pages from all other URLs with URL_accessed = 0, within domain_id =[all]
    if data == None:
        requested_domain_id =1

    while new_selected_URL == None and requested_domain_id <= (new_domain_id-1):
        c.execute('''SELECT URL, URL_id, domain_id FROM new_URLs WHERE domain_id=:domain_id AND URL_accessed=:URL_accessed ORDER BY URL_id ASC LIMIT 1''', {"domain_id":requested_domain_id, 'URL_accessed' : 0, })
        data = c.fetchone()
        requested_domain_id +=1

        if data != None:
            new_selected_URL = data[0]
            new_selected_URL_id = data[1]
            new_selected_domain_id = data[2]
            return new_selected_domain_id, new_selected_URL, new_selected_URL_id
    
    #otherwise:
    # NO MORE URLs with accessed  = 0
    # either empty database or all accessed:
    # The database has entries, but no URL was found that was not previously accessed !!!
    #   no URL in TABLE new_URLs has URL_accessed==0.
    #   All URLs were accessed and there were no new URLs found within them.
    # input is required from the user!
    print("All the new_URLs in the database were previously accessed")
    print("This appears to be a new database or all URLs were previously accessed")
    print("We need some input from you, best would be one seed URL") 
    new_input_URL = URL_input()
    new_selected_URL = new_input_URL
    new_selected_URL_id, new_selected_domain_id = add_new_URL(new_input_URL)
    return new_selected_domain_id, new_selected_URL, new_selected_URL_id

def crawler(set_database, limit, requested_domain_id=1, set_default_crawl_delay=0.1, sitemap_limit=0):
    from IPython.display import clear_output
    import time
    global database
    global new_domain_id
    global new_URL_id
    global default_crawl_delay

    #---------------------------------------------------------------------------
    # USING INPUT PARAMETERS:
    #---------------------------------------------------------------------------
    #
    # initialising the database
    database = initiate_db(set_database)
    # limit
    # requested_domain_id
    default_crawl_delay = set_default_crawl_delay
    # sitemap_limit

    #---------------------------------------------------------------------------
    # Collecting Statistics, Part 1
    #---------------------------------------------------------------------------
    # this sets the max ids
    #   and also allows to collect
    #   some basic data for final 
    #   statistics to be returned
    #
    tic = time.perf_counter()
    new_domain_id, new_URL_id = set_new_ids(database)
    previous_domain_id = new_domain_id
    previous_URL_id = new_URL_id
    previous_limit = limit

    #---------------------------------------------------------------------------
    # MAIN STEP OF THE FUNCTION: THE CRAWLING UNTIL LIMIT REACHED
    #---------------------------------------------------------------------------
    # this while loop will run until the specified limit is reached
    #
    count = 0
    while count < limit:
        data = select_new_URL_to_access(database, requested_domain_id)
        domain_id = data[0]
        selected_new_URL = data[1]
        selected_new_URL_id = data[2]
        #print(f"New URL accessed: {selected_new_URL}")
        data = access_domain(domain_id, sitemap_limit)
        if data == False:
            print("something has actually gone wrong")
        domain_URL = data[0]
        crawl_delay = data[1]
        disallowed = data[2]
        #print("obtained data:")
        #print(domain_URL, crawl_delay, domain_id)
        #print("data passed on:")
        #print(selected_new_URL, selected_new_URL_id, domain_id, crawl_delay)
        data_stored = access_new_URL(selected_new_URL, selected_new_URL_id, domain_id, crawl_delay, disallowed)
        
        #this only indicates 1 or 0 depending on whether it was possible to access data or not
        if data_stored == 1:
            count +=1
            #print(count)
        elif data_stored ==2:
            return False
    
    #---------------------------------------------------------------------------
    # Collecting Statistics Part 2
    #---------------------------------------------------------------------------
    # set the final max ids
    #   to get info about the current 
    #   state of the database.
    #
    toc = time.perf_counter()
    new_domain_id, new_URL_id = set_new_ids(database)
    final_domain_id = new_domain_id
    final_URL_id = new_URL_id
    new_domains_added = final_domain_id - previous_domain_id
    new_URLs_added = final_URL_id - previous_URL_id
    
    # Some rows need to be counted within the database:
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    c.execute('''SELECT COUNT() FROM new_URLs WHERE URL_accessed!=0 ''')
    # total attemted of URLs accessed
    attempted = c.fetchone()[0]

    # timeout occured:
    c.execute('''SELECT COUNT() FROM new_URLs WHERE URL_accessed=999 ''')
    timedout = c.fetchone()[0]

    # number stored in table
    c.execute('''SELECT COUNT() FROM webpage_data''')
    webpages_totally_stored = c.fetchone()[0]

    clear_output(wait=True)
    print()
    print(f"The crawler saved data from {previous_limit} webpages URLs")
    print("During this crawl the following happened:")
    print(f"New URLs added: {new_URLs_added}")
    print(f"New domains added: {new_domains_added}")
    print("")
    print("General info about the database now:")
    print(f"The total number of all webpages stored {webpages_totally_stored}")
    print(f"This took a total of {attempted} attempts")
    print(f"With a total of {timedout} URLs not accessed due to timeout")
    print(f"This took {round(toc-tic,3)} seconds.")


##################################################################################################################
#Process B: Access and retrieve robots.txt data:
##################################################################################################################
def access_robots(domain_URL):
    # this function needs to be adapted
    # Usually the robots.txt specifies who the rules apply to.
    # The "who" is called the user-agent and could be a webbrowser, or a webcrawler
    # good example of robots.txt is https://www.apple.com/robots.txt
    # This code cannot yet determine if the rules (especially crawl_delay or disallowed)
    #       are applicable to this crawler, or not. 
    # This can and SHOULD! be implemented at a later stage.

    #get the robots.txt file located at the root of the domain 
    robots_URL = domain_URL +"/robots.txt"
    html = access_any_URL(robots_URL, 0)
    if html[0] == False:
        return False, html[1]
    soup = parse_html(html[1])
    data = soup.prettify()

    #expect to fetch the following data and store it in a dictionary.
    result_data_set = {"Disallowed":[], "Allowed":[], "Crawl_Delay":[],"Sitemap":[],}
    
    #read in each line and add the content to the dictionary
    for line in data.split("\n"):
        if line.startswith('Allow: '):    # this is for allowed url
            result_data_set["Allowed"].append(line.split(': ')[1].split(' ')[0])    # to neglect the comments or other junk info
        elif line.startswith('Disallow: '):    # this is for disallowed url
            result_data_set["Disallowed"].append(line.split(': ')[1].split(' ')[0])    # to neglect the comments or other junk info
        elif line.startswith("Sitemap"):
            result_data_set["Sitemap"].append(line.split(': ')[1].split(' ')[0])
        elif line.startswith("Crawl"):
            result_data_set["Crawl_Delay"].append(line.split(': ')[1].split(' ')[0].strip("\n"))
    
    # Sometimes zero, one or multiple crawl_delays are defined:
    # I only want one crawl_delay value!
    crawl_delays = result_data_set["Crawl_Delay"]
    if len(crawl_delays) == 0:
        crawl_delays = 0
    elif len(crawl_delays) == 1:
        crawl_delays = float(crawl_delays[0])
    elif len(crawl_delays) > 1:
        #if multiple are found, select the smallest :)
        crawl_delays = float(min(crawl_delays))
    
    result_data_set["Crawl_Delay"] = crawl_delays
    
    return True, result_data_set

def access_a_sitemap_URL(sitemap_URL, crawl_delay):
    html = access_any_URL(sitemap_URL, crawl_delay)
    if html[0] == False:
        return []
    soup = parse_html(html[1])
    URLs_on_sitemap = soup.find_all("loc")
    
    new_sitemap_URLs = []
    inter = []
    for i in URLs_on_sitemap:
        inter =(i.text).split("\n")
        inter = [value for value in inter if value != ""]
        for j in inter:
            j = j.split()
            new_sitemap_URLs += j
    return new_sitemap_URLs

def sitemap(sitemap_data, domain_id, crawl_delay, sitemap_limit):
    # The sitemap of a webpage contains all URLs to the differnet "sites" or webpages.

    # The robots.txt found the text after "Sitemap:"
    # This is usually a URL that leads to the actual sitemap.
    # Can look like: "https://www.bbc.co.uk/sitemap.xml"
    
    # Some websites list multiple sitemaps within the robots.txt file
    # Other websites have sitemaps that are cascaded:
    #   The list of URLs of the provided sitemap is connected to more sitemaps.

    # To implement this infinite loop: 
    # Initially sitemap_data is a list containing the entries from robots.txt
    # Each entry is looped over and tried to be accessed.
    # Once accessed 

    counter = 0
    while counter <= sitemap_limit:
        for one_sitemap_URL in sitemap_data:
            new_sitemap_URLs =access_a_sitemap_URL(one_sitemap_URL, crawl_delay)
            for line in new_sitemap_URLs:
                if line[-4:] == ".xml":
                    # if yes, then it will add the link to the sitemaplinks which is currently iterated over.
                    sitemap_data+=[line]
                else:
                    add_new_URL(line, domain_id, True) # PREVIOUSLY PASSED ON CRAWL DELAY, NOT NECESSARY
                    # the iteration of the global URL_id is performed by the above function.
                    if sitemap_limit != 0:
                        counter += 1
                        if counter == sitemap_limit:
                            return False
        
        # just in case...
        counter +=1
    return False
    
def access_domain(domain_id, sitemap_limit):

    #connect to database:
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    # get all the data from the domain stored in TABLE domains:
    c.execute(  '''SELECT domain_id, domain_URL, domain_accessed, crawl_delay, disallowed 
                FROM domains WHERE domain_id=:domain_id ''', {"domain_id": domain_id})
    resulting_domain_data = c.fetchone()
    
    if resulting_domain_data == None:
        #URL was probably manually added and so no row exists yet.

        return False

    elif resulting_domain_data[2] == 1:
    # domain was previously accessed, the data can be returned
        domain_URL = resulting_domain_data[1]
        domain_accessed = resulting_domain_data[2]
        crawl_delay = resulting_domain_data[3]
        disallowed = resulting_domain_data[4]
        return domain_URL, crawl_delay, disallowed
    
    elif resulting_domain_data[2] == 0:
    # domain was not accessed yet, the default value 0 is still there.
    # access the domain

        domain_URL = resulting_domain_data[1]

        # try to access the "/robots.txt" file
        robots_data = access_robots(domain_URL)

        # if the URL "[domain]/robots.txt" had some error when requesting the page
        #   (function access_any_URL())it will return a list: [False, "error code"]
        if robots_data[0] == False:
            # update the domain data:
            crawl_delay = default_crawl_delay
            domain_accessed = robots_data[1]
            disallowed = ""
            c.execute('''UPDATE domains SET crawl_delay=:crawl_delay, domain_accessed=:domain_accessed
                        WHERE domain_id=:domain_id''', {"crawl_delay":crawl_delay, "domain_accessed":domain_accessed, "domain_id":domain_id})
            conn.commit()
            
            return domain_URL, crawl_delay, disallowed

        # if robots data exists then:
        #   update the domain data in Table domains.
        #   use the sitemap to retreive even more URLs
        #   return the domain data back

        if robots_data[0] == True:
            robots_data = robots_data[1]
            crawl_delay = robots_data["Crawl_Delay"]
            domain_accessed = 1
            disallowed = robots_data["Disallowed"]
            disallowed =  ", ".join(disallowed)
            #print(disallowed)
            c.execute('''UPDATE domains SET crawl_delay=:crawl_delay, domain_accessed=:domain_accessed, disallowed=:disallowed
                        WHERE domain_id=:domain_id''', 
                        {"crawl_delay":crawl_delay, "domain_accessed":domain_accessed, "disallowed":disallowed, "domain_id":domain_id})
            conn.commit()

            sitemap_data = robots_data["Sitemap"]
            # since sitemaps could be huge, flooding the table "new URLs" as well as potentially taking time
            # they can be limited through, by default the limit is turned off.
            # when the sitemap_limit = 1 then it should not be accessed. 
            #print(f"sitemap limit = {sitemap_limit}")

            if sitemap_data == []:
                print("No Sitemaps found!")
                return domain_URL, crawl_delay, disallowed
            
            elif sitemap_limit != 1:
                print("Sitemaps are accessed...")
                # the counting does not really work...
                #previous_max_URL_id = set_new_ids(database)[1]
                #print(previous_max_URL_id)
                dummy = True
                while dummy:
                    dummy = sitemap(sitemap_data, domain_id, crawl_delay, sitemap_limit)
                current_max_URL_id = set_new_ids(database)[1]
                #print(previous_max_URL_id)
                #print(current_max_URL_id)
                #diff = current_max_URL_id - previous_max_URL_id
                #print(f"{diff} URLs were added from the sitemap")
            return domain_URL, crawl_delay, disallowed
    
    # if a value other than 0 or 1 is associated to the domain
    # it has an error code associated to it
    # therefore entries exist on domain data. Return! 
    else:
    # domain was previously accessed, the data can be returned
        #domain_URL = resulting_domain_data[0]
        #domain_accessed = resulting_domain_data[0]
        crawl_delay = resulting_domain_data[3]
        disallowed = resulting_domain_data[4]

        #nb: these are the default values, since not possible to access robots.txt
        return domain_URL, crawl_delay, disallowed

##################################################################################################################     
#Process C: Finally accessing and retreiving data from a URL:
##################################################################################################################
def is_allowed(URL, disallowed):
    #compares if the URL is part of the disallowed data listed on robots.txt
    #for element in disallowed:
    #    if element in URL:
    #        return 0
    return 1

def access_new_URL(URL, URL_id, domain_id, crawl_delay, disallowed):
    # first step is to check if its allowed to access the URL via the disallowed() function
    #   if not possible update variable URL_accessed within table new_URLs (to -1)
    # second step involves actually obtaining the html data from the website
    #   if this is not possible  update variable URL_accessed within table new_URLs 
    #     to the received error code
    # Finally scrape the data:
    #   save new URLs found to the table new_URLs and data to the table webpage_data
    #global database
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()

    allowed = is_allowed(URL, disallowed)
    
    if not allowed:
        URL_accessed = -1
        c.execute('''UPDATE new_URLs SET URL_accessed=:URL_accessed
                        WHERE URL_id=:URL_id''', 
                        {"URL_accessed":URL_accessed, "URL_id":URL_id})
        conn.commit()
        return 0
    
    # now the fun part!
    html = access_any_URL(URL, crawl_delay)
    if html[0] == False:
        URL_accessed = html[1]
        c.execute('''UPDATE new_URLs SET URL_accessed=:URL_accessed
                        WHERE URL_id=:URL_id''', 
                        {"URL_accessed":URL_accessed, "URL_id":URL_id})
        conn.commit()
        return 0
    else:
        URL_accessed = 1
        c.execute('''UPDATE new_URLs SET URL_accessed=:URL_accessed
                        WHERE URL_id=:URL_id''', 
                        {"URL_accessed":URL_accessed, "URL_id":URL_id})
        conn.commit()

    soup = parse_html(html[1])
    list_of_new_URLs = obtain_newURLs_from_URL(soup, domain_id) #set domain_id to "" to increase speed
    for new_URL in list_of_new_URLs:
        add_new_URL(new_URL) # crawl_delay = crawl_delay)# PREVIOUSLY PASSED ON DEFAULT CRAWL DELAY
    
    ####
    #save remaining data to the database!!
    standard_columns = [URL_id, domain_id]
    metadata_columns = access_metadata_from_URL(soup)
    customdata_columns = access_customdata_from_URL(soup)

    all_columns = standard_columns + metadata_columns + customdata_columns
    
    question_marks = "(?"
    for i in range(0,len(all_columns)-1):
        question_marks +=",?"
    question_marks += ")"
    #print(question_marks)
    #print(all_columns)
    try:
    #print(question_marks)
    #print(all_columns)
        c.execute("INSERT INTO webpage_data VALUES " + question_marks, all_columns)
        conn.commit()
    except Exception as e:
        print("Something went wrong")
        print("Saving Webpage data to database failed")
        print("Common errors:")
        print("-) collumns and data wrongly specified")
        print("-) some internal error about primary keys")
        print(f"The following collumns were tried to be added {all_columns}")
        print(f"The following was the resulting match phrase:")
        print(f"{question_marks}")
        return 2
    return 1

##################################################################################################################
#Process D: Take a URL and add it to the table new_URLs WITHOUT accessing the associated webpage:
##################################################################################################################
def get_domain_URL(URL):
    # get_domain returns the domain_URL of any URL, 
    #   eg  link = "https://www.apple.com/store/1234" returns "https://www.apple.com"
    #   currently it only recognises a link with either "https://", "http://" or "www."
    
    # split the link at each forward slash
    split_URL = URL.split("/")

    # check if its a useable link which includes https, http, or www:
    if URL[0:8] == "https://":
        #create the domain_URL:
        domain_URL =  split_URL[0]+ "//" + split_URL[2] # + "/"
    
    elif URL[0:7] == "http://":
        #create the domain_URL:
        domain_URL =  split_URL[0]+ "//" + split_URL[2] # + "/"

    # could be left out:
    elif URL[0:4] == "www.":
        #assume that all links with www. can be accessed through the http protocol
        domain_URL =  split_URL[0] #+ "/"
        
    # if not, then might be something wrong, stop here:
    else: return False

    return domain_URL

def add_new_URL(URL, domain_id=0, dont_check = False):
    # Import global variables
    global new_URL_id
    #global database

    # connect tot the database:
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # 
    # by default: check if the URL is already in the TABLE new_URLs:
    if dont_check == False:
        c.execute('''SELECT URL_id, domain_id FROM new_URLs WHERE URL=:URL ''', {"URL": URL})
        resulting_domain_data = c.fetchone()
        if resulting_domain_data != None:
            # URL IS ALREADY IN TABLE AND SO WILL NOT BE ADDED AGAIN!
            URL_id, domain_id = resulting_domain_data[0], resulting_domain_data[1]
            return URL_id, domain_id
    
    #FYI: when URLs are added from sitemap, dont_check = 1
    # this can be done since it is assumed that the sitemap only contains unique URLs.
    # some function could also be added to not check any URLs against the table
    # only before it is actually accessed, it is checked against the new_URLs table
    #   if duplicates exist, delete them!

    #####
    #Otherwise, the URL needs to be added to table new_URLs
    #Before that the corresponding domain_id needs to be found
    # The exception exists when the current function is called from the sitemaps() function
    # Then, the domain_id is already known!
    if domain_id == 0:
        # if it is zero, from the function default value,
        # the domain_id needs to be found
        domain_id = add_domain_stuff(URL)

    # otherwise the domain id is known!

    #####
    # now add the new URL to the table!
    URL_accessed = 0
    URL_id = new_URL_id
    c.execute('''INSERT INTO new_URLs VALUES (?,?,?,?)''', (URL_id, domain_id, URL, URL_accessed))
    conn.commit()
    new_URL_id +=1
    return URL_id, domain_id

def add_domain_stuff(URL):
    # the domain_stuff(URL) function receives a URL 
    # The function aims to return the domain_id associated to the URL
    # It initially creates the domain_URL by scraping the URL
    # It then checks if this domain_URL is present in TABLE domains
    # If it is not present then the domain_URL gets associated a domain_id and is added to the table
    # 
    # The function returns the domain_id

    # the global variables are imported:
    #global database
    global new_domain_id
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()


    #determine the domain_URL
    domain_URL = get_domain_URL(URL)
    # if it returns False then still add a row, but with the indicating error
    if domain_URL == False:
        #print("function get_domain returned False")
        domain_accessed = 0
        crawl_delay = default_crawl_delay
        disallowed = ""
        domain_id = new_domain_id # NEEDS TO BE ITERATED GLOBALLY
        c.execute('''INSERT INTO domains VALUES (?,?,?,?,?)''', (domain_id, domain_URL, domain_accessed, crawl_delay, disallowed))
        conn.commit()
        #print(f"new domain_inserted with crawl_delay: {crawl_delay}")
        #ITERATE!!
        new_domain_id+=1
        return domain_id
    

    #now check if it exists in the database:
    c.execute('''SELECT domain_id FROM domains WHERE domain_URL=:domain_URL ''', {"domain_URL": domain_URL})
    resulting_domain_id = c.fetchone()

    # if the domain_URL is not present in the table, it returns None
    if resulting_domain_id == None:
        #add the domain with default values
        domain_accessed = 0
        crawl_delay = default_crawl_delay
        disallowed = ""
        domain_id = new_domain_id # NEEDS TO BE ITERATED GLOBALLY
        c.execute('''INSERT INTO domains VALUES (?,?,?,?,?)''', (domain_id, domain_URL, domain_accessed, crawl_delay, disallowed))
        conn.commit()
        #print(f"new domain_inserted with crawl_delay: {crawl_delay}")
        #the domain was added to the table
        #the domain_URL is now associated with its unique domainURL!

        #for the next one, the global counter gets iterated by one
        new_domain_id += 1
        return domain_id
        

    # this domain is already present in the domain TABLE, find the domain_id
    else: 
        domain_id = resulting_domain_id[0]
        return domain_id


    
    

####################
####################
## To initialsie the Generic Crawler: run #crawler()
####################
####################

limit = 100
domain_id = 1
default_crawl_delay = 0.3
sitemap_limit = 1
database = "database_sample_100.db"  
#crawler(database, limit, domain_id , default_crawl_delay, sitemap_limit)


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

