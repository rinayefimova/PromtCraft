let currentLevel = 1;

function loadLevel(level) {
    fetch(`/level/${level}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("level-title").innerText = `Level ${data.level}`;
            document.getElementById("room").innerText = data.room;
            document.getElementById("goal").innerText = data.goal;
            document.getElementById("guardian").innerText = data.guardian;
            document.getElementById("response").innerText = "";
            document.getElementById("promptInput").value = "";
            document.getElementById("nextButton").style.display = "none";
        });
}
function sendPrompt() {

    let prompt = document.getElementById("promptInput").value;

    fetch("/command", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: prompt,
            level: currentLevel})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.response;

        if (data.success) {
            if (data.game_complete) {
                document.getElementById("nextButton").style.display = "none";
                document.getElementById("response").innerText += " Game complete!";
            } else {
                document.getElementById("nextButton").style.display = "inline-block";
            }
        }
    });

}

function nextLevel() {
    currentLevel += 1;
    loadLevel(currentLevel);
}

function restartGame() {
    currentLevel = 1;
    loadLevel(currentLevel);
}

window.onload = function () {
    loadLevel(currentLevel);
};