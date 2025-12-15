document.addEventListener("DOMContentLoaded", () => {

  document.getElementById("createRequestForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Failed to create request");
      }

      const data = await response.json();

      // Render card from SERVER response
      const template = document.getElementById("request_card_temp");
      const card = template.content.cloneNode(true);

      card.querySelector(".card_title").textContent = data.courseName;
      card.querySelector(".card_prof").textContent = data.facultyName;

      document.getElementById("request_grid").prepend(card);

      form.reset();
      // dismiss modal after success
      const modalEl = document.getElementById("createRequestModal");
      const modal = bootstrap.Modal.getInstance(modalEl);
      modal.hide();

    } catch (err) {
      console.error(err);
      alert("Something went wrong. Please try again.");
    }
  });
});
