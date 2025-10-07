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


// Upload Avatar/Image/Banner Preview Script
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



// AJAX for comment and post Voting
document.querySelectorAll(".vote-btn").forEach(btn => {
  btn.addEventListener("click", function () {
    const voteId = this.dataset.id;
    const action = this.dataset.action;
    const csrfToken = this.dataset.csrf; // read token from HTML

    fetch(`/vote/${this.dataset.model}/${this.dataset.id}/`, { // gets the model and id from data attributes
      method: "POST",
      headers: {
        "X-CSRFToken": this.dataset.csrf,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `action=${this.dataset.action}`
    })
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.json();
    })
    .then(data => {
      document.getElementById(`upvotes-${voteId}`).innerText = data.upvotes;
      document.getElementById(`downvotes-${voteId}`).innerText = data.downvotes;
    })
    .catch(err => console.error("Vote failed:", err));
  });
});


// Toggle active state for vote buttons and ensure only one active at a time
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".vote-btn");
    if (!btn) return;

    const action = btn.dataset.action; // upvote or downvote
    const commentId = btn.dataset.id;

    // Find both buttons for this comment
    const upvoteBtn = document.querySelector(
        `.vote-btn[data-id="${commentId}"][data-action="upvote"]`
    );
    const downvoteBtn = document.querySelector(
        `.vote-btn[data-id="${commentId}"][data-action="downvote"]`
    );

    // Toggle logic
    if (action === "upvote") {
        btn.classList.toggle("upvote-active");
        downvoteBtn.classList.remove("downvote-active"); // disable opposite
    } else if (action === "downvote") {
        btn.classList.toggle("downvote-active");
        upvoteBtn.classList.remove("upvote-active"); // disable opposite
    }
});


// AJAX for follow/joining games and topics
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


// Comment Edit Toggle
document.addEventListener("DOMContentLoaded", () => {
  // Handle Edit button click
  document.querySelectorAll(".edit-comment-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.commentId;
      document.getElementById(`comment-text-${id}`).style.display = "none";
      document.getElementById(`edit-form-${id}`).style.display = "block";
    });
  });

  // Handle Cancel button
  document.querySelectorAll(".cancel-edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.commentId;
      document.getElementById(`comment-text-${id}`).style.display = "block";
      document.getElementById(`edit-form-${id}`).style.display = "none";
    });
  });

// AJAX submit for edit form
  document.querySelectorAll(".edit-comment-form").forEach(form => {
    form.addEventListener("submit", function(e) {
      e.preventDefault();

      const id = this.dataset.commentId;
      const formData = new FormData(this);
      const url = this.getAttribute("action");

      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Update comment text in UI
          const textElem = document.getElementById(`comment-text-${id}`);
          textElem.textContent = data.new_text;

          // Hide form, show text again
          textElem.style.display = "block";
          document.getElementById(`edit-form-${id}`).style.display = "none";
        } else {
          alert(data.error || "Something went wrong");
        }
      })
      .catch(err => {
        console.error("Error:", err);
        alert("Error saving comment");
      });
    });
  });
});


// Show More Comments and Replies
document.addEventListener("DOMContentLoaded", () => {
  // === Comments (top-level) ===
  function setupShowMore(sectionSelector, itemSelector, buttonSelector, initialVisible = 3, loadCount = 3) {
    const section = document.querySelector(sectionSelector);
    if (!section) return;
    const items = section.querySelectorAll(itemSelector);
    const button = document.querySelector(buttonSelector);
    if (!button) return;

    let visibleCount = initialVisible;

    // hide extra items
    items.forEach((item, index) => {
      if (index >= initialVisible) item.classList.add("hidden");
    });

    button.addEventListener("click", () => {
      const hidden = Array.from(items).filter(i => i.classList.contains("hidden"));
      hidden.slice(0, loadCount).forEach(i => i.classList.remove("hidden"));
      visibleCount += loadCount;

      if (visibleCount >= items.length) {
        button.style.display = "none";
      }
    });
  }

  setupShowMore("#comments-section", ".comment-item", "#show-more-comments", 3, 3);


// === Replies (per comment) ===
  document.querySelectorAll(".comment-replies").forEach(replySection => {
    const replies = replySection.querySelectorAll(".reply-item");
    const button = replySection.nextElementSibling; // the "show replies" button we placed

    if (!button) return;

    // show only 2 replies first
    replies.forEach((reply, index) => {
      if (index >= 2) reply.classList.add("hidden");
    });

    button.addEventListener("click", () => {
      const hiddenReplies = replySection.querySelectorAll(".reply-item.hidden");
      hiddenReplies.forEach(r => r.classList.remove("hidden"));
      button.style.display = "none"; // hide button after expanding
    });
  });
});
    
// Helper: get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// AJAX for submitting new comments and replies without page reload
document.addEventListener("submit", function (e) {
    if (e.target.classList.contains("comment-form")) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrftoken   
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                if (data.parent_id) {
                    // Find parent comment
                    const parentEl = document.querySelector(`#comment-${data.parent_id}`);

                    // Find or create replies container
                    let repliesContainer = parentEl.querySelector(".comment-replies");
                    // safe because it's always rendered by template
                    
                    // Insert reply at the bottom
                    //repliesContainer.insertAdjacentHTML("beforeend", data.comment_html);

                    // Insert reply at the top
                    repliesContainer.insertAdjacentHTML("afterbegin", data.comment_html);

                    
                } else {
                    // Top-level comment
                    document.querySelector("#comments-section")
                        .insertAdjacentHTML("afterbegin", data.comment_html);
                }

                // Clear form textarea
                form.querySelector("textarea").value = "";
            } else {
                alert("Error: " + JSON.stringify(data.errors));
            }
        })
        .catch(err => console.error("Error:", err));
    }
});

// close reply form on submit
document.addEventListener("submit", function (e) {
  if (e.target.matches(".comment-form")) {
    const form = e.target;
    const replyFormWrapper = form.closest(".reply-form");

    // Collapse form right away after clicking "Reply"
    if (replyFormWrapper) {
      replyFormWrapper.style.display = "none";
    }
  }
});

// AJAX for deleting comments without page reload
document.addEventListener("submit", async function (e) {
  if (e.target.matches(".delete-comment-form")) {
    e.preventDefault();

    const form = e.target;
    const commentId = form.dataset.commentId;
    const url = form.action;
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

    if (!confirm("Are you sure you want to delete this comment?")) return;

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Smooth fade-out before removing
        const commentElement = form.closest(".comment-item, .reply-item");
        if (commentElement) {
          commentElement.style.transition = "opacity 0.3s ease, transform 0.3s ease";
          commentElement.style.opacity = "0";
          commentElement.style.transform = "translateY(-5px)";
          setTimeout(() => commentElement.remove(), 300);
        }

        console.log("Comment deleted:", data.comment_id);
      } else {
        alert(data.error || "Something went wrong while deleting.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An unexpected error occurred.");
    }
  }
});