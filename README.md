# web-scraping-challenge
Web Scraping Homework

I had major problems with this homework! Several approaches that were discussed and others that I found online did not work as indicated.
I suspect I have some fundamental lack of understanding on how Flask works and integration with MongoDB and HTML. The problems are as follows:

1. Python extraction and scraping of the data was not that difficult. However, I had SEVERE problems with instability on Twitter. Many if not 
most of the time, my scraping would be held up because the Twitter extraction would fail. I became so fed up with this problem that I found another
website from NASA and used their iframe to resolve this problem. I still have the Twitter code, but I feel that such instability is highly problematic!
I have two files for scraping: mission_to_mars.py is the direct scraping program not linked to the scrape function, scrape_mars.py is the program
with the def scrape(): defined function for calling in the Flask/HTML application.

2. Translation to MongoDB from Python/Pandas worked extremely well using the standard approach:

	conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

	db = client.Mars_DataDB
    collection = db.scraped_mars_data

	collection.drop()

    for data in total_mars_data:
    collection.insert_one(data)
	
This worked directly and I tested exhaustively (at least 20-30 times). The MongoDB interface did not fail once. I tracked about 15 failures and all
except 2 were attributed to Twitter.
	
3. My initial attempts on the app.py in Flask were EXTREMELY PROBLEMATIC!
	A. Attempts to use the similar approach as in Python/Pandas failed multiple times. I could not establish an effective connection for some reason.
	B. Using the app.config and mongo=PyMongo(app) approach did establish an effective MongoDB connection. I still would like to understand why the 
		Python method failed given that Flask is a Python library.
	C. A MAJOR time sink (about 12 hours or so) was spent trying to understand why MongoDB extration could not be done directly in Flask. This was a 
		major impediment on my work in this project.
		
			mars_data = scraped_mars_data.find() worked well in extracting all of the data in the scraped_mars_data database collection.
			
			mars_data = scraped_mars_data.find({"key": "value"}) approach to try to get specific subsets of the database collection failed. This was
			more troubling because the same .find approach worked great for MongoDB directly. This caused some of the major problems in the HTML file
			as well.
			
4. In the HTML file (index.html), I made almost 100 attempts to use the main approach that was demonstrated in class, I found online, and discussed
	with other students.
	
			The following iteration approach worked to a degree:
	
			{% for data in mars_data %}
            <tr>
              <td>{{ data.title }}</td>
              <td>{{ data.teaser }}</td>
              <td>{{ data.reference }}</td>
            </tr>
            {% endfor %}
			
			I used this to generate the News Title table with Paragraph and Reference data. This worked for all of the lines in the MongoDB
			that had these keys and values. However, a number of extra rows appears to be appended to the end of the table and the number of rows is
			exactly the same as the remaining dictionaries in the MongoDB table. The iteration tried to make table entries for all of the MongoDB
			data, not just the iterations with the appropriate data. This is why the extraction of data for specific data in the scraped_mars_data trials
			in Item 3 above was so important and troubling to me. I needed to extract only the data I wanted for analysis, and could do so in MongoDB,
			but not in this Flask application.
			
			This same problem occurs in the bottom table. This time was much more obvious because there were only 4 rows of hemisphere data. The table
			obviously hase 44 rows of not-hemisphere data, so these rows are blank, but present.
			
			{% for data2 in mars_data2 %}
            <tr>
              <td>{{ data2.hemisphere }}</td>
              <td>{{ data2.image_url }}</td>
            </tr>
			{% endfor %}
			
			Finally, there are numerous examples of the following coding, using the mars_data extraction that I used in Item 3 above:
			
			{{mars_data.featured_image_url}} should have specifically identified the featured_image_url in the mars_data. This is copied from the classa
			activities. More generally, {{mars_data.keys}} should extract the value for that key. This may be more complex because many dictionaries have
			several keys and values. However, I was able to use MongoDB coding like scraped_mars_data.find("key":"/.*XYZ.*/) to extract specific data. I could
			find no approach to do the same in the Flask app, so the index.html file is very rough and not completely finished.
			
			In the future, my plan would be to not generate a large MongoDB collection, but to use specific collections for specific data types in Flask. 
			This should enable extraction only on the data necessary for construction of proper tables and use of iteration only on the required data.
			
			I still do not understand why the {{mars_data.featured_image_url}} test did not work. There was only one dictionary in mars_data and there was only
			one key, featured_image_url. There is something I fundamentally do not understand here.
			
5. Many problems with formatting of the html file, but a lot of this was me spending too much time on problems with the Flask data extraction and table problems.
			
			
I would appreciate if Elsa, Kirby, or Chris would look over this in some detail and take 30 minutes soon to restore my sanity! This was extremely frustrating!
			
			
			
			
			
			
			
			