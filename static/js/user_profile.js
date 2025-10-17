document.addEventListener("DOMContentLoaded", function () {
    // Activate saved tab on load
    const hash = window.location.hash;
    if (hash) {
      const tabTrigger = document.querySelector(`a[href="${hash}"]`);
      if (tabTrigger) {
        const tab = new bootstrap.Tab(tabTrigger);
        tab.show();
      }
    }

    // Save tab state when clicked
    const tabLinks = document.querySelectorAll('#profileTabs a[data-bs-toggle="tab"]');
    tabLinks.forEach(link => {
      link.addEventListener('shown.bs.tab', function (e) {
        history.replaceState(null, null, e.target.getAttribute('href'));
      });
    });
  });