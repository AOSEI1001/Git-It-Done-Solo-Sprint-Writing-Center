document.addEventListener("DOMContentLoaded", () => {

    const requestContainer = document.getElementById("requests-container");

    fetch("/api/v1/admin-top-matches")
        .then(response => response.json())
        .then(data => {
            data.forEach(request => {
                const requestRow = document.createElement("div");
                requestRow.classList.add("request-row");
                requestRow.requestId = request.id;

                const requestContent = document.createElement("div");
                requestContent.classList.add("request-content");


                requestContent.innerHTML = `<h5>${request.courseName} - ${request.professorName}</h5>
                <p>${request.details}</p>`;


                const topTutorContainer = document.createElement("div");
                topTutorContainer.classList.add("suggested-tutors");

                request.suggestedTutors.forEach(tutor => {
                    const tutorSelectBtn = document.createElement("button");
                    tutorSelectBtn.classList.add("tutor-select-btn");
                    tutorSelectBtn.innerText = tutor.name;
                    tutorSelectBtn.dataset.tutorId = tutor.id;

                    tutorSelectBtn.addEventListener("click", () => {
                        requestRow.querySelectorAll(".operation-btns").forEach(e => e.remove());

                        const operationDiv = document.createElement("div");
                        operationDiv.classList.add("operation-btns");

                        const confirmBtn = document.createElement("button");
                        confirmBtn.innerText = "Confirm";
                        confirmBtn.classList.add("confirm-btn");

                        confirmBtn.addEventListener("click", () => {
                            fetch("/api/confirm-match", { method: "POST" })
                                .then(response => response.json())
                                .then(data => {
                                    alert(data.message)
                                });
                        });

                        const cancelBtn = document.createElement("button");
                        cancelBtn.innerText = "Cancel";
                        cancelBtn.classList.add("cancel-btn");
                        cancelBtn.addEventListener("click", () => operationDiv.remove());

                        operationDiv.append(confirmBtn, cancelBtn);
                        requestRow.appendChild(operationDiv);

                    });

                    topTutorContainer.appendChild(tutorSelectBtn);
                });


                requestRow.appendChild(requestContent);
                requestRow.appendChild(topTutorContainer);
                requestContainer.appendChild(requestRow);



            });
        });

});