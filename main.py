"""
Code for a web scraping thing for papers

RANDOM IDEAS:
1. Go through sci-hub and open pdf directly
2. Citation graph
3. Make a dashboard
4. Read paper in reading list

TODO:
- Delete button backend                                                 [ ]
- Clean the code up                                                     [ ]
- Add open Alex                                                         [ ]
- Add elsevier + google scholar + add chose DB                          [ ]
- Suggest new papers                                                    [ ]
- Add containers for every keyword/search query in the new papers       [ ]
- Make the groups draggable                                             [ ]
- Write init function                                                   [ ]
- Trigger load_readtables function more often...                        [ ]
- Fix the readlist single delete bug                                    [ ]
"""
 
import eel
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import numpy as np

curdir = str(os.getcwd())
eel.init('web')

def scrape_nature(keyword,pages):
    '''Scrape the nature website for a given keyword in a number of pages'''

    # Create empty lists to store the paper details
    titles = []
    authors = []
    #abstracts = []
    dates = []
    links = []
    citations = []

    if pages == '':
        pages = 2
    else:
        pages = int(pages)

    for i in range(1, pages):
        url = f"https://www.nature.com/search?q={keyword}&order=relevance&page={i}"  # URL for Nature search with the keyword

        # Send a GET request to the website
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the relevant elements containing the paper information
        articles = soup.find_all('li', class_='app-article-list-row__item')  # Replace 'li' and 'class_' with the appropriate HTML tags and attributes

        # Extract and process the paper details
        for article in articles:
            title_element = article.find('a', class_='c-card__link')  # Replace 'a' and 'class_' with the appropriate HTML tags and attributes
            authors_element = article.find('ul', class_='c-author-list')  # Replace 'ul' and 'class_' with the appropriate HTML tags and attributes
            #abstract_element = article.find('div', class_='c-card__section')  # Replace 'div' and 'class_' with the appropriate HTML tags and attributes
            date_element = article.find('time')
           
            # Extract the text from the elements if they exist
            title = title_element.text.strip() if title_element else "N/A"
            author = authors_element.text.strip() if authors_element else "N/A"
            #abstract = abstract_element.text.strip() if abstract_element else "N/A"
            date = date_element['datetime'] if date_element else "N/A"
            link = title_element['href'] if title_element else "N/A"
            

            # Append the paper details to the corresponding lists
            if title not in titles: 
                titles.append(title)
                authors.append(author)
                #abstracts.append(abstract)
                dates.append(date)
                links.append(f'https://www.nature.com{link}')
                

            # Create a DataFrame from the lists of paper details
            data = {'Title': titles, 'Authors': authors, 'Date of Publication': dates, 'Links': links}
            df = pd.DataFrame(data)
            # format the hyperlinks
            df['Links'] = df['Links'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    return df



def scrape_pubmed(keyword,pages):

    # Create empty lists to store the paper details
    titles = []
    authors = []
    dates = []
    links = []
    if pages == '':
        pages = 2
    else:
        pages = int(pages)

    for i in range(0,pages):
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={keyword}&page={i}"  # PubMed search URL with the keyword

        # Send a GET request to the website
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the relevant elements containing the paper information
        articles = soup.find_all('div', class_='docsum-content')  # Replace 'div' and 'class_' with the appropriate HTML tags and attributes


        # Extract and process the paper details
        for article in articles:
            title_element = article.find('a', class_='docsum-title')  # Replace 'a' and 'class_' with the appropriate HTML tags and attributes
            authors_element = article.find('span', class_='docsum-authors')  # Replace 'span' and 'class_' with the appropriate HTML tags and attributes
            date_element = article.find('span', class_='docsum-journal-citation-date')

            # Extract the text from the elements if they exist
            title = title_element.text.strip() if title_element else "N/A"
            author = authors_element.text.strip() if authors_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = title_element['href'] if title_element else "N/A"

            # Append the paper details to the corresponding lists
            if title not in titles:
                titles.append(title)
                authors.append(author)
                dates.append(date)
                links.append(f'https://pubmed.ncbi.nlm.nih.gov{link}')

    # Create a DataFrame from the lists of paper details
    data = {'Title': titles, 'Authors': authors, 'Date of Publication': dates, "Links": links}
    df = pd.DataFrame(data)
    # Format the hyperlinks
    df['Links'] = df['Links'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    return df


@eel.expose
def scrape_papers(keyword,pages):
    df1 = scrape_nature(keyword,pages)
    df2 = scrape_pubmed(keyword,pages)
    df = df1.append(df2)
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
        classes = classe+" "+group
        #print(classes)
        # return the html of the df except the last two columns
        html_tables.append(table.iloc[:, :-2].to_html(escape=False,classes=classes,table_id=id))
    #print(html_tables)
    return html_tables
    


@eel.expose
def add_read_entry(keyword,group_name,title,file_path = "read_papers.csv",headers=[]):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # get the row containing the title of the paper to add
    df = pd.read_csv("papers.csv")
    add = df[df['Title']==title].copy()

    # add keyword column and groupname column
    add.loc[add.loc[df['Title'] == title].index,'Keyword']=keyword
    add.loc[add.loc[df['Title'] == title].index,'Groupname']=group_name
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
def remove_read_entry(title, method = 'Title', file_path = "read_papers.csv"):
    '''
    Removes entry from csv file

    PARAMETERS
    - title
    - file_path
    - method: The column name in which we want to iterate to find the element(s)
    '''
    print(method)
    # remove the entry from the read papers list
    df2 = pd.read_csv("read_papers.csv")
    df2 = df2[df2[method] != title]
    df2.to_csv("read_papers.csv", index=False)
    print("entry removed")


eel.start('index.html', size=(1000, 800))
