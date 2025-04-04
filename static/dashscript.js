document.addEventListener("DOMContentLoaded", function () {
    let score = localStorage.getItem("userScore") || 0;
    const scoreDisplay = document.getElementById("user-score");

    if (scoreDisplay) {
        scoreDisplay.textContent = score;
    }

    setInterval(() => {
        score++;
        localStorage.setItem("userScore", score);
        if (scoreDisplay) {
            scoreDisplay.textContent = score;
        }
    }, 1000);
});
