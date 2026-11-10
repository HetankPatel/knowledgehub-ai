const uploadButton =
    document.getElementById("upload-button");

const askButton =
    document.getElementById("ask-button");


async function displayDocuments() {

    const response =
        await fetch("/api/documents");

    const documents =
        await response.json();

    const documentList =
        document.getElementById("document-list");

    documentList.innerHTML = "";


    if (documents.length === 0) {

        documentList.textContent =
            "No documents uploaded yet.";

        return;
    }


    documents.forEach(function (item) {

        const row =
            document.createElement("div");

        row.className = "document-row";


        const name =
            document.createElement("span");

        name.textContent =
            item.filename;


        const deleteButton =
            document.createElement("button");

        deleteButton.textContent =
            "Delete";


        deleteButton.addEventListener(
            "click",
            async function () {

                await fetch(
                    "/api/documents/" + item.id,
                    {
                        method: "DELETE"
                    }
                );

                displayDocuments();
            }
        );


        row.appendChild(name);

        row.appendChild(deleteButton);

        documentList.appendChild(row);
    });
}


uploadButton.addEventListener(
    "click",
    async function () {

        const fileInput =
            document.getElementById(
                "document-file"
            );

        const message =
            document.getElementById(
                "upload-message"
            );


        if (fileInput.files.length === 0) {

            message.textContent =
                "Please choose a file first.";

            return;
        }


        const formData =
            new FormData();

        formData.append(
            "file",
            fileInput.files[0]
        );


        message.textContent =
            "Uploading...";


        const response =
            await fetch(
                "/api/documents",
                {
                    method: "POST",
                    body: formData
                }
            );


        const result =
            await response.json();


        if (response.ok) {

            message.textContent =
                result.filename +
                " uploaded successfully.";

            fileInput.value = "";

            displayDocuments();

        } else {

            message.textContent =
                result.detail ||
                "Upload failed.";
        }
    }
);


askButton.addEventListener(
    "click",
    async function () {

        const questionInput =
            document.getElementById(
                "question"
            );

        const answerBox =
            document.getElementById(
                "answer"
            );


        const question =
            questionInput.value.trim();


        if (!question) {

            answerBox.textContent =
                "Please enter a question.";

            return;
        }


        answerBox.textContent =
            "Finding an answer...";


        try {

            const response =
                await fetch(
                    "/api/ask",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            question: question
                        })
                    }
                );


            const result =
                await response.json();


            if (!response.ok) {

                answerBox.textContent =
                    result.detail;

                return;
            }


            answerBox.innerHTML = "";


            const answer =
                document.createElement("p");

            answer.textContent =
                "Answer: " + result.answer;


            answerBox.appendChild(answer);


            if (result.source) {

                const source =
                    document.createElement("p");

                source.textContent =
                    "Source: " + result.source;

                answerBox.appendChild(source);
            }


        } catch (error) {

            answerBox.textContent =
                "Something went wrong while answering the question.";
        }
    }
);


displayDocuments();
