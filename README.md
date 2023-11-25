# sqlalchemy-challenge
Completed by Daniel Stephens

## About this project
This is a two part project demonstarting use of SQLAlchemy to reflect and query SQL databases in Python, Pandas to convert query results to dataframes and perform analysis, Matplotlib to generate visualizaitons, and Flask to generate an API that retrieves the data. 

### climate.ipynb
This notebook reflects a SQLite database that contains precipitation and temperature data captured from multiple weather stations in Hawaii. After reflecting the database and creating a session, we perform multiple queries and then convert the results to a Pandas dataframe. Finally, we use Matplotlib to generate visualizations. 

The notebook can be accessed in the [HawaiiClimate](HawaiiClimate) folder in this repo.
Note: If downloading the notebook to run locally, download the entire repo and retain the file structure. The notebook and python app reference the database file in the Resources folder. 

### app.py
This is a Python application that uses Flask to generate an API that returns much of the data from the climate notebook. The app will reflect the database, open a session, query the database, and return results in JSON based on the endpoint.

The app can be accessed in the [HawaiiClimate](HawaiiClimate) folder in this repo.

#### Running the app

To run the app: 
* Download the complete repo. Retain the file structure and do not move files from the folders as the notebook and python app reference the database file in the Resources folder. 
* Once downloaded use the terminal to run app.py from the HawaiiClimate folder
* As the app starts a local server will start and the address will be returned in the terminal
* Paste the address to the server in your browser to get an index of the endpoints

