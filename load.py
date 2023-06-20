import pandas as pd


def load_reading_list_csv(path,id="myTable"):
    '''
    Return a list containing html tables with the same id as in groupName
    '''
    html_tables = []

    # Load the CSV file into a DataFrame
    df = pd.read_csv(path)

    # Create an array of html tables with id corresponding to the group
    groups = list(set(df['Groupname']))
    colnames = df.columns.to_list()

    for group in groups:
        table = pd.DataFrame(columns=colnames)

        for index, row in df.iterrows():

            if row['Groupname'] == group:
                pd.concat([table,row])
        classes = "table "+group
        html_tables.append(table.to_html(escape=False,classes=classes,table_id=id))

    print(html_tables)
    return html_tables
    
load_reading_list_csv("read_papers.csv")