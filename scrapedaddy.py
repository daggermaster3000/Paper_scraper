import pandas as pd
import requests
from bs4 import BeautifulSoup

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