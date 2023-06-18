"""
Code for a web scraping thing for papers

TODO:
- Get the checkboxes of the results to be checked with the read papers  [v]
- Suggest new papers                                                    [ ]
- Add containers for every keyword/search query in the reading list     [ ]
- Add containers for every keyword/search query in the new papers       [ ]
- Press Enter to search                                                 [v]
- Remove group name input                                               [ ]
- Fix the open of the collapsibles                                      [v]
- Fix the remove paper issue                                            [v]
- Container gets the class name of the input                            [v]
- Handle spaces as input to the container                               [v]
"""
 
import eel
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import csv

curdir = str(os.getcwd())
eel.init('web')

def scrape_nature(keyword,pages):

    # Create empty lists to store the paper details
    titles = []
    authors = []
    #abstracts = []
    dates = []
    links = []

    if pages == '':
        pages = 2
    else:
        pages = int(pages)
    

    for i in range(1,pages):
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
    data = {'Title': titles, 'Authors': authors, 'Date of Publication': dates, "Links": links}
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
def add_read_entry(keyword,title,file_path = "read_papers.csv",headers=[]):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)
    # get the row containing the title of the paper to add
    df = pd.read_csv("papers.csv")
    add = df[df['Title']==title]
    df['Keyowrd'] = keyword
        
    if not file_exists or os.stat(file_path).st_size == 0:
            add.to_csv("read_papers.csv", mode='a', header=True, index=False)
            print("header created")
    else:
        add.to_csv("read_papers.csv", mode='a', header=False, index=False)
        print("entry added")

@eel.expose
def remove_read_entry(keyword,title,file_path = "read_papers.csv",headers=[]):
    # get the row containing the title of the paper to add
    df = pd.read_csv("papers.csv")
    remove = df[df['Title']==title]
    # remove the entry from the read papers list
    df2 = pd.read_csv("read_papers.csv")
    df2 = df2[df2['Title'] != title]
    df2.to_csv("read_papers.csv", index=False)
    print("entry removed")


eel.start('index.html', size=(1000, 800))
