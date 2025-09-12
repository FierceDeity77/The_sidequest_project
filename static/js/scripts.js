/*!
* Start Bootstrap - Blog Home v5.0.9 (https://startbootstrap.com/template/blog-home)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-home/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function toggleReplyForm(commentId) {
    // Close all other reply forms
    const allForms = document.querySelectorAll('.reply-form');
    allForms.forEach(form => {
        if (form.id !== `reply-form-${commentId}`) {
            form.style.display = "none";
        }
    });

    // Toggle the selected form
    const selectedForm = document.getElementById(`reply-form-${commentId}`);
    if (selectedForm.style.display === "none") {
        selectedForm.style.display = "block";
    } else {
        selectedForm.style.display = "none";
    }
}

// for AJAX add game
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
          // ✅ Close modal
          const modalEl = document.getElementById("addGameModal");
          const modal = bootstrap.Modal.getInstance(modalEl);
          modal.hide();

          // ✅ Optionally append new game to list
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


// Avatar Preview Script
document.addEventListener("DOMContentLoaded", function () {
  const fileInputs = document.querySelectorAll('input[type="file"][data-preview-target]');

  fileInputs.forEach(input => {
    const previewId = input.getAttribute("data-preview-target");
    const previewImg = document.getElementById(previewId);

    if (previewImg) {
      input.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = e => {
            previewImg.src = e.target.result;
          };
          reader.readAsDataURL(file);
        } else {
          // Optional: reset to default if no file is selected
          const defaultSrc = previewImg.getAttribute("data-default-src");
          if (defaultSrc) {
            previewImg.src = defaultSrc;
          }
        }
      });
    }
  });
});