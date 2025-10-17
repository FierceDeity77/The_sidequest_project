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
