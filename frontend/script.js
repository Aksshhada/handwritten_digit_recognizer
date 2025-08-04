const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");


ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);



let drawing = false;

// Start drawing when mouse is pressed
canvas.addEventListener("mousedown", () => {
  drawing = true;
  ctx.beginPath(); // Begin a new stroke path
});

// Stop drawing when mouse is released
canvas.addEventListener("mouseup", () => {
  drawing = false;
  ctx.beginPath(); // Reset the stroke path
});

// Draw circle brush on canvas
canvas.addEventListener("mousemove", draw);

// Function to draw on canvas
function draw(e) {
  if (!drawing) return;
  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.arc(e.offsetX, e.offsetY, 10, 0, Math.PI * 2);
  ctx.fill();
}

// Clear the canvas and result text
function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  document.getElementById("result").textContent = "";
}

// Send canvas image to backend for prediction
function predictDigit() {
  const image = canvas.toDataURL("image/png");

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Response from server:", data); // ✅ Debug
      if (data.prediction !== undefined) {
        document.getElementById("result").textContent = `Prediction: ${data.prediction}`;
      } else {
        document.getElementById("result").textContent = `Error: Prediction failed`;
      }
    })
    .catch((err) => {
      console.error("Prediction error:", err);
      document.getElementById("result").textContent = `Error: ${err.message}`;
    });
}