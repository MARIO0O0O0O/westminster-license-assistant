const API_URL = window.WBLEPA_API_URL || "https://westminster-license-assistant.onrender.com";

function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    event.target.classList.add('active');
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

async function submitQuestion() {
    const input = document.getElementById('question-input');
    const question = input.value.trim();
    if (!question) return;

    const resultsDiv = document.getElementById('assistant-results');
    resultsDiv.style.display = 'block';
    resultsDiv.innerHTML = `<div class="loading">⏳ Querying Westminster AI Assistant...</div>`;

    try {
        const response = await fetch(`${API_URL}/eligibility`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const json = await response.json();
        if (json.success) {
            const data = json.data;
            let sourcesHTML = '';
            if (data.sources && data.sources.length > 0) {
                sourcesHTML = `
                    <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;">
                        <h4 style="color:#60a5fa; margin-bottom: 8px;">🔗 Cited Official Sources:</h4>
                        <ul class="sources-list">
                            ${data.sources.map(s => `<li>• <a href="${s.source_url}" target="_blank">${s.section_heading}</a></li>`).join('')}
                        </ul>
                    </div>
                `;
            }

            resultsDiv.innerHTML = `
                <div class="results-card">
                    <h2>${data.in_scope ? '📋 Guidance Output' : '⚠️ Scope Notice'}</h2>
                    <div class="answer-body">${formatAnswerText(data.answer_text)}</div>
                    ${sourcesHTML}
                </div>
            `;
        } else {
            resultsDiv.innerHTML = `<div class="results-card" style="border-color:#f87171;"><p style="color:#f87171;">Error: ${json.error}</p></div>`;
        }
    } catch (err) {
        resultsDiv.innerHTML = `<div class="results-card" style="border-color:#f87171;"><p style="color:#f87171;">Connection Error: Could not connect to API server at ${API_URL}. Ensure backend API server is running.</p></div>`;
    }
}

function formatAnswerText(text) {
    return text.replace(/\[(chk_[a-zA-Z0-9_]+)\]/g, '<span style="color:#34d399; font-weight:600; font-size:0.85em; background:rgba(52,211,153,0.15); padding:2px 6px; border-radius:4px;">[$1]</span>');
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
