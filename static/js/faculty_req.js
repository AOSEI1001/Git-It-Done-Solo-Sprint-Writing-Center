document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("createRequestForm").addEventListener("submit", function(e){
        e.preventDefault();
        // alert("Sumbit Clicked!");

        const request_title = document.getElementById("title").value;
        const prof = document.getElementById("prof_name").value;
        // const email = document.getElementById("prof_email").value;
        // const desc = document.getElementById("course_desc").value;


        if(!request_title || !prof){
            return;
        }

        const template = document.getElementById("request_card_temp");
        const card = template.content.cloneNode(true);


        card.querySelector(".card_title").textContent = request_title;
        card.querySelector(".card_prof").textContent = prof;
        // card.querySelector().textContent = email;
        // card.querySelector().textContent = desc;

        document.getElementById("request_grid").appendChild(card);
        document.getElementById("createRequestForm").reset();

        
    
    });
});

