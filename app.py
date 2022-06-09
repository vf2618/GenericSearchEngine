###################
# to run app  through local host enter into concole:
# flask run --host= [146.169.218.212]
# ######################
# ip address is local from computer and varies 
# then accessible through, for example 146.169.218.212:5000


from flask import Flask, render_template, request
# app is a flask object
# we pass in name to determine the route path
app = Flask(__name__)

database = "bbc_food_sample.db"



@app.route('/', methods = ['POST','GET'])
def results():
    import time
    if request.method == 'GET':
        import sqlite3
        conn = sqlite3.connect(database)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        result = c.execute('''SELECT DISTINCT category FROM webpage_data ORDER BY category ASC''')
        all_categories = result.fetchall()

        result = c.execute('''SELECT DISTINCT cuisine FROM webpage_data ORDER BY cuisine ASC''')
        all_cuisines = result.fetchall()
        return render_template("data_get_report.html", selection= (all_categories, all_cuisines))
    
    
    
    
    if request.method == 'POST':
        tic = time.perf_counter()
        form_data = request.form

        # here you might want to select a category
        selected_categories = form_data.getlist("category_selection")
        selected_cuisine = form_data.getlist("cuisine_selection")

        # this accesses the string of words that was input in /search2
        query = form_data.getlist("text")[0]


        # select the category and pass them into a string if unless "all" is selected
        category_string_like = ""
        if "all" not in selected_categories and selected_categories != []:
            category_string_like = " (category LIKE "
            for i in selected_categories:
                category_string_like += '"' + str(i) + '%" '
                category_string_like += "or category LIKE "
            category_string_like += '"") AND'
            print(category_string_like)
        if selected_categories == []:
            selected_categories = "['all']"

        # select the cuisine and pass them into a string if unless "all" is selected
        cuisine_string_like = ""
        if "all" not in selected_cuisine and selected_cuisine != []:
            cuisine_string_like = " (cuisine LIKE "
            for i in selected_cuisine:
                cuisine_string_like += '"' + str(i) + '%" '
                cuisine_string_like += "or cuisine LIKE "
            cuisine_string_like += '"") AND'
            #print(cuisine_string_like)
        if selected_cuisine == []:
            selected_cuisine = "['all']"

        query_string_like = category_string_like + cuisine_string_like
        # now create the query string

        ###########################
        #########################
        # CHANGE MAIN FEATURES HERE:
        ###########################
        #########################

        query_string  = ("SELECT title, URL, image_link, chef, bm25(virtual_data_table), rating, rating_number, prep, snippet(virtual_data_table, 3, " + ' "<b>", "</b>", "...", 25) '+ " FROM virtual_data_table WHERE" 
                        + query_string_like +
                        " virtual_data_table MATCH (?) ORDER BY bm25(virtual_data_table)")
        print (query_string)
        import sqlite3
        conn = sqlite3.connect(database)
        c = conn.cursor()
        result = c.execute(query_string, [query])

        ###########################
        #########################
        # THE RESULTS ARE STORED HERE 
        ###########################
        #########################

        dbresults = result.fetchall()
        
        result = c.execute('''SELECT domain_URL FROM domains ''')
        all_drop_domains = result.fetchall()
        
        result = c.execute('''SELECT DISTINCT category FROM virtual_data_table WHERE virtual_data_table MATCH (?) ORDER BY category ASC''', [query])
        all_categories = result.fetchall()
        all_categories = [''.join(i) for i in all_categories]

        result = c.execute('''SELECT DISTINCT cuisine FROM virtual_data_table WHERE virtual_data_table MATCH (?) ORDER BY cuisine ASC''', [query])
        all_cuisines = result.fetchall()
        all_cuisines = [''.join(i) for i in all_cuisines]

        number_of_results = len(dbresults)
        toc = time.perf_counter()
        time_taken = round((toc-tic)*1000)
        
        ###########################
        #########################
        # AND PASSED ON TO THE CRAWLER HERE:
        ###########################
        #########################




        return render_template('data_post_report.html',dbresults = (dbresults, query, selected_categories, all_drop_domains, number_of_results, selected_cuisine, all_categories, all_cuisines, time_taken))




        ###########################
        #########################
        # WHEN HOSTING LOCALLY TURN debug=False 
        # to avoid malitious access to your python scrip
        ###########################
        #########################


if __name__ == "__main__":
    app.run(debug=True)


