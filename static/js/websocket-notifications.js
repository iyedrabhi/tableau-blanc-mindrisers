/**
 * WebSocket Notifications
 * Écoute les notifications en temps réel via WebSocket et les affiche en toast
 * Chaque onglet/fenêtre a sa PROPRE connexion WebSocket indépendante
 */

(function () {
  "use strict";

  // Génère un ID unique pour cette fenêtre/onglet
  const windowId = Math.random().toString(36).substr(2, 9);
  console.log("[WS] Window ID:", windowId);

  // Détecte si l'utilisateur est connecté
  const isAuthenticated =
    document.documentElement.dataset.authenticated === "true" ||
    (typeof window.isAuthenticated !== "undefined" && window.isAuthenticated);

  // Si l'utilisateur n'est pas connecté, ne pas connecter le WebSocket
  if (!isAuthenticated) {
    console.log("[WS] User not authenticated, WebSocket notification disabled");
    return;
  }

  // Détermine le protocole WebSocket (ws ou wss)
  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${wsProtocol}//${window.location.host}/ws/notifications/`;

  console.log("[WS] Connecting to:", wsUrl, "Window:", windowId);

  let notificationSocket = null;
  let reconnectAttempts = 0;
  const maxReconnectAttempts = 5;
  const reconnectDelay = 3000; // 3 secondes
  // Polling fallback (for environments without Daphne/ASGI)
  let pollingIntervalId = null;
  const pollingIntervalMs = 5000; // 5 seconds
  let lastSeenTimestamp = 0; // ms since epoch

  /**
   * Établit la connexion WebSocket
   */
  function connectWebSocket() {
    try {
      notificationSocket = new WebSocket(wsUrl);

      notificationSocket.onopen = function (e) {
        console.log("[WS] Connection established - Window:", windowId);
        reconnectAttempts = 0; // Reset counter on success
        // Stop polling if it was running
        stopPolling();
        toastr.info("Connecté aux notifications en temps réel", "Statut", {
          timeOut: 3000,
          extendedTimeOut: 1000,
        });
      };

      notificationSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log("[WS] Message received - Window:", windowId, data);

        const title = data.title || "Notification";
        const message = data.message || "";
        const type = data.type || "info"; // 'client', 'manager', 'info'

        // Détermine le type de toast basé sur notification_type
        let toastType = "info";
        if (type === "client" || type === "reservation") {
          toastType = "success";
        } else if (type === "manager" || type === "admin") {
          toastType = "warning";
        } else if (type === "error" || type === "cancel") {
          toastType = "error";
        }

        // Affiche le toast avec durée PLUS LONGUE pour mieux voir
        toastr[toastType](message, title, {
          closeButton: true,
          progressBar: true,
          timeOut: 12000,
          extendedTimeOut: 4000,
          positionClass: "toast-top-right",
          newestOnTop: true,
          showDuration: 500,
          hideDuration: 1500,
          onclick: function () {
            // Redirige vers la page notifications si clic
            window.location.href = "/reservations/notifications/";
          },
        });

        // Joue un son de notification
        playNotificationSound();

        // Ajoute la notification au DOM en temps réel si une zone existe
        addNotificationToDOM(title, message, type);
      };

      notificationSocket.onerror = function (error) {
        console.error("[WS] WebSocket error:", error, "Window:", windowId);
        toastr.error("Erreur de connexion aux notifications", "Erreur", {
          timeOut: 4000,
        });
        // Start polling as a fallback
        startPolling();
      };

      notificationSocket.onclose = function (e) {
        console.log("[WS] Connection closed - Window:", windowId);

        // Tentative de reconnexion avec backoff
        if (reconnectAttempts < maxReconnectAttempts) {
          reconnectAttempts++;
          const delay = reconnectDelay * reconnectAttempts;
          console.log(
            `[WS] Reconnecting in ${delay}ms (attempt ${reconnectAttempts}/${maxReconnectAttempts})`
          );

          setTimeout(function () {
            console.log("[WS] Attempting reconnection...");
            connectWebSocket();
          }, delay);
        } else {
          console.error("[WS] Max reconnection attempts reached");
          toastr.error(
            "Connexion perdue. Rechargez la page pour reconnecter.",
            "Déconnecté",
            {
              timeOut: 0,
              extendedTimeOut: 0,
              closeButton: true,
            }
          );
          // If we can't reconnect, start polling
          startPolling();
        }
      };
    } catch (err) {
      console.error("[WS] Error creating WebSocket:", err);
    }
  }

  /**
   * Start polling the server for new notifications as a WebSocket fallback.
   */
  function startPolling() {
    if (pollingIntervalId) return; // already polling
    console.log(
      "[POLL] Starting notifications polling every",
      pollingIntervalMs,
      "ms"
    );
    // Immediately poll once
    pollOnce();
    pollingIntervalId = setInterval(pollOnce, pollingIntervalMs);
  }

  function stopPolling() {
    if (!pollingIntervalId) return;
    clearInterval(pollingIntervalId);
    pollingIntervalId = null;
    console.log("[POLL] Stopped polling");
  }

  function pollOnce() {
    try {
      const url = `/reservations/api/notifications/poll/?since=${lastSeenTimestamp}`;
      fetch(url, { credentials: "same-origin" })
        .then((res) => res.json())
        .then((data) => {
          if (!data || !data.notifications) return;
          // notifications are returned newest-first; show oldest-first
          const notifications = data.notifications.slice().reverse();
          notifications.forEach((n) => {
            // update lastSeenTimestamp
            if (n.ts && n.ts > lastSeenTimestamp) lastSeenTimestamp = n.ts;

            const title = n.title || "Notification";
            const message = n.message || "";
            const type = n.type || "info";

            // Decide toast type
            let toastType = "info";
            if (type === "client" || type === "reservation") {
              toastType = "success";
            } else if (type === "manager" || type === "admin") {
              toastType = "warning";
            } else if (type === "error" || type === "cancel") {
              toastType = "error";
            }

            toastr[toastType](message, title, {
              closeButton: true,
              progressBar: true,
              timeOut: 12000,
              extendedTimeOut: 4000,
              positionClass: "toast-top-right",
              newestOnTop: true,
              showDuration: 500,
              hideDuration: 1500,
              onclick: function () {
                window.location.href = "/reservations/notifications/";
              },
            });

            playNotificationSound();
            addNotificationToDOM(title, message, type);
          });
        })
        .catch((err) => {
          console.error("[POLL] Error polling notifications:", err);
        });
    } catch (e) {
      console.error("[POLL] Exception while polling:", e);
    }
  }

  /**
   * Joue un son de notification (optionnel)
   */
  function playNotificationSound() {
    try {
      const audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gain = audioContext.createGain();

      oscillator.connect(gain);
      gain.connect(audioContext.destination);

      oscillator.frequency.value = 800;
      oscillator.type = "sine";

      gain.gain.setValueAtTime(0.3, audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(
        0.01,
        audioContext.currentTime + 0.1
      );

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
      console.log("[WS] Could not play notification sound:", e);
    }
  }

  /**
   * Ajoute la notification au DOM si élément notifications existe
   */
  function addNotificationToDOM(title, message, type) {
    const notifContainer = document.getElementById("notifications-list");
    if (!notifContainer) return;

    const now = new Date();
    const timeString = now.toLocaleTimeString("fr-FR");

    const notifElement = document.createElement("li");
    notifElement.className = `notification-item notification-${type}`;
    notifElement.innerHTML = `
            <div class="notification-content">
                <strong>${title}</strong>
                <p>${message}</p>
                <small>${timeString}</small>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">✕</button>
        `;
    notifElement.style.animation = "slideInLeft 0.3s ease-out";

    // Ajoute au début de la liste
    notifContainer.insertBefore(notifElement, notifContainer.firstChild);

    // Limite à 10 notifications affichées
    while (notifContainer.children.length > 10) {
      notifContainer.removeChild(notifContainer.lastChild);
    }
  }

  // Établit la première connexion.
  // Forcer l'utilisation du fallback polling sous runserver (pas d'ASGI/Daphne).
  // On n'essaie plus d'ouvrir immédiatement une connexion WebSocket pour éviter
  // les 404 répétées lorsqu'ASGI/Daphne n'est pas lancé.
  console.log("[POLL] WebSocket attempt disabled; using polling fallback");
  startPolling();

  // Export pour utilisation globale
  window.notificationSocket = notificationSocket;
  window.reconnectWebSocket = connectWebSocket;
})();
