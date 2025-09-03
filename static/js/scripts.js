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