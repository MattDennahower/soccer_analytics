import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_match_data(url):
    """
    This function retrieves match data from a given URL, cleans the data, and saves it to a CSV file.
    The URL should point to a match page on fbref.com.

    Parameters:
    url (str): The URL of the match page.

    Returns:
    None
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        tables = pd.read_html(data, header=1)  # Skip the first row when reading the table
        combined_table = pd.DataFrame()

        # Extract the team names and date from the URL
        url_parts = url.split('/')[-1].split('-')
        teams = [' '.join(url_parts[i].split('-')) for i in range(2)]
        date = '-'.join(url_parts[2:5])

        for i, table in enumerate(tables):
            if i == 3 or i == 10:  # 4th and 11th tables have indices 3 and 10
                table = table.iloc[:-1]  # Remove the last row
                team = teams[0] if i == 3 else teams[1]  # Assign the team name based on the table index
                table['Team'] = team  # Add a new 'Team' column

                # Clean the 'Nation' column
                if 'Nation' in table.columns:
                    table['Nation'] = table['Nation'].apply(lambda x: ''.join([c for c in x.split()[-1] if c.isupper()]))

                combined_table = pd.concat([combined_table, table], ignore_index=True)

        # Save the combined table to a CSV file named after the teams and date
        output_file = f'{teams[0]}_vs_{teams[1]}_{date}.csv'
        combined_table.to_csv(output_file, index=False)
        print(f'Tables saved to {output_file}.')
    else:
        print('Failed to retrieve data. Status code:', response.status_code)

def main():
    """
    This is the main function that calls the get_match_data function with a sample URL.
    """
    link = 'https://fbref.com/en/matches/sample-match-url'
    get_match_data(link)

if __name__ == '__main__':
    main()