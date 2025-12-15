document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const formEl = document.getElementById("createRequestForm");
    if (!formEl) {
        console.error("Create Request Form not found!");
        return;
    }

    formEl.addEventListener("submit", async function(e) {
        e.preventDefault();
        console.log("Form submit intercepted");

        const form = e.target;
        const formData = new FormData(form);
        console.log("FormData prepared:", formData);

        try {
            console.log("Sending fetch POST request to:", form.action);
            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });

            console.log("Fetch completed with status:", response.status);

            if (!response.ok) {
                console.error("Response not OK:", response.status, response.statusText);
                throw new Error("Failed to create request");
            }

            const data = await response.json();
            console.log("Server response JSON:", data);

            // Render card from SERVER response
            const template = document.getElementById("request_card_temp");
            if (!template) {
                console.error("Card template not found!");
                return;
            }

            const card = template.content.cloneNode(true);
            console.log("Card template cloned");

            const titleEl = card.querySelector(".card_title");
            const profEl = card.querySelector(".card_prof");

            if (!titleEl || !profEl) {
                console.error("Card elements not found in template!");
            } else {
                titleEl.textContent = data.courseName;
                profEl.textContent = data.facultyName;
                console.log("Card populated with server data");
            }

            const grid = document.getElementById("request_grid");
            if (!grid) {
                console.error("Request grid not found!");
            } else {
                grid.prepend(card);
                console.log("Card added to request grid");
            }

            form.reset();
            console.log("Form reset");

            // dismiss modal after success
            const modalEl = document.getElementById("createRequestModal");
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) {
                    modal.hide();
                    console.log("Modal hidden");
                } else {
                    console.warn("Bootstrap modal instance not found");
                }
            } else {
                console.warn("Modal element not found");
            }

        } catch (err) {
            console.error("Error in form submission:", err);
            alert("Something went wrong. Please try again.");
        }
    });

    async function fetchMatches(requestId, card) {
        console.log("Fetching matches for requestId:", requestId);
        try {
            const response = await fetch(`/admin/match/${requestId}`);
            console.log("Fetch matches response status:", response.status);

            if (!response.ok) throw new Error("Failed to fetch matches");

            const matches = await response.json();
            console.log("Matches received:", matches);

            const container = card.querySelector(".match_results");
            if (!container) console.warn("Match container not found in card");

            renderMatches(matches, container);
        } catch (err) {
            console.error("Error generating matches:", err);
            alert("Error generating matches");
        }
    }

    function renderMatches(matches, container) {
        if (!container) return;

        container.innerHTML = "";
        matches.forEach(match => {
            const div = document.createElement("div");
            div.classList.add("card", "mb-2", "p-2", "shadow-sm");
            div.innerHTML = `<strong>${match.tutorName}</strong> — Match Score: ${match.score}%`;
            container.appendChild(div);
        });
        console.log("Matches rendered in container");
    }

    document.querySelectorAll(".generate_match_btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const requestId = e.target.dataset.requestId;
            const card = e.target.closest(".request_card");
            console.log("Generate match clicked for requestId:", requestId, "on card:", card);
            fetchMatches(requestId, card);
        });
    });
});
