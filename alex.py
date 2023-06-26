from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
import pandas as pd
from datetime import datetime


def scrape_alex(keyword,filters=None,data_list=["title","publication_date","author","relevance_score","cited_by_count","doi"],config_email="favey.quillan@gmail.com"):
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
        # init the df
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

def get_new_related_works(title,data_list=["title","publication_date","author","cited_by_count","doi"]):
    """
    Gets the related works of a paper and returns two dfs one with 
    all related and one with new papers from the current date

    PARAMETERS
    - title:    a list of titles
    """
    # A few variables
    
    current_date = datetime.now().date()

    # to keep track of similar papers
    related_papers = []
    new_related_papers = []

    # init the dataframe
    related_df = {}
    new_df = {}
    for data in data_list:
        related_df[data] = []
        new_df[data] = []

    for tit in title:  
        add_to_new = False
        # get the related works
        related_works = Works().search(tit).get()[0]["related_works"] #maybe using the OA ID would be better

        # get the data of the individual related works
        for work in related_works:
            related_paper = Works()[work[21:]]

            if datetime.strptime(related_paper["publication_date"],"%Y-%m-%d").date()>=current_date and related_paper["id"] not in new_related_papers:
                add_to_new = True
                new_related_papers.append(related_paper["id"])

            if related_paper["id"] not in related_papers:
                related_papers.append(related_paper["id"])

                for data in data_list:
                # a bit of twerking for the author name
                    if data == "author":
                            #print(work["authorships"][0]["author"]["display_name"])
                            related_df[data].append(related_paper["authorships"][0]["author"]["display_name"])
                            if add_to_new == True:
                                new_df[data].append(related_paper["authorships"][0]["author"]["display_name"])
                    else:    
                        try:
                            if add_to_new == True:
                                new_df[data].append(related_paper[data])
                            related_df[data].append(related_paper[data])
                        except:
                            if add_to_new == True:
                                new_df[data].append("N/A")
                            related_df[data].append("N/A")

    related_df = pd.DataFrame(related_df)
    new_df = pd.DataFrame(new_df)
    related_df['doi'] = related_df['doi'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    return related_df, new_df

#print(Authors().search("Neuhauss").get())
paper = scrape_alex("zebrafish")
paper_title = paper.at[0,"title"]
print(get_new_related_works([paper_title])[1])