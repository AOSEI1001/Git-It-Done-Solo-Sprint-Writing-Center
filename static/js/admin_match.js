document.addEventListener("DOMContentLoaded", () => {

    const requestContainer = document.getElementById("pending-requests-container");

    fetch("/api/v1/admin-top-matches")
        .then(response => response.json())
        .then(data => {
            data.forEach(request => {
                const requestRow = document.createElement("div");
                requestRow.classList.add("card", "mb-3", "p-2");
                requestRow.requestId = request.request_id;

                // Request details
                const requestContent = document.createElement("div");
                requestContent.classList.add("card-body");
                requestContent.innerHTML = `
                    <h5>${request.courseName} - ${request.professorName}</h5>
                    <p>${request.details}</p>
                `;

                // Only display top match
                const topTutor = request.suggestedTutors[0];
                const topTutorDiv = document.createElement("div");
                topTutorDiv.classList.add("top-tutor", "mb-2");
                if (topTutor) {
                    topTutorDiv.innerHTML = `
                        <strong>Top Match:</strong> ${topTutor.tutorName} (Score: ${topTutor.score})<br>
                        Reasons: ${topTutor.reason}
                    `;
                } else {
                    topTutorDiv.innerHTML = `<em>No matches found</em>`;
                }

                // Confirm button
                const confirmBtn = document.createElement("button");
                confirmBtn.classList.add("btn", "btn-success", "mt-2");
                confirmBtn.innerText = "Confirm Assignment";

                confirmBtn.addEventListener("click", () => {
                    if (!topTutor) return alert("No tutor to assign!");
                    fetch("/assign-tutor", {
                        method: "POST",
                        headers: { "Content-Type": "application/x-www-form-urlencoded" },
                        body: `request_id=${request.request_id}&tutor_id=${topTutor.tutor_id}`
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message || "Tutor assigned successfully!");
                        requestRow.querySelector(".card-body").insertAdjacentHTML(
                            "beforeend",
                            `<p class="text-success mt-2"><strong>Assigned to:</strong> ${topTutor.tutor_name}</p>`
                        );
                        confirmBtn.disabled = true;
                    });
                });

                requestRow.append(requestContent, topTutorDiv, confirmBtn);
                requestContainer.appendChild(requestRow);
            });
        });
});
