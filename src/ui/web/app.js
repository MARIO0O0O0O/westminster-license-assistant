const API_URL = window.WBLEPA_API_URL || "https://westminster-license-assistant.onrender.com";

let isSending = false;

function switchTab(tabName, event) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    if (event && event.target) {
        event.target.classList.add('active');
    }
    document.getElementById(`tab-${tabName}`).classList.add('active');

    if (tabName === 'checklist') {
        fetchChecklist();
    } else if (tabName === 'sources') {
        fetchSources();
    }
}

function selectPersona(personaKey) {
    switchTab('assistant');
    const input = document.getElementById('question-input');

    if (personaKey === 'home-business') {
        input.value = "I run a business from my home in Westminster, what permits do I need?";
    } else if (personaKey === 'landlord') {
        input.value = "Do I need a business license if I lease out residential property I own?";
    } else if (personaKey === 'contractor') {
        input.value = "I am a contractor working in Westminster but based elsewhere, do I need a license?";
    }
    submitQuestion();
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitQuestion();
    }
}

async function submitQuestion() {
    if (isSending) return;

    const input = document.getElementById('question-input');
    const question = input.value.trim();
    if (!question) return;

    // Clear input & collapse category cards on first query
    input.value = '';
    const personasGrid = document.getElementById('personas-container');
    if (personasGrid) {
        personasGrid.classList.add('collapsed');
    }

    // Hide empty state if present
    const emptyState = document.getElementById('empty-state');
    if (emptyState) {
        emptyState.style.display = 'none';
    }

    const messagesContainer = document.getElementById('chat-messages');

    // 1. Append User Message Bubble
    appendUserBubble(question);
    scrollToBottom();

    // 2. Show Animated Typing Indicator Bubble
    const typingBubble = appendTypingIndicator();
    scrollToBottom();

    isSending = true;

    try {
        const response = await fetch(`${API_URL}/eligibility`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        // Remove typing indicator
        if (typingBubble && typingBubble.parentNode) {
            typingBubble.parentNode.removeChild(typingBubble);
        }

        const json = await response.json();
        if (json.success) {
            appendAiBubble(json.data);
        } else {
            appendErrorBubble(`Error: ${json.error || 'Server error occurred'}`);
        }
    } catch (err) {
        if (typingBubble && typingBubble.parentNode) {
            typingBubble.parentNode.removeChild(typingBubble);
        }
        appendErrorBubble(`Connection Error: Could not reach API server at ${API_URL}. Please ensure the server is running.`);
    } finally {
        isSending = false;
        scrollToBottom();
    }
}

function appendUserBubble(text) {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble user';
    bubble.innerText = text;
    messagesContainer.appendChild(bubble);
}

function appendAiBubble(data) {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ai';

    let sourcesAccordionHTML = '';
    if (data.sources && data.sources.length > 0) {
        const accordionId = `sources-${Date.now()}`;
        sourcesAccordionHTML = `
            <div class="sources-accordion">
                <button class="sources-toggle" onclick="toggleSources('${accordionId}')">
                    <span>🔗 Cited Sources (${data.sources.length})</span> <span id="arrow-${accordionId}">▼</span>
                </button>
                <div id="${accordionId}" class="sources-content">
                    <ul>
                        ${data.sources.map(s => `<li>• <a href="${s.source_url}" target="_blank">${s.section_heading} ↗</a></li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    bubble.innerHTML = `
        <div class="ai-header">🤖 Westminster Licensing Guide</div>
        <div class="answer-text">${formatAnswerText(data.answer_text)}</div>
        ${sourcesAccordionHTML}
    `;

    messagesContainer.appendChild(bubble);
}

function appendErrorBubble(errorText) {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ai';
    bubble.style.borderColor = '#f87171';
    bubble.innerHTML = `
        <div class="ai-header" style="color:#f87171;">⚠️ System Error</div>
        <div class="answer-text" style="color:#f87171;">${errorText}</div>
    `;
    messagesContainer.appendChild(bubble);
}

function appendTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'typing-bubble';
    bubble.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    messagesContainer.appendChild(bubble);
    return bubble;
}

function toggleSources(id) {
    const content = document.getElementById(id);
    const arrow = document.getElementById(`arrow-${id}`);
    if (content) {
        content.classList.toggle('open');
        if (arrow) {
            arrow.innerText = content.classList.contains('open') ? '▲' : '▼';
        }
    }
}

function formatAnswerText(text) {
    return text.replace(/\[(chk_[a-zA-Z0-9_]+)\]/g, '<span style="color:#34d399; font-weight:600; font-size:0.82em; background:rgba(52,211,153,0.15); padding:2px 6px; border-radius:4px;">[$1]</span>');
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

async function fetchChecklist() {
    const topic = document.getElementById('topic-select').value;
    const resultsDiv = document.getElementById('checklist-results');
    resultsDiv.innerHTML = `<div class="loading">Loading checklist items...</div>`;

    try {
        const response = await fetch(`${API_URL}/checklist?topic=${topic}`);
        const json = await response.json();

        if (json.success) {
            const items = json.data.items;
            if (items.length === 0) {
                resultsDiv.innerHTML = `<p style="padding: 20px; color: #94a3b8;">No items found for topic "${topic}".</p>`;
                return;
            }

            resultsDiv.innerHTML = items.map(item => `
                <div class="results-card" style="margin-top: 12px; padding: 18px;">
                    <h3 style="color:#38bdf8; font-size: 1.05rem; margin-bottom: 6px;">
                        <a href="${item.source_url}" target="_blank" style="color:#38bdf8; text-decoration:none;">${item.section_heading} ↗</a>
                    </h3>
                    <p style="font-size: 0.9rem; color: #cbd5e1;">${item.snippet}</p>
                    <span style="font-size: 0.75rem; color: #94a3b8; margin-top: 8px; display:inline-block;">Tags: ${item.topic_tags}</span>
                </div>
            `).join('');
        }
    } catch (err) {
        resultsDiv.innerHTML = `<p style="color:#f87171; padding:20px;">Failed to load checklist from API.</p>`;
    }
}

async function fetchSources() {
    const resultsDiv = document.getElementById('sources-results');
    resultsDiv.innerHTML = `<div class="loading">Loading official source directory...</div>`;

    try {
        const response = await fetch(`${API_URL}/sources`);
        const json = await response.json();

        if (json.success) {
            const sources = json.data.sources;
            resultsDiv.innerHTML = sources.map(s => `
                <div class="results-card" style="margin-top: 12px; padding: 18px;">
                    <h3 style="color:#34d399; font-size: 1.1rem; margin-bottom: 6px;">
                        <a href="${s.url}" target="_blank" style="color:#34d399; text-decoration:none;">${s.title} ↗</a>
                    </h3>
                    <p style="font-size: 0.85rem; color: #94a3b8; word-break: break-all;">URL: ${s.url}</p>
                    <span style="font-size: 0.75rem; color: #60a5fa; margin-top: 8px; display:inline-block;">Tags: ${s.default_tags}</span>
                </div>
            `).join('');
        }
    } catch (err) {
        resultsDiv.innerHTML = `<p style="color:#f87171; padding:20px;">Failed to load source directory from API.</p>`;
    }
}
