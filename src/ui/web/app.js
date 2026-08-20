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

function getCurrentTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2200);
}

function copyAnswer(rawText, btnElement) {
    const textToCopy = rawText.replace(/\\n/g, '\n');
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            showToast('📋 Copied answer to clipboard!');
            if (btnElement) {
                const original = btnElement.innerText;
                btnElement.innerText = '✅ Copied';
                setTimeout(() => { btnElement.innerText = original; }, 2000);
            }
        }).catch(() => {
            fallbackCopy(textToCopy);
        });
    } else {
        fallbackCopy(textToCopy);
    }
}

function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('📋 Copied answer to clipboard!');
}

function handleChipClick(questionText) {
    const input = document.getElementById('question-input');
    input.value = questionText;
    submitQuestion();
}

function handleChatScroll() {
    const container = document.getElementById('chat-messages');
    const scrollBtn = document.getElementById('scroll-bottom-btn');
    if (!container || !scrollBtn) return;

    const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight;
    if (distanceFromBottom > 80) {
        scrollBtn.style.display = 'block';
    } else {
        scrollBtn.style.display = 'none';
    }
}

function scrollToBottom(force = false) {
    const container = document.getElementById('chat-messages');
    const scrollBtn = document.getElementById('scroll-bottom-btn');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
    if (scrollBtn) {
        scrollBtn.style.display = 'none';
    }
}

async function submitQuestion() {
    if (isSending) return;

    const input = document.getElementById('question-input');
    const question = input.value.trim();
    if (!question) return;

    input.value = '';
    const personasGrid = document.getElementById('personas-container');
    if (personasGrid) {
        personasGrid.classList.add('collapsed');
    }

    const emptyState = document.getElementById('empty-state');
    if (emptyState) {
        emptyState.style.display = 'none';
    }

    // 1. Append User Message
    appendUserBubble(question);
    scrollToBottom();

    // 2. Append Typing Indicator
    const typingBubble = appendTypingIndicator();
    scrollToBottom();

    isSending = true;

    try {
        const response = await fetch(`${API_URL}/eligibility`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        if (typingBubble && typingBubble.parentNode) {
            typingBubble.parentNode.removeChild(typingBubble);
        }

        const json = await response.json();
        if (json.success) {
            appendAiBubble(json.data, question);
        } else {
            appendErrorBubble(`Error: ${json.error || 'Server error occurred'}`);
        }
    } catch (err) {
        if (typingBubble && typingBubble.parentNode) {
            typingBubble.parentNode.removeChild(typingBubble);
        }
        appendErrorBubble(`Connection Error: Could not reach API server at ${API_URL}. Ensure server is running.`);
    } finally {
        isSending = false;
        scrollToBottom();
    }
}

function appendUserBubble(text) {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble user';
    bubble.innerHTML = `
        <div>${escapeHtml(text)}</div>
        <div class="message-timestamp">${getCurrentTimestamp()}</div>
    `;
    messagesContainer.appendChild(bubble);
}

function appendAiBubble(data, originalQuestion) {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ai';

    const safeAnswerText = data.answer_text.replace(/'/g, "\\'").replace(/"/g, '&quot;').replace(/\n/g, '\\n');

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

    const followUpChipsHTML = getFollowUpChipsHTML(originalQuestion);

    bubble.innerHTML = `
        <div class="ai-header-row">
            <span class="ai-header">🤖 Westminster Licensing Guide</span>
            <button class="copy-btn" onclick="copyAnswer('${safeAnswerText}', this)">📋 Copy</button>
        </div>
        <div class="answer-text">${formatAnswerText(data.answer_text)}</div>
        ${sourcesAccordionHTML}
        ${followUpChipsHTML}
        <div class="message-timestamp">${getCurrentTimestamp()}</div>
    `;

    messagesContainer.appendChild(bubble);
}

function getFollowUpChipsHTML(questionText) {
    const lower = questionText.toLowerCase();
    let suggestions = [
        "What information do I need to apply?",
        "How do I renew my business license online?",
        "Where do I check state permit requirements?"
    ];

    if (lower.includes("home") || lower.includes("residential")) {
        suggestions = [
            "What are the rules for home-based businesses?",
            "What information is required to apply?",
            "What happens if I operate without a license?"
        ];
    } else if (lower.includes("landlord") || lower.includes("lease") || lower.includes("rent")) {
        suggestions = [
            "Are commercial landlords required to get a license?",
            "What is the fee for residential landlord licenses?",
            "How do I renew online via HdL portal?"
        ];
    } else if (lower.includes("contractor") || lower.includes("cslb")) {
        suggestions = [
            "Do out-of-city contractors need a license?",
            "What permits are needed for specialty work?",
            "Where do I check state CSLB requirements?"
        ];
    }

    return `
        <div class="followup-container">
            <div class="followup-label">💡 Suggested follow-ups:</div>
            <div class="chips-wrapper">
                ${suggestions.map(q => `<button class="chip-btn" onclick="handleChipClick('${q.replace(/'/g, "\\'")}')">${q}</button>`).join('')}
            </div>
        </div>
    `;
}

function appendErrorBubble(errorText) {
    const messagesContainer = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ai';
    bubble.style.borderColor = '#f87171';
    bubble.innerHTML = `
        <div class="ai-header-row">
            <span class="ai-header" style="color:#f87171;">⚠️ System Error</span>
        </div>
        <div class="answer-text" style="color:#f87171;">${escapeHtml(errorText)}</div>
        <div class="message-timestamp">${getCurrentTimestamp()}</div>
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

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
