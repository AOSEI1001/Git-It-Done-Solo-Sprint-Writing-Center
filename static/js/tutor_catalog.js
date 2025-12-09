const tutors = [
  {
    colby_id: 1,
    name: "Maria Lopez",
    experience: "WI101",
    rating: 4.9,
    about_me : "I like teaching",
    image: "/static/images/team-1.jpg"
  },
  {
    colby_id: 2,
    name: "Jordan Kim",
    experience: "WI101",
    rating: 4.7,
    about_me : "I like teaching",
    image: "/static/images/team-1.jpg"
  },
  {
    colby_id: 3,
    name: "Emily Zhang",
    experience: "WI101",
    about_me : "I like teaching",
    rating: 4.8,
    image: "/static/images/team-1.jpg"
  }
];


const grid = document.getElementById("tutor_grid");
const temp = document.getElementById("tutor_card_temp");

grid.innerHTML = "";

tutors.forEach(tutor => {
    const tut = temp.content.cloneNode(true);

    tut.querySelector(".card_title").textContent = tutor.name;
    tut.querySelector(".experience").textContent = tutor.experience;
    tut.querySelector(".about_me").textContent = tutor.about_me;
    tut.querySelector(".rating").textContent = tutor.rating;

    grid.appendChild(tut);

});
