function sendPrompt() {

    let prompt = document.getElementById("promptInput").value;

    fetch("/command", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({prompt: prompt})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.response;
    });

}