# Risk_estimator_supply_chain

This web tool build with Django does the following:

Scrapes through the internet to find relevant information on a particular supplier from various sources like: LinkedIn, Google Finance, BBC, CNN and other news sources.

Wrangles, pre-processes and translates the information to a common language and creates a data base out of the scraped data for each of the suppliers. 

Ranks the suppliers based on:

             1. The sentiment analysis (using Natural Language Processing)  of linkedIn setiments.
             2. Statistical evaluation of financial information.
             3. Key word matching of "supply chain risky" words in the news medias, like flood, war etc. in the city or country of the geophrical location of                   the supplier.
             (If one or more information is not available for a aprticular supplier, they are listed at the bottom depending on the number of informations                         unavailable and the importance of that information)
 
 Allows the user to serach for a supplier and informs the user about the quantitative and qualititative risks associated with them along with the rank of the supplier as compared to the other suppliers in the database. 
 
 Keeps an history of every search and displays it on dashboard in a tabular format with a time stamp to keep track of the performance record of a particular supplier over time. Useful for prediction of the best suppliers in future 
             
