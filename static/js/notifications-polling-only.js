/*
 Minimal polling-only notifications client
 This file purposely contains NO WebSocket code to avoid any /ws/notifications/ requests.
 It polls the JSON endpoint `/reservations/api/notifications/poll/` every 5s when the user is authenticated.
*/

(function () {
  "use strict";

  const POLL_INTERVAL_MS = 5000;
  let lastSeenTimestamp = 0; // ms since epoch
  let intervalId = null;

  function isAuth() {
    try {
      return !!window.isAuthenticated;
    } catch (e) {
      return false;
    }
  }

  function startPolling() {
    if (!isAuth()) {
      console.log("[POLL-ONLY] User not authenticated — polling disabled");
      return;
    }
    if (intervalId) return;
    console.log(
      "[POLL-ONLY] Starting polling for notifications every",
      POLL_INTERVAL_MS,
      "ms"
    );
    pollOnce();
    intervalId = setInterval(pollOnce, POLL_INTERVAL_MS);
  }

  function stopPolling() {
    if (!intervalId) return;
    clearInterval(intervalId);
    intervalId = null;
    console.log("[POLL-ONLY] Stopped polling");
  }

  function pollOnce() {
    const url = `/reservations/api/notifications/poll/?since=${lastSeenTimestamp}`;
    fetch(url, { credentials: "same-origin" })
      .then((res) => {
        if (!res.ok) {
          // If 401/403, stop polling to avoid spam
          if (res.status === 401 || res.status === 403) {
            console.log(
              "[POLL-ONLY] Not authenticated (status",
              res.status,
              "), stopping polling"
            );
            stopPolling();
          }
          throw new Error("Network response was not ok: " + res.status);
        }
        return res.json();
      })
      .then((data) => {
        if (!data || !data.notifications) return;
        const notifs = data.notifications.slice().reverse();
        notifs.forEach((n) => {
          if (n.ts && n.ts > lastSeenTimestamp) lastSeenTimestamp = n.ts;
          const title = n.title || "Notification";
          const message = n.message || "";
          const type = n.type || "info";

          // Map types to toastr functions
          let toastFn = "info";
          if (type === "client" || type === "reservation") toastFn = "success";
          if (type === "manager" || type === "admin") toastFn = "warning";
          if (type === "error" || type === "cancel") toastFn = "error";

          try {
            if (window.toastr && typeof window.toastr[toastFn] === "function") {
              window.toastr[toastFn](message, title, {
                closeButton: true,
                progressBar: true,
                timeOut: 12000,
                extendedTimeOut: 4000,
                positionClass: "toast-top-right",
                newestOnTop: true,
              });
            }
          } catch (e) {
            console.error("[POLL-ONLY] Error showing toast:", e);
          }
        });
      })
      .catch((err) => {
        console.debug("[POLL-ONLY] Poll error:", err.message || err);
      });
  }

  // Auto-start polling when DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startPolling);
  } else {
    startPolling();
  }

  // Export for debugging
  window.notificationsPolling = {
    start: startPolling,
    stop: stopPolling,
    lastSeen: () => lastSeenTimestamp,
  };
})();
