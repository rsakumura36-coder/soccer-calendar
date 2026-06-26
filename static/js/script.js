const allTeams = window.allTeams || {};

const leagueSelect = document.querySelector('select[name="league"]');
const teamSelect = document.querySelector('select[name="team_id"]');

leagueSelect.addEventListener("change", function () {

    const league = this.value;
    teamSelect.innerHTML = "";

    for (const [name, id] of Object.entries(allTeams[league])) {

        const option = document.createElement("option");
        option.value = id;
        option.textContent = name;

        teamSelect.appendChild(option);
    }
});