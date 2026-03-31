/* 
File name: kicker_stats.js 

Authors: Timothy Birmingham

Description: Contains js functionality to enable additional functionality in the "add-kicker"
        dropdown menus

Code Citations: The code in this file represents all original work by the author
*/

const kickerSelect = document.getElementById("kicker_id");
const weekSelect = document.getElementById("week");
const yearSelect = document.getElementById("year");

let kicker_games = [];

kickerSelect.addEventListener("change", async () => {
    const kickerId = kickerSelect.value;    // grab the selected player's ID from kicker_stats page
    if (!kickerId) return;

    // Send a asynchronous request to Flask to get games for the given player
    const response = await fetch(`/kicker-stats/${kickerId}`);
    kicker_games = await response.json(); // JSON array of games

    // Clear previous options in the week dropdown
    weekSelect.innerHTML = '<option value="" disabled selected hidden>Select Week</option>';
    yearSelect.innerHTML = '<option value="" disabled selected hidden>Select Year</option>';

    // Keep track of years already added (to avoid duplicates)
    const yearsAdded = new Set();

    // Populate dropdowns dynamically
    kicker_games.forEach(game => {
        // First weeks...
        weekSelect.innerHTML += `<option value="${game.week_number}">${game.week_number}</option>`;

        // Then years dropdown, avoiding duplicates
        if (!yearsAdded.has(game.year)) {
            yearSelect.innerHTML += `<option value="${game.year}">${game.year}</option>`;
            yearsAdded.add(game.year);
        }
    });

    // Enable dropdowns
    weekSelect.disabled = false;
    yearSelect.disabled = false;
})

// Now populate the home and away team names based on the given selection
const homeInput = document.getElementById("home_team_name");
const awayInput = document.getElementById("away_team_name");
const homeIdInput = document.getElementById("home_team_id");
const awayIdInput = document.getElementById("away_team_id");

function updateTeams() {
    const selectedWeek = parseInt(weekSelect.value);
    const selectedYear = parseInt(yearSelect.value);

    // If one isn't selected yet, stop
    if (!selectedWeek || !selectedYear) return;

    const game = kicker_games.find(g =>
        g.week_number === selectedWeek &&
        g.year === selectedYear
    );

    if (game) {
        homeInput.value = game.home_team;
        awayInput.value = game.away_team;

        homeIdInput.value = game.home_team_id;
        awayIdInput.value = game.away_team_id;
    }
}

weekSelect.addEventListener("change", updateTeams);
yearSelect.addEventListener("change", updateTeams);
