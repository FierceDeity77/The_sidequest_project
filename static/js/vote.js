
// AJAX for post Voting
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
