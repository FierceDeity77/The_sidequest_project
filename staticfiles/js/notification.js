document.addEventListener('DOMContentLoaded', function() {
  const notifDropdown = document.getElementById('notifDropdown');
  const notifMenu = notifDropdown.nextElementSibling;
  const notifDot = document.getElementById('notifDot');

  async function loadNotifications() {
    try {
      const response = await fetch(NOTIFICATIONS_URL);
      const data = await response.json();

      // Toggle red dot visibility
      if (data.unread_count > 0) {
        notifDot.classList.remove('d-none');
      } else {
        notifDot.classList.add('d-none');
      }

      notifMenu.innerHTML = '';

      if (data.notifications.length === 0) {
        notifMenu.innerHTML = '<li><span class="dropdown-item-text text-muted">No notifications yet</span></li>';
        return;
      }

      data.notifications.forEach(n => {
        const li = document.createElement('li');
        li.innerHTML = `
          <a class="dropdown-item d-flex justify-content-between align-items-center ${n.is_read ? '' : 'fw-bold'} notif-item"
             href="${n.url || '#'}"
             data-id="${n.id}">
            <span>${n.message}</span>
            <small class="text-muted ms-2">${n.created_at}</small>
          </a>`;
        notifMenu.appendChild(li);
      });

    } catch (error) {
      console.error("Error loading notifications:", error);
    }
  }

  //  When the bell is clicked — load notifications
  notifDropdown.addEventListener('click', loadNotifications);

  //  When a notification item is clicked — mark as read
  notifMenu.addEventListener('click', async function(e) {
    if (e.target.closest('.notif-item')) {
      const item = e.target.closest('.notif-item');
      const notifId = item.getAttribute('data-id');
      const notifUrl = item.getAttribute('href');

      try {
        const response = await fetch(`/notifications/mark-read/${notifId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
        });
        const result = await response.json();
        if (result.success) {
          item.classList.remove('fw-bold'); // visually mark as read
          if (notifUrl && notifUrl !== '#') {
            window.location.href = notifUrl; // go to link
          }
        }
      } catch (error) {
        console.error('Error marking notification as read:', error);
      }
    }
  });

  //  Helper to get CSRF token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});