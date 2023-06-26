### functions to read in sql data from mysql database

# IMPORTS
from env import user, password, host
from sqlalchemy import text, create_engine
import pandas as pd

# FUNCTIONS
# defining a function to return a string that is a url for accessing Codeup mysql server
def get_db_url(db_name, user=user, host=host, password=password):
    '''
    get_db_url accepts a database name, username, hostname, password 
    and returns a url connection string formatted to work with codeup's 
    sql database.
    Default values from env.py are provided for user, host, and password.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'

# generic function to get a sql pull into a dataframe
def get_mysql_data(sql_query, database):
    """
    This function will:
    - take in a sql query and a database (both strings)
    - create a connection url to mySQL database
    - return a df of the given query, connection_url combo
    - cao May 2023, new pandas update changed sql pulls, and this is up to date
    """
    # get the url with the user, password, host info
    url = get_db_url(database)
    # create this "engine" and use it to make a "connection"
    engine = create_engine(url)
    connection = engine.connect()
    # use text function to turn a string query into the format needed
    query = text(sql_query)
    # Now we can use the connection and read the query into a df
    df = pd.read_sql(query, connection)
    
    return df   
