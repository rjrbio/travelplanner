let sessionId = null;

// Crear sesión automáticamente al cargar
async function startSession() {
    try {
        const res = await fetch("/session/create", { method: "POST" });

        if (!res.ok) {
            appendMessage("bot", "No se pudo crear la sesión. Intenta más tarde.");
            return;
        }

        const data = await res.json();
        sessionId = data.session_id;

    } catch (err) {
        appendMessage("bot", "Error de conexión al iniciar sesión.");
    }
}

async function sendMessage() {
    const input = document.getElementById("input");
    const msg = input.value.trim();
    if (!msg) return;

    appendMessage("user", msg);

    // Si no hay sesión, intenta crear una nueva
    if (!sessionId) {
        await startSession();
        if (!sessionId) {
            appendMessage("bot", "No se pudo iniciar sesión. Intenta nuevamente.");
            return;
        }
    }

    try {
        const res = await fetch(`/chat/${sessionId}`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg})
        });

        // Error HTTP (500, 404, etc.)
        if (!res.ok) {
            appendMessage("bot", "Hubo un problema en el servidor. Intenta más tarde.");
            return;
        }

        // Intentar parsear JSON
        let data;
        try {
            data = await res.json();
        } catch {
            appendMessage("bot", "Respuesta inválida del servidor.");
            return;
        }

        // Validar estructura
        if (!data.response) {
            appendMessage("bot", "El servidor no envió una respuesta válida.");
            return;
        }

        appendMessage("bot", data.response);

    } catch (err) {
        // Error de red (servidor caído, sin internet, CORS, etc.)
        appendMessage("bot", "No se pudo conectar con el servidor.");
    }

    input.value = "";
}

function appendMessage(role, text) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = role === "user" ? "msg user-msg" : "msg bot-msg";
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

async function endSession() {
    if (!sessionId) {
        appendMessage("bot", "No hay sesión activa.");
        return;
    }

    try {
        await fetch(`/session/${sessionId}/reset`, { method: "POST" });
    } catch {
        appendMessage("bot", "No se pudo finalizar la sesión.");
        return;
    }

    const messages = document.getElementById("messages");
    messages.innerHTML = "";

    appendMessage("bot", "La sesión ha sido finalizada. Puedes empezar una nueva conversación.");

    await startSession();
}

document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("end-session").addEventListener("click", endSession);

startSession();
