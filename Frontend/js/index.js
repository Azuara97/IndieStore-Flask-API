async function fetchGames() {
    try {
        const response = await fetch("http://127.0.0.1:5000/Store/GetAllStoreGames");

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const games = await response.json();
        const container = document.getElementById("gamesContainer");
        container.innerHTML = "";

        games.forEach(game => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${game.gameName}</td>
                <td>v${game.gameVer}</td>
                <td>${game.genre}</td>
                <td>${game.gameDesc}</td>
                <td class="price">$${game.price.toFixed(2)}</td>
            `;
            container.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("gamesContainer").innerHTML = "<tr><td colspan='5'>Failed to load games.</td></tr>";
    }
}

fetchGames();
