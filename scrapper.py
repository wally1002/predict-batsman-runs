from bs4 import BeautifulSoup
import requests
import csv

class Player(object):
    def __init__(self, player_id):
        self.player_id = player_id
        self.data = {}

    def get_career_averages(self, file_name=None, match_format=11, data_type='allround') :

        """Get Player career averages

        Arguements:
            file_name {string}: File name to save data
            match_format {int}: Match format (default is 11) (1-Test), (2-Odi) (3-T20I), (11-All International), (20-Youth Tests), (21-Youth ODI)
            data_type {string}: Data type (default is allround) (allround, batting, bowling, fielding)
        
        Return:
            Data in csv file
        """
        self.match_format = match_format
        self.data_type = data_type
        self.file_name = file_name

        if self.file_name is None:
            self.file_name = f"{self.player_id}_{self.match_format}_{self.data_type}_career_averages.csv"

        self.url=f"https://stats.espncricinfo.com/ci/engine/player/{self.player_id}.html?class={self.match_format};template=results;type={self.data_type}"
        html_doc = requests.get(self.url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        tables = soup.find_all("table")[2]
        table_rows = tables.find_all("tr")
        scores =[]
        for tr in table_rows:
            scores.append(tr.text)
        with open(self.file_name, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for row in scores:
                    writer.writerow(row.splitlines()[1:]) 
    
    def get_career_summary(self, file_name=None, match_format=11, data_type='allround'):
        
        """Get Player data match by match sorted by date

        Arguements:
            file_name {string}: File name to save data
            match_format {int}: Match format (default is 11) (1-Test), (2-Odi) (3-T20I), (11-All International), (20-Youth Tests), (21-Youth ODI)
            data_type {string}: Data type (default is allround) (allround, batting, bowling, fielding)
        
        Return:
            Data in csv file
        """
        self.match_format = match_format
        self.data_type = data_type
        self.file_name = file_name

        if self.file_name is None:
            self.file_name = f"{self.player_id}_{self.match_format}_{self.data_type}_career_summary.csv"

        self.url=f"https://stats.espncricinfo.com/ci/engine/player/{self.player_id}.html?class={self.match_format};template=results;type={self.data_type}"
        html_doc = requests.get(self.url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        tables = soup.find_all("table")[3]
        table_rows = tables.find_all("tr")
        scores =[]
        for tr in table_rows:
            scores.append(tr.text)
        with open(self.file_name, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for row in scores:
                    writer.writerow(row.splitlines())

    def get_data(self, file_name=None, match_format=11, data_type='allround', view='match'):

        """Get Player data match by match sorted by date

        Arguements:
            file_name {string}: File name to save data
            match_format {int}: Match format (default is 11) (1-Test), (2-Odi) (3-T20I), (11-All International), (20-Youth Tests), (21-Youth ODI)
            data_type {string}: Data type (default is allround) (allround, batting, bowling, fielding)
            view {string}: View type (default is match) (match, innings, cumulative, reverse_cumulative, series, tour, ground)
        
        Return:
            Data in csv file
        """
        self.match_format = match_format
        self.data_type = data_type
        self.view = view
        self.file_name = file_name

        if self.file_name is None:
            self.file_name = f"{self.player_id}_{self.match_format}_{self.data_type}_{self.view}.csv"

        self.url=f"https://stats.espncricinfo.com/ci/engine/player/{self.player_id}.html?class={self.match_format};template=results;type={self.data_type};view={self.view}"
        html_doc = requests.get(self.url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        tables = soup.find_all("table")[3]
        table_rows = tables.find_all("tr")
        scores =[]
        match_data = []
        for tr in table_rows:
            scores.append(tr.text)
        for row in scores:
                match_data.append(row.splitlines()[1:]) 
        match_data[0][-1] = 'match_id'
        self.data[f'{self.view}_{self.match_format}_{self.data_type}'] = match_data