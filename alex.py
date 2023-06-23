from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
import pandas as pd


def scrape_alex(keyword,filters=None,data_list=["title","publication_year","author","relevance_score","cited_by_count","doi"],config_email="favey.quillan@gmail.com"):
    '''
    Function to search papers in open alex

    PARAMETERS:
    - keyword
    - data_list:        list of the information we want eg. title, doi, ...
    - filters:          list of filters we want to apply to the query
    - config_email:     config email for faster searching...

    RETURNS
    - a dataframe with data_list as header (the order is kept)
    '''

    pyalex.config.email = config_email

    df = {}

    #search the OpenAlex
    works = Works().search(keyword).get()

    for data in data_list:
        df[data] = []
        # a bit of twerking for the author name
        if data == "author":
            for work in works:
                #print(work["authorships"][0]["author"]["display_name"])
                df[data].append(work["authorships"][0]["author"]["display_name"])
        else:    
            for work in works:
                df[data].append(work[data])

    df = pd.DataFrame(df)
    df['doi'] = df['doi'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    
    return(df)

def get_related_works(OA_ID):
    ...

#print(scrape_alex(keyword = "zebrafish csf")["authors"])