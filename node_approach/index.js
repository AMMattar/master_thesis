const axios = require("axios");
const cheerio = require("cheerio");
const fs = require("fs");

// Define the base URL of the Transfermarkt.com page
const baseUrl = "https://www.transfermarkt.com/lionel-messi/leistungsdaten/spieler/28003/plus/0?";

// Define the list of seasons to extract data for
const seasons = ["saison=2018"];

// Define the list of columns to extract for each match day
const columns = ["Spieltag", "Pos", "Wettbewerb", "Begegnung", "Tore", "Assists", "Gelbe Karten", "Gelb-Rote Karten", "Rote Karten", "Eingesetzt", "Einwechslungen", "Auswechslungen", "Minuten"];

// Loop through each season and extract the data
for (const season of seasons) {
    // Construct the URL for the current season
    const url = `${baseUrl}/${season}`;
    
    // Send a GET request to the URL and get the HTML content
    axios.get(url)
        .then(response => {
            // Load the HTML content using Cheerio
            const $ = cheerio.load(response.data);

            // Find the table that contains the performance data
            const table = $("table.items");
            //console.log(table.find("thead tr").find("th"));
            // Extract the table headers
            const headers = [];
            const headerRow = table.find("thead tr");
            headerRow.find("th").each((i, el) => {
                const headerText = $(el).text().trim();
                console.log(headerText);
                if (columns.includes(headerText)) {
                    console.log(columns.includes(headerText));
                    headers.push(headerText);
                }
            });
            console.log(headers);
            // Extract the table data
            const dataRows = [];
            const dataRowsEls = table.find("tbody tr");
            dataRowsEls.each((i, rowEl) => {
                const dataCells = [];
                $(rowEl).find("td").each((j, cellEl) => {
                    const dataText = $(cellEl).text().trim();
                    if (columns.includes(headers[j])) {
                        dataCells.push(dataText);
                    }
                });
                dataRows.push(dataCells);
            });
            console.log(dataRows);
            // Split the data into groups by match day
            const matchesByMatchDay = {};
            dataRows.forEach(row => {
                const matchDay = row[0];
                if (!matchesByMatchDay[matchDay]) {
                    matchesByMatchDay[matchDay] = [];
                }
                const rowData = [row[0], row[3], row[4], row[5], row[6], row[7], row[9], row[10], row[11], row[12]];
                matchesByMatchDay[matchDay].push(rowData);
            });
            
            // Write the CSV file for each match day
            Object.keys(matchesByMatchDay).forEach(matchDay => {
                const seasonName = season === "gesamt" ? "all" : season.split("/")[1];
                const csvString = "Match Day,Opponent,Goals,Assists,Yellow Cards,Red Cards,Time Played\n" + matchesByMatchDay[matchDay].map(row => row.join(",")).join("\n");
                fs.writeFileSync(`lionel_messi_performance_${seasonName}_matchday_${matchDay}.csv`, csvString, "utf8");
            });
        })
        .catch(error => {
            console.log(error);
        });
}