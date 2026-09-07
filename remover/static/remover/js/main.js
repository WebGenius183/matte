(function () {
  "use strict";

  const form = document.getElementById("cut-form");
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const idleView = document.getElementById("dropzone-idle");
  const filledView = document.getElementById("dropzone-filled");
  const filenameDisplay = document.getElementById("filename-display");
  const submitBtn = document.getElementById("submit-btn");
  const errorMsg = document.getElementById("error-msg");
  const result = document.getElementById("result");
  const originalImg = document.getElementById("original-img");
  const resultImg = document.getElementById("result-img");
  const resultFrame = document.getElementById("result-frame");
  const downloadLink = document.getElementById("download-link");
  const resetBtn = document.getElementById("reset-btn");

  let selectedFile = null;

  function getCsrfToken() {
    const input = form.querySelector("input[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
  }

  function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.remove("is-hidden");
  }

  function clearError() {
    errorMsg.textContent = "";
    errorMsg.classList.add("is-hidden");
  }

  function setFile(file) {
    if (!file) return;

    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
      showError("This isn't an image Matte can read — try a JPG or PNG.");
      return;
    }

    clearError();
    selectedFile = file;
    filenameDisplay.textContent = file.name;
    idleView.classList.add("is-hidden");
    filledView.classList.remove("is-hidden");
    submitBtn.disabled = false;
  }

  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      fileInput.click();
    }
  });

  fileInput.addEventListener("change", () => {
    setFile(fileInput.files[0]);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add("is-dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.remove("is-dragover");
    });
  });

  dropzone.addEventListener("drop", (event) => {
    const file = event.dataTransfer.files[0];
    setFile(file);
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!selectedFile) return;

    clearError();
    submitBtn.disabled = true;
    submitBtn.classList.add("is-working");
    submitBtn.textContent = "Cutting...";

    const quality = form.querySelector("input[name=quality]:checked").value;
    const body = new FormData();
    body.append("image", selectedFile);
    body.append("quality", quality);

    try {
      const response = await fetch(form.dataset.action || "/cut/", {
        method: "POST",
        headers: { "X-CSRFToken": getCsrfToken() },
        body,
      });
      const data = await response.json();

      if (!response.ok) {
        showError(data.error || "Something went wrong. Try again.");
        return;
      }

      originalImg.src = URL.createObjectURL(selectedFile);
      resultImg.src = data.result;
      downloadLink.href = data.result;

      // Restart the reveal animation for a fresh result.
      resultFrame.classList.remove("checker");
      void resultFrame.offsetWidth;
      resultFrame.classList.add("checker");

      result.classList.remove("is-hidden");
      result.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) {
      showError("Couldn't reach the server. Check your connection and try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.classList.remove("is-working");
      submitBtn.textContent = "Cut it out";
    }
  });

  resetBtn.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";
    filledView.classList.add("is-hidden");
    idleView.classList.remove("is-hidden");
    submitBtn.disabled = true;
    result.classList.add("is-hidden");
    clearError();
  });
})();
