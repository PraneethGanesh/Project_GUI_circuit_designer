// script.js

function submitForm() {
    const input = document.getElementById('input').value;

    fetch("/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ input: input })
    })
    .then(response => response.json())
    .then(data => {
        alert("Result from server: " + data.result);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
