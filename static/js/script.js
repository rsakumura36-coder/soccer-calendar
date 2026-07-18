document.addEventListener("DOMContentLoaded", function () {

    const allTeams = window.allTeams || {};

    const leagueSelect = document.querySelector('select[name="league"]');
    const teamSelect = document.querySelector('select[name="team_id"]');

    // =========================
    // DOM安全チェック
    // =========================
    if (!leagueSelect || !teamSelect) {
        console.warn("leagueSelect or teamSelect not found");
        return;
    }

      // =========================
    // チーム更新
    // =========================
    function updateTeams(league) {

        console.log("selected league:", league);

        const teams = allTeams?.[league] || {};

        teamSelect.innerHTML = "";

        for (const [name, team] of Object.entries(teams)) {

            console.log(name, team);

            const option = document.createElement("option");

            option.value = team.id;

            option.textContent = name;

            option.dataset.logo = team.logo;

            teamSelect.appendChild(option);
        }
    }

    // =========================
    // リーグ変更イベント
    // =========================
    leagueSelect.addEventListener("change", function () {
        updateTeams(this.value);
    });

    // 初期表示
    updateTeams(leagueSelect.value);

    // =========================
    // お気に入り登録（検索画面）
    // =========================
    const favoriteTeamBtn = document.getElementById("favorite-team-btn");

    if (favoriteTeamBtn) {

        favoriteTeamBtn.addEventListener("click", function () {

            const teamId = teamSelect.value;

            const teamName =
                teamSelect.options[teamSelect.selectedIndex].text;

            const logo =
                teamSelect.options[teamSelect.selectedIndex].dataset.logo;


            const team = {
                id: teamId,
                name: teamName,
                logo: logo
            };


            let favorites =
                JSON.parse(localStorage.getItem("favorites")) || [];


            if (!favorites.some(t => t.id === team.id)) {

                favorites.push(team);

                localStorage.setItem(
                    "favorites",
                    JSON.stringify(favorites)
                );

                alert(`${team.name} をお気に入りに登録しました！`);

                renderFavorites();

                loadFavoriteMatches();


            } else {

                alert("すでに登録されています。");

            }

        });

    }

});

// ======================================================
// ⭐ お気に入り機能（登録・削除・表示）
// ======================================================

// =========================
// お気に入り表示
// =========================
function renderFavorites() {

    const list = document.getElementById("favorite-list");

    if (!list) return;


    let favorites =
        JSON.parse(localStorage.getItem("favorites")) || [];


    if (favorites.length === 0) {

        list.innerHTML = `
            <li class="list-group-item text-muted text-center">
                まだお気に入りはありません。
            </li>
        `;

        return;
    }


    const html = favorites.map(team => `

        <li class="list-group-item d-flex justify-content-between align-items-center">


            <button
                class="btn btn-link favorite-team-select d-flex align-items-center"
                data-id="${team.id}">


                ${
                    team.logo
                    ?
                    `<img 
                        src="${team.logo}"
                        width="30"
                        class="me-2"
                    >`
                    :
                    "⚽"
                }


                ${team.name}


            </button>



            <button
                class="btn btn-sm btn-outline-danger remove-favorite"
                data-id="${team.id}">

                ×

            </button>


        </li>


    `).join("");


    list.innerHTML = html;
}

document.addEventListener("click", function (e) {

    // 削除ボタン
    if (e.target.classList.contains("remove-favorite")) {

        const id = e.target.dataset.id;

        let favorites =
            JSON.parse(localStorage.getItem("favorites")) || [];

        favorites = favorites.filter(team => team.id !== id);

        localStorage.setItem(
            "favorites",
            JSON.stringify(favorites)
        );

        renderFavorites();

        return;

    }

    // チーム選択
    if (e.target.classList.contains("favorite-team-select")) {

        const teamId = e.target.dataset.id;

        loadTeamMatches(teamId);

        return;

    }

    //戻る処理
    if (e.target.id === "back-favorites-btn") {

        loadFavoriteMatches();

        e.target.style.display = "none";

        return;

    }


});

// =========================
// お気に入りチームの試合取得
// =========================
function formatDate(dateString) {

    const date = new Date(dateString);

    return date.toLocaleString(
        "ja-JP",
        {
            year: "numeric",
            month: "long",
            day: "numeric",
            weekday: "short",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}

function translateCompetition(name) {

    const map = {
        "Premier League": "プレミアリーグ",
        "Primera Division": "ラ・リーガ",
        "National Teams": "代表戦"
    };

    return map[name] || name;
}

async function loadFavoriteMatches() {

    const favorites =
        JSON.parse(localStorage.getItem("favorites")) || [];

    if (favorites.length === 0) {

        const weekly = document.getElementById("weekly-matches");

        if(weekly){
            weekly.innerHTML =
            "<p class='text-muted text-center'>お気に入りチームを登録してください。</p>";
        }

        return;
    }

    let favoriteMatches = [];

    for (const team of favorites) {

        const response = await fetch(`/api/team/${team.id}`);

        if(!response.ok){

            console.log(
                "API error:",
                team.name,
                team.id,
                response.status
            );

            continue;
        }

        const matches = await response.json();

        // 未来の試合だけ
        const upcomingMatches = matches.filter(match => {

            return new Date(match.start) >= new Date();

        });


        // 日付順
        upcomingMatches.sort((a, b) => {

            return new Date(a.start) - new Date(b.start);

        });


        // 直近1試合
        const nextMatch = upcomingMatches[0];


        console.log(team.name);
        console.log(nextMatch);


        if (nextMatch) {

            favoriteMatches.push({
                team: team,
                match: nextMatch
            });

        }

    }

    const weekly = document.getElementById("weekly-matches");

    if (!weekly) return;


    weekly.innerHTML = favoriteMatches.map(item => {

        const match = item.match;

        return `

        <div class="card mb-3">

            <div class="card-body">

                <h5>
                    ⚽ ${item.team.name}
                </h5>

                <div class="d-flex align-items-center">

                    <img 
                        src="${match.home_logo}"
                        width="40"
                        class="me-2"
                    >

                    <span>
                        ${match.home}
                    </span>


                    <span class="mx-2">
                        vs
                    </span>


                    <span>
                        ${match.away}
                    </span>


                    <img 
                        src="${match.away_logo}"
                        width="40"
                        class="ms-2"
                    >

                </div>


                <p>
                    ${translateCompetition(match.competition)}
                </p>


                <small>
                    ${formatDate(match.start)}
                </small>


            </div>

        </div>

    `}).join("");

    const backBtn = document.getElementById("back-favorites-btn");

    if (backBtn) {
        backBtn.style.display = "none";

    }

}

// =========================
// 選択したチームの直近5試合取得
// =========================

async function loadTeamMatches(teamId) {


    const response = await fetch(`/api/team/${teamId}`);

    const matches = await response.json();

    const backBtn =
    document.getElementById("back-favorites-btn");

    const upcomingMatches = matches.filter(match => {

        return new Date(match.start) >= new Date();

    });


    upcomingMatches.sort((a,b)=>{

        return new Date(a.start)-new Date(b.start);

    });

    const nextMatches = upcomingMatches.slice(0,5);

    const weekly = document.getElementById("weekly-matches");

    if (!weekly) return;


    if(nextMatches.length === 0){

        weekly.innerHTML =
        "<p>今後の試合はありません。</p>";

        return;

    }

    if (backBtn) {

        backBtn.style.display = "block";

    }

    weekly.innerHTML = nextMatches.map(match => `

        <div class="card mb-3">

            <div class="card-body">

                <div class="d-flex align-items-center">

                    <img 
                    src="${match.home_logo}"
                    width="40"
                    class="me-2">

                    ${match.home}

                    <span class="mx-2">
                    vs
                    </span>

                    ${match.away}

                    <img 
                    src="${match.away_logo}"
                    width="40"
                    class="ms-2">

                </div>

                <p>
                ${translateCompetition(match.competition)}
                </p>

                <small>
                ${formatDate(match.start)}
                </small>

            </div>

        </div>

    `).join("");

}

// =========================
// 初期化
// =========================
renderFavorites();

loadFavoriteMatches();
