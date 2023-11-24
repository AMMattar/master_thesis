import requests
import pandas as pd
from bs4 import BeautifulSoup

# Set the URL for the website with the player statistics
url = "https://www.transfermarkt.com/lionel-messi/leistungsdaten/spieler/28003/plus/0?saison=2018"

# Send a request to the website and get the HTML content
response = requests.get(url, headers={'User-Agent': 'Custom'})
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the table with the player statistics and extract the data
table = soup.find("table", {"class": "items"})
rows = table.find_all("tr")

# Create empty lists to store the data
months = []
goals = []
assists = []
yellow_cards = []
red_cards = []
minutes_played_player = []
minutes_played_team = []
international_games = []
# Loop through each row in the table and extract the data
for row in rows[1:]:
    cells = row.find_all("td")
    month = cells[1].text.split()[0] + " " + cells[1].text.split()[1]
    months.append(month)
    goals.append(cells[4].text)
    assists.append(cells[5].text)
    yellow_cards.append(cells[6].text)
    red_cards.append(cells[7].text)
    minutes_played_player.append(cells[8].text)
    minutes_played_team.append(cells[9].text)
    international_games.append(cells[10].text)

# Create a pandas DataFrame with the extracted data
data = {
    "Month": months,
    "Goals": goals,
    "Assists": assists,
    "Yellow Cards": yellow_cards,
    "Red Cards": red_cards,
    "Minutes Played by Player": minutes_played_player,
    "Minutes Played by Team": minutes_played_team,
    "Participated in International Games": international_games,
}
df = pd.DataFrame(data)

# Group the data by month and aggregate the values
df = df.groupby("Month").agg(
    {
        "Goals": "sum",
        "Assists": "sum",
        "Yellow Cards": "sum",
        "Red Cards": "sum",
        "Minutes Played by Player": "sum",
        "Minutes Played by Team": "sum",
        "Participated in International Games": lambda x: "Yes" if "Yes" in list(x) else "No",
    }
)

# Write the DataFrame to a CSV file
df.to_csv("lionel_messi_stats_monthly.csv")