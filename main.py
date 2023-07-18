"""
Code for a web scraping thing for papers

RANDOM IDEAS:
1. Go through sci-hub and open pdf directly
2. Citation graph
3. Make a dashboard
4. Read paper in reading list

TODO:
- Add crossref                                                          [ ]
- Add notes section                                                     [ ]
- Suggest new papers                                                    [ ]
- Add excalidraw notes                                                  [ ] 
- Add containers for every keyword/search query in the new papers       [ ]
- Make the groups draggable                                             [ ]
- Write init function                                                   [ ]
- Trigger load_readtables function more often...                        [ ]
- Add status bar                                                        [ ]
- Trigger the related papers only on startup                            [ ]
"""
 
import eel
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import warnings
import alex
from scrapedaddy import scrape_nature, scrape_pubmed

warnings.simplefilter(action='ignore', category=FutureWarning)
curdir = str(os.getcwd())
eel.init('web')


@eel.expose
def scrape_papers(keyword,pages):
    #df1 = scrape_nature(keyword,pages)
    #df2 = scrape_pubmed(keyword,pages)
    #df = df1.append(df2)
    df = alex.scrape_alex(keyword)
    df.to_csv('papers.csv', index=False)
    print("Saved df as csv")


@eel.expose
def load_csv(path,classes,id):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(path)

    # Return the DataFrame as html to be displayed in the GUI
    df = df.to_html(escape=False,classes=classes,table_id=id)
    return df

@eel.expose
def load_reading_list_csv(path,classe,id):
    '''
    Return a list containing html tables with the same id as in groupName
    '''
    html_tables = []

    # Load the CSV file into a DataFrame
    df = pd.read_csv(path)

    # Create an array of html tables with id corresponding to the group
    groups = list(set(df['Groupname']))
    colnames = df.columns.to_list().sort()

    for group in groups:
        table = pd.DataFrame(columns=colnames)

        for index, row in df.iterrows():
            
            if row['Groupname'] == group:
                table = table.append(row,ignore_index=True)
        

        # Keep the columns we want
        table = table.iloc[:, :-2]
        #table = table.drop("relevance_score",axis=1)

        # return the html of the df except the last two columns
        html_tables.append(table.to_html(escape=False,classes=classe,table_id=group))
    #print(html_tables)
    return html_tables
    


@eel.expose
def add_read_entry(keyword,group_name,title,file_path = "read_papers.csv",headers=[]):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # get the row containing the title of the paper to add
    df = pd.read_csv("papers.csv")
    add = df[df['title']==title].copy()

    # add keyword column and groupname column
    add.loc[add.loc[df['title'] == title].index,'Keyword']=keyword
    add.loc[add.loc[df['title'] == title].index,'Groupname']=group_name
    # pd.set_option('display.max_columns', None)
    # print(add)
    
    # add to csv with header if file not created
    if not file_exists or os.stat(file_path).st_size == 0:
            add.to_csv("read_papers.csv", mode='a', header=True, index=False)
            print("header created")
    else:
        add.to_csv("read_papers.csv", mode='a', header=False, index=False)
        print("entry added")

@eel.expose
def remove_read_entry(title, method = 'title', file_path = "read_papers.csv"):
    '''
    Removes entry from csv file

    PARAMETERS
    - title
    - file_path
    - method: The column name in which we want to iterate to find the element(s)
    '''
    print("remove method: "+method)
    # remove the entry from the read papers list
    df2 = pd.read_csv("read_papers.csv")
    df2 = df2[df2[method] != title]
    df2.to_csv("read_papers.csv", index=False)
    return("entry removed")

@eel.expose
def get_related_works(title,classes=None,id="relatedTable"):
    print(f"A search will be performed on the\nfollowing titles:{title}")
    print("searching related works...")
    related_papers_df = alex.get_new_related_works(title)[0]
    final_related_papers_df = related_papers_df.copy()

    # check if the related papers are already present
    for index, row in related_papers_df.iterrows():
        if related_papers_df.isin(row).all(axis=1).any():
            pass
        else:
            final_related_papers_df.append(row, ignore_index=True)

    print("loading to csv...")
    final_related_papers_df.to_csv("related_papers.csv",mode="a")
    print("converting to html...")
    html = final_related_papers_df.to_html(escape=False,classes=classes,table_id=id)
    

    print("Done!")

    return html

@eel.expose
def rename_group_name(old_name,new_name):
    """
    Rename the group name column if the groupname is changed after adding papers to read
    """
    print("old name:"+str(old_name)+"new name: "+new_name)
    df = pd.read_csv("read_papers.csv")
    df['Groupname'] = df['Groupname'].replace(old_name, new_name)

    df.to_csv("read_papers.csv", index=False)
    print("Groupname updated in read_papers.csv")
    return "DB updated with success!"


eel.start('index.html', size=(700, 800))
