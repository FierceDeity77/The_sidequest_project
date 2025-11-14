/*!
* Start Bootstrap - Blog Home v5.0.9 (https://startbootstrap.com/template/blog-home)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-home/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


// for AJAX adding game
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("addGameForm");

  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault(); // stop normal submit

      const url = form.getAttribute("action");
      const formData = new FormData(form);

      try {
        const response = await fetch(url, {
          method: "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest" // let Django know it's AJAX
          }
        });

        if (!response.ok) {
          throw new Error("Network error");
        }

        const data = await response.json();

        if (data.success) {
          // Close modal
          const modalEl = document.getElementById("addGameModal");
          const modal = bootstrap.Modal.getInstance(modalEl);
          modal.hide();

          // Optionally append new game to list
          const gameList = document.querySelector(".game-list-section ol");
          if (gameList) {
            gameList.insertAdjacentHTML("beforeend", data.new_game_html);
          }

          form.reset(); // clear form
        } else {
          // Show errors (basic example)
          alert("There were errors. Please check your form.");
        }

      } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
      }
    });
  }
});


// AJAX for follow/joining games and communities
document.querySelectorAll(".follow-btn").forEach(btn => {
  btn.addEventListener("click", function (e) {
    e.preventDefault(); // stop form submission if inside <form>

    const followId = this.dataset.id;
    const csrfToken = this.dataset.csrf;

    fetch(`/follow/${this.dataset.model}/${this.dataset.id}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `action=${this.dataset.action}`
    })
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.json();
    })
    .then(data => {
      // update follower count separately
      document.getElementById(`followers-${followId}`).innerText = data.member_count;

      // toggle button text
      this.innerText = data.is_following ? "Unfollow" : "Follow";
    })
    .catch(err => console.error("Follow failed:", err));
  });
});

// news feed cards 
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.topic-card').forEach(card => {
    card.addEventListener('click', (e) => {
      const tag = e.target.tagName.toLowerCase();

      // prevent click on links, buttons, icons inside the vote/comment/share section
      if (
        tag === 'a' || 
        tag === 'button' || 
        e.target.closest('.vote-btn') // optional: wrapper div for your vote buttons
      ) {
        e.stopPropagation();
        return;
      }

      // go to topic detail
      window.location.href = card.dataset.url;
    });
  });
});











