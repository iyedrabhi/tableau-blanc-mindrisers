/**
 * WebSocket Notification Client
 * Connects to Django Channels WebSocket and displays real-time notifications
 */

(function () {
  "use strict";

  // Establish WebSocket connection
  function initWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = protocol + "//" + window.location.host + "/ws/notifications/";

    const socket = new WebSocket(wsUrl);

    socket.onopen = function (e) {
      console.log("[WebSocket] Connection established");
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      console.log("[WebSocket] Received:", data);
      displayNotification(data);
    };

    socket.onerror = function (error) {
      console.error("[WebSocket] Error:", error);
    };

    socket.onclose = function (e) {
      console.log("[WebSocket] Connection closed");
      // Optionally attempt to reconnect after delay
      setTimeout(initWebSocket, 5000);
    };

    return socket;
  }

  // Display notification in the UI
  function displayNotification(data) {
    const title = data.title || "Notification";
    const message = data.message || "";
    const type = data.type || "info";

    const notificationBox = createNotificationElement(title, message, type);
    document.body.appendChild(notificationBox);

    // Auto-dismiss after 5 seconds
    setTimeout(function () {
      notificationBox.classList.add("fade-out");
      setTimeout(function () {
        notificationBox.remove();
      }, 300);
    }, 5000);
  }

  // Create notification DOM element
  function createNotificationElement(title, message, type) {
    const div = document.createElement("div");
    div.className = "notification-toast notification-" + (type || "info");

    const closeBtn = document.createElement("button");
    closeBtn.className = "notification-close";
    closeBtn.innerHTML = "&times;";
    closeBtn.onclick = function () {
      div.classList.add("fade-out");
      setTimeout(function () {
        div.remove();
      }, 300);
    };

    const titleEl = document.createElement("div");
    titleEl.className = "notification-title";
    titleEl.textContent = title;

    const msgEl = document.createElement("div");
    msgEl.className = "notification-message";
    msgEl.textContent = message;

    div.appendChild(closeBtn);
    div.appendChild(titleEl);
    div.appendChild(msgEl);

    return div;
  }

  // Do NOT attempt to auto-start a WebSocket here — websocket support is
  // handled centrally in `websocket-notifications.js` which now prefers
  // a polling fallback when ASGI/Daphne is not available. To avoid
  // duplicate WebSocket attempts (which caused repeated 404s), we expose
  // the display function globally and do not automatically connect.
  window.displayNotification = displayNotification;
  window.createNotificationElement = createNotificationElement;
  console.log(
    "[notifications.js] Auto WebSocket disabled; use displayNotification(data) to show a notification"
  );
})();
