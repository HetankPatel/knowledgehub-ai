const uploadButton = document.getElementById("upload-button");
const askButton = document.getElementById("ask-button");

uploadButton.addEventListener("click", function () {
    document.getElementById("upload-message").textContent =
        "Upload functionality is coming in the next step.";
});

askButton.addEventListener("click", function () {
    document.getElementById("answer").textContent =
        "AI question answering is coming in a later step.";
});
