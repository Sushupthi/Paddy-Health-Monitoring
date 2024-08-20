document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = new FormData(this);

  fetch("/analyze", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("health-status").innerText = data.health_status;

      const outputImages = document.getElementById("output-images");
      outputImages.innerHTML = "";
      for (const [name, url] of Object.entries(data.images)) {
        const img = document.createElement("img");
        img.src = url;
        img.alt = name;
        outputImages.appendChild(img);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
