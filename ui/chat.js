(function () {
  'use strict';

  const STATE = {
    sessionId: null,
    history: [],
    theme: localStorage.getItem('tp-theme') || 'light',
    isWaiting: false,
    typingTimer: null,
    typingIndex: 0,
  };

  const TYPING_MESSAGES = [
    'Analizando tu consulta',
    'Buscando opciones de viaje',
    'Consultando destinos',
    'Planificando itinerario',
    'Organizando actividades',
    'Casi listo',
  ];

  const GREETINGS = {
    morning: 'Buenos d\u00edas',
    afternoon: 'Buenas tardes',
    evening: 'Buenas noches',
  };

  /* ─── DOM refs ─── */
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);

  const el = {
    messages: $('#messages'),
    welcome: $('#welcome'),
    input: $('#input'),
    sendBtn: $('#sendBtn'),
    typing: $('#typingIndicator'),
    typingText: $('#typingText'),
    resetBtn: $('#resetBtn'),
    menuToggle: $('#menuToggle'),
    sidebar: $('#sidebar'),
    overlay: $('#overlay'),
    toast: $('#toast'),
    greeting: $('#greeting'),
    currentDest: $('#currentDest'),
    themeToggle: $('#themeToggle'),
    darkModeToggle: $('#darkModeToggle'),
    statusText: $('#statusText'),
    chatView: $('#chatView'),
    historyView: $('#historyView'),
    settingsView: $('#settingsView'),
    historyList: $('#historyList'),
    chips: $('#chips'),
  };

  /* ─── Init ─── */
  function init() {
    setTheme(STATE.theme);
    setGreeting();
    setupSidebarNav();
    setupThemeToggle();
    setupInput();
    setupButtons();
    setupChips();
    startSession();
  }

  /* ─── Greeting ─── */
  function setGreeting() {
    const h = new Date().getHours();
    let key = 'afternoon';
    if (h < 12) key = 'morning';
    else if (h >= 20) key = 'evening';
    el.greeting.textContent = GREETINGS[key];
  }

  /* ─── Theme ─── */
  function setTheme(theme) {
    STATE.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('tp-theme', theme);
    if (el.darkModeToggle) el.darkModeToggle.checked = theme === 'dark';
  }

  function toggleTheme() {
    setTheme(STATE.theme === 'light' ? 'dark' : 'light');
  }

  function setupThemeToggle() {
    el.themeToggle.addEventListener('click', toggleTheme);
    el.darkModeToggle.addEventListener('change', function () {
      setTheme(this.checked ? 'dark' : 'light');
    });
  }

  /* ─── Sidebar Nav ─── */
  function setupSidebarNav() {
    $$('.sidebar__item[data-view]').forEach(function (item) {
      item.addEventListener('click', function () {
        const view = this.dataset.view;
        $$('.sidebar__item').forEach(function (i) { i.classList.remove('sidebar__item--active'); });
        this.classList.add('sidebar__item--active');
        showView(view);
        closeSidebar();
      });
    });

    el.menuToggle.addEventListener('click', toggleSidebar);
    el.overlay.addEventListener('click', closeSidebar);
  }

  function toggleSidebar() { el.sidebar.classList.toggle('open'); el.overlay.classList.toggle('open'); }
  function closeSidebar() { el.sidebar.classList.remove('open'); el.overlay.classList.remove('open'); }

  function showView(view) {
    el.chatView.hidden = view !== 'chat';
    el.historyView.hidden = view !== 'history';
    el.settingsView.hidden = view !== 'settings';
    if (view === 'history') renderHistory();
  }

  /* ─── Session ─── */
  async function startSession() {
    try {
      const res = await fetch('/session/create', { method: 'POST' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      STATE.sessionId = data.session_id;
      el.statusText.textContent = 'Conectado';
    } catch (e) {
      el.statusText.textContent = 'Sin conexi\u00f3n';
    }
  }

  /* ─── Reset ─── */
  async function resetSession() {
    if (STATE.sessionId) {
      try { await fetch('/session/' + STATE.sessionId + '/reset', { method: 'POST' }); } catch (e) { /* ignore */ }
    }
    el.messages.innerHTML = '';
    STATE.history = [];
    STATE.sessionId = null;
    stopTyping();
    el.currentDest.textContent = '';
    await startSession();

    const welcomeHTML =
      '<div class="welcome__globe">' +
      '<svg viewBox="0 0 120 120" width="80" height="80"><circle cx="60" cy="60" r="56" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.15"/>' +
      '<ellipse cx="60" cy="60" rx="56" ry="28" fill="none" stroke="currentColor" stroke-width="1" opacity="0.1"/>' +
      '<ellipse cx="60" cy="60" rx="56" ry="28" fill="none" stroke="currentColor" stroke-width="1" opacity="0.1" transform="rotate(60 60 60)"/>' +
      '<ellipse cx="60" cy="60" rx="56" ry="28" fill="none" stroke="currentColor" stroke-width="1" opacity="0.1" transform="rotate(-60 60 60)"/>' +
      '<circle cx="60" cy="60" r="20" fill="none" stroke="currentColor" stroke-width="1" opacity="0.15"/>' +
      '</svg></div>' +
      '<h1 class="welcome__title">Nueva conversaci\u00f3n</h1>' +
      '<p class="welcome__desc">Cu\u00e9ntame a d\u00f3nde quieres viajar</p>';
    const div = document.createElement('div');
    div.className = 'welcome';
    div.id = 'welcome';
    div.style.animation = 'none';
    div.innerHTML = welcomeHTML;
    el.messages.appendChild(div);
    el.currentDest.textContent = '';
  }

  /* ─── Send ─── */
  async function sendMessage() {
    const text = el.input.value.trim();
    if (!text || STATE.isWaiting) return;

    STATE.isWaiting = true;
    el.sendBtn.disabled = true;
    removeWelcome();
    appendMessage('user', text);
    el.input.value = '';
    el.input.style.height = 'auto';
    startTyping();

    if (!STATE.sessionId) await startSession();

    if (!STATE.sessionId) {
      stopTyping();
      appendMessage('bot', 'No se pudo conectar con el servidor. Verifica que est\u00e9 corriendo.');
      STATE.isWaiting = false;
      el.sendBtn.disabled = false;
      return;
    }

    try {
      const res = await fetch('/chat/' + STATE.sessionId, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!res.ok) throw new Error('HTTP ' + res.status);

      const data = await res.json();
      stopTyping();

      if (!data.response) {
        appendMessage('bot', 'El servidor no devolvi\u00f3 una respuesta v\u00e1lida.');
      } else {
        appendMessage('bot', data.response);
        updateDestFromResponse(text, data.response);
      }
    } catch (err) {
      stopTyping();
      appendMessage('bot', 'Error de conexi\u00f3n. Aseg\u00farate de que el servidor est\u00e9 corriendo en el puerto 8000.');
    }

    STATE.isWaiting = false;
    el.sendBtn.disabled = false;
    el.input.focus();
  }

  /* ─── Extract dest from text ─── */
  function extractDest(text) {
    const match = text.match(/(?:viajar\s+a|visit(?:ar)?\s+|ir\s+a|a\s+)([A-Za-z\u00c0-\u024f]+(?:\s+[A-Za-z\u00c0-\u024f]+)?)/i);
    return match ? match[1].trim() : null;
  }

  function updateDestFromResponse(inputText, responseText) {
    const dest = extractDest(inputText || '');
    if (dest) {
      el.currentDest.textContent = dest.charAt(0).toUpperCase() + dest.slice(1);
    } else {
      const match = responseText.match(/##\s+(.+?)\s*\u2014/);
      if (match) el.currentDest.textContent = match[1].trim();
    }
  }

  /* ─── Append message ─── */
  function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = 'msg msg--' + role;

    if (role === 'bot') {
      div.innerHTML = renderMarkdown(text);
    } else {
      div.textContent = text;
    }

    const time = document.createElement('span');
    time.className = 'msg__time';
    time.textContent = formatTime(new Date());
    div.appendChild(time);

    el.messages.appendChild(div);
    el.messages.scrollTop = el.messages.scrollHeight;

    STATE.history.push({ role: role, text: text, time: Date.now() });
  }

  /* ─── Markdown render ─── */
  function renderMarkdown(text) {
    var html = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>');

    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>[\s\S]*?<\/li>(\s*<li>[\s\S]*?<\/li>)*)/g, function (m) {
      return '<ul>' + m + '</ul>';
    });

    html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>[\s\S]*?<\/li>(\s*<li>[\s\S]*?<\/li>)*)/g, function (m) {
      return '<ol>' + m + '</ol>';
    });

    html = html.replace(/D\u00eda \d+/g, function (m) {
      return '<br><strong>' + m + '</strong>';
    });

    html = html.replace(/\n/g, '<br>');
    html = html.replace(/(<br>)+<\/ul>/g, '</ul>');
    html = html.replace(/(<br>)+<\/ol>/g, '</ol>');
    html = html.replace(/<\/ul><br>/g, '</ul>');
    html = html.replace(/<\/ol><br>/g, '</ol>');
    html = html.replace(/<br><ul>/g, '<ul>');
    html = html.replace(/<br><ol>/g, '<ol>');
    html = html.replace(/<br>(<h[1-3]>)/g, '$1');
    html = html.replace(/(<h[1-3]>)/g, '<br>$1');
    html = html.replace(/<br><br>/g, '<br>');
    html = html.replace(/^<br>/, '');
    html = html.replace(/<br>$/, '');

    return html;
  }

  /* ─── Time formatting ─── */
  function formatTime(date) {
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
  }

  function formatDate(date) {
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
  }

  /* ─── Typing ─── */
  function startTyping() {
    STATE.typingIndex = 0;
    el.typing.classList.add('active');
    el.typingText.textContent = TYPING_MESSAGES[0] + '...';
    STATE.typingTimer = setInterval(function () {
      STATE.typingIndex = (STATE.typingIndex + 1) % TYPING_MESSAGES.length;
      el.typingText.textContent = TYPING_MESSAGES[STATE.typingIndex] + '...';
    }, 2500);
  }

  function stopTyping() {
    el.typing.classList.remove('active');
    if (STATE.typingTimer) {
      clearInterval(STATE.typingTimer);
      STATE.typingTimer = null;
    }
  }

  /* ─── Welcome ─── */
  function removeWelcome() {
    if (el.welcome) {
      el.welcome.remove();
      el.welcome = null;
    }
  }

  /* ─── Input ─── */
  function setupInput() {
    el.input.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 100) + 'px';
      el.sendBtn.disabled = this.value.trim().length === 0 || STATE.isWaiting;
    });

    el.input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    el.sendBtn.addEventListener('click', sendMessage);
  }

  /* ─── Buttons ─── */
  function setupButtons() {
    el.resetBtn.addEventListener('click', resetSession);
  }

  /* ─── Chips ─── */
  function setupChips() {
    el.chips.addEventListener('click', function (e) {
      var chip = e.target.closest('.chip');
      if (!chip) return;
      var text = chip.getAttribute('data-text');
      if (text) {
        el.input.value = text;
        sendMessage();
      }
    });
  }

  /* ─── History ─── */
  function renderHistory() {
    el.historyList.innerHTML = '';
    if (STATE.history.length === 0) {
      el.historyList.innerHTML = '<div class="history__empty">' +
        '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3">' +
        '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' +
        '<p>A\u00fan no hay mensajes en esta sesi\u00f3n</p></div>';
      return;
    }

    var firstUserMsg = STATE.history.find(function (m) { return m.role === 'user'; });
    if (!firstUserMsg) return;

    var div = document.createElement('div');
    div.className = 'history__item';
    div.innerHTML =
      '<span class="history__item-icon">' +
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' +
      '</span>' +
      '<div class="history__item-info">' +
      '<div class="history__item-title">' + firstUserMsg.text.slice(0, 60) + (firstUserMsg.text.length > 60 ? '...' : '') + '</div>' +
      '<div class="history__item-meta">' + formatDate(new Date(firstUserMsg.time)) + ' &middot; ' + STATE.history.length + ' mensajes</div>' +
      '</div>';
    el.historyList.appendChild(div);
  }

  /* ─── Toast ─── */
  function showToast(msg) {
    el.toast.textContent = msg;
    el.toast.classList.add('show');
    setTimeout(function () { el.toast.classList.remove('show'); }, 2500);
  }

  /* ─── Boot ─── */
  document.addEventListener('DOMContentLoaded', init);

})();
