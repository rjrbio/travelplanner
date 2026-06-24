let sessionId = null;

async function startSession() {
    try {
        const res = await fetch("/session/create", { method: "POST" });
        if (!res.ok) return;
        const data = await res.json();
        sessionId = data.session_id;
    } catch {
        appendMessage("bot", "Error de conexi&oacute;n al iniciar sesi&oacute;n.");
    }
}

function renderMarkdown(text) {
    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
    html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
    html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");
    html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>\n?)+/g, "<ul>$&</ul>");
    html = html.replace(/\n/g, "<br>");
    html = html.replace(/(<br>)+<\/ul>/g, "</ul>");
    html = html.replace(/<\/ul><br>/g, "</ul>");
    html = html.replace(/<br><ul>/g, "<ul>");
    html = html.replace(/(<h[1-3]>)/g, "<br>$1");
    html = html.replace(/<br><br>/g, "<br>");
    html = html.replace(/^<br>/, "");

    return html;
}

function appendMessage(role, text) {
    const container = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = role === "user" ? "msg user-msg" : "msg bot-msg";

    if (role === "bot") {
        div.innerHTML = renderMarkdown(text);
    } else {
        div.textContent = text;
    }

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function removeWelcome() {
    const welcome = document.querySelector(".welcome-message");
    if (welcome) welcome.remove();
}

function showTyping() {
    document.getElementById("typingIndicator").classList.add("active");
}

function hideTyping() {
    document.getElementById("typingIndicator").classList.remove("active");
}

async function sendMessage() {
    const input = document.getElementById("input");
    const msg = input.value.trim();
    if (!msg) return;

    removeWelcome();
    appendMessage("user", msg);
    input.value = "";
    showTyping();

    if (!sessionId) {
        await startSession();
        if (!sessionId) {
            hideTyping();
            appendMessage("bot", "No se pudo iniciar sesi&oacute;n. Intenta nuevamente.");
            return;
        }
    }

    try {
        const res = await fetch(`/chat/${sessionId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg }),
        });

        if (!res.ok) {
            throw new Error("HTTP " + res.status);
        }

        let data;
        try {
            data = await res.json();
        } catch {
            throw new Error("JSON inv&aacute;lido");
        }

        hideTyping();

        if (!data.response) {
            appendMessage("bot", "El servidor no envi&oacute; una respuesta v&aacute;lida.");
            return;
        }

        appendMessage("bot", data.response);
    } catch (err) {
        hideTyping();
        appendMessage("bot",
            "Hubo un problema al conectar con el servidor. " +
            "Verifica que el servidor est&eacute; corriendo e intenta de nuevo."
        );
    }
}

async function endSession() {
    if (sessionId) {
        try {
            await fetch(`/session/${sessionId}/reset`, { method: "POST" });
        } catch {
            // ignore
        }
    }

    const container = document.getElementById("messages");
    container.innerHTML = "";
    sessionId = null;
    hideTyping();
    await startSession();

    const welcome = document.createElement("div");
    welcome.className = "welcome-message";
    welcome.innerHTML =
        '<div class="welcome-icon">&#127758;</div>' +
        '<h2>Sesi&oacute;n reiniciada</h2>' +
        '<p>&iexcl;Listo para un nuevo viaje!</p>';
    container.appendChild(welcome);
}

function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("input");
    const endBtn = document.getElementById("end-session");

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", handleKeyDown);
    endBtn.addEventListener("click", endSession);

    document.querySelectorAll(".chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            const text = chip.getAttribute("data-text");
            input.value = text;
            sendMessage();
        });
    });

    startSession();
});
