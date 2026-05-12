// Configuração: Netlify injeta a URL do Railway via config.js
const API_BASE = window.__OBSIDIAI_CONFIG__?.API_BASE_URL ||
    (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
        ? "http://localhost:8000/api"
        : "https://YOUR-RAILWAY-APP.up.railway.app/api");

// Elementos da UI
const menuItems = document.querySelectorAll('.menu-item');
const views = document.querySelectorAll('.view');
const statChunks = document.getElementById('stat-chunks');

const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('resultsContainer');

const vaultList = document.getElementById('vaultList');
const clearVaultFilterBtn = document.getElementById('clearVaultFilterBtn');
const documentList = document.getElementById('documentList');
const documentCountLabel = document.getElementById('documentCountLabel');
const documentReader = document.getElementById('documentReader');

const chatInput = document.getElementById('chatInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const chatHistory = document.getElementById('chatHistory');

// Estado
let chatMessages = [];
let currentVault = null;
let currentDocuments = [];
let currentDocumentId = null;

document.addEventListener("DOMContentLoaded", () => {
    initializeApp();
});

async function initializeApp() {
    bindNavigation();
    bindSearch();
    bindChat();

    await Promise.all([
        fetchStats(),
        fetchVaults(),
        fetchDocuments(),
    ]);
}

function bindNavigation() {
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            menuItems.forEach(mi => mi.classList.remove('active'));
            e.currentTarget.classList.add('active');

            const viewId = e.currentTarget.getAttribute('data-view');
            views.forEach(view => view.classList.remove('active-view'));
            document.getElementById(`view-${viewId}`).classList.add('active-view');
        });
    });
}

function bindSearch() {
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    clearVaultFilterBtn.addEventListener('click', () => {
        selectVault(null);
    });
}

function bindChat() {
    sendMessageBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
    });
}

async function fetchStats() {
    try {
        const res = await fetch(`${API_BASE}/stats`);
        const data = await res.json();
        statChunks.innerText = data.total_documents || data.total_chunks || 0;
    } catch (err) {
        console.error("Erro ao buscar stats", err);
        statChunks.innerText = "Offline";
    }
}

async function fetchVaults() {
    try {
        const res = await fetch(`${API_BASE}/vaults`);
        if (!res.ok) throw new Error("Falha ao carregar vaults");
        const data = await res.json();
        renderVaults(data.vaults || []);
    } catch (err) {
        vaultList.innerHTML = '<div class="empty-state">Não foi possível carregar os vaults.</div>';
    }
}

async function fetchDocuments(vault = null) {
    try {
        const url = new URL(`${API_BASE}/documents`);
        url.searchParams.set('limit', '100');
        if (vault) url.searchParams.set('vault', vault);

        const res = await fetch(url.toString());
        if (!res.ok) throw new Error("Falha ao carregar documentos");
        const data = await res.json();
        currentDocuments = data.results || [];
        renderDocuments(currentDocuments);

        documentCountLabel.innerText = currentDocuments.length;

        if (currentDocuments.length > 0 && !currentDocumentId) {
            openDocument(currentDocuments[0].id);
        }
    } catch (err) {
        documentList.innerHTML = '<div class="empty-state">Não foi possível carregar os documentos.</div>';
        documentCountLabel.innerText = '0';
    }
}

function renderVaults(vaults) {
    const items = ['<button class="vault-pill vault-pill-active" data-vault="">Todos</button>']
        .concat(vaults.map(vault => `<button class="vault-pill" data-vault="${escapeHtml(vault)}">${escapeHtml(vault)}</button>`));

    vaultList.innerHTML = items.join('');
    vaultList.querySelectorAll('.vault-pill').forEach(btn => {
        btn.addEventListener('click', () => selectVault(btn.getAttribute('data-vault') || null));
    });
}

function selectVault(vault) {
    currentVault = vault || null;

    vaultList.querySelectorAll('.vault-pill').forEach(btn => {
        const active = (btn.getAttribute('data-vault') || null) === currentVault;
        btn.classList.toggle('vault-pill-active', active);
    });

    clearVaultFilterBtn.classList.toggle('is-active', !currentVault);
    currentDocumentId = null;
    fetchDocuments(currentVault);
}

function renderDocuments(documents) {
    if (!documents.length) {
        documentList.innerHTML = '<div class="empty-state">Sem documentos para este vault.</div>';
        return;
    }

    documentList.innerHTML = documents.map(doc => `
        <button class="document-item" data-document-id="${doc.id}">
            <div class="document-title">${escapeHtml(doc.title || doc.filepath)}</div>
            <div class="document-path">${escapeHtml(doc.filepath)}</div>
        </button>
    `).join('');

    documentList.querySelectorAll('.document-item').forEach(item => {
        item.addEventListener('click', () => openDocument(item.getAttribute('data-document-id')));
    });
}

async function openDocument(documentId) {
    currentDocumentId = documentId;

    documentList.querySelectorAll('.document-item').forEach(item => {
        item.classList.toggle('active', item.getAttribute('data-document-id') === documentId);
    });

    documentReader.innerHTML = '<div class="empty-state">Carregando nota...</div>';

    try {
        const res = await fetch(`${API_BASE}/documents/${documentId}`);
        if (!res.ok) throw new Error("Falha ao carregar documento");
        const doc = await res.json();
        renderDocumentReader(doc);
    } catch (err) {
        documentReader.innerHTML = '<div class="empty-state">Não foi possível abrir essa nota.</div>';
    }
}

function renderDocumentReader(doc) {
    const metadata = doc.metadata || {};
    const chunks = doc.chunks || [];
    const content = chunks.map(chunk => chunk.content).join('\n\n---\n\n');

    const tags = metadata.tags || [];
    const links = metadata.links || [];

    documentReader.innerHTML = `
        <div class="reader-header">
            <div>
                <div class="reader-vault">${escapeHtml(doc.vault || '')}</div>
                <h2 class="reader-title">${escapeHtml(doc.title || doc.filepath || 'Documento')}</h2>
                <div class="reader-path">${escapeHtml(doc.filepath || '')}</div>
            </div>
            <button class="link-button" id="openRawContentBtn" type="button">Ver texto bruto</button>
        </div>
        <div class="reader-meta">
            ${tags.length ? `<span class="meta-group">Tags: ${tags.map(escapeHtml).join(', ')}</span>` : '<span class="meta-group">Sem tags detectadas</span>'}
            ${links.length ? `<span class="meta-group">Links: ${links.map(escapeHtml).join(', ')}</span>` : '<span class="meta-group">Sem links detectados</span>'}
        </div>
        <div class="reader-content" id="readerContent">${renderMarkdownPreview(content)}</div>
        <div class="reader-relations">
            <section class="relation-card">
                <div class="panel-header">
                    <h3>Relacionadas</h3>
                </div>
                <div id="relatedDocuments" class="relation-list">
                    <div class="empty-state">Carregando relações...</div>
                </div>
            </section>
            <section class="relation-card">
                <div class="panel-header">
                    <h3>Backlinks</h3>
                </div>
                <div id="backlinkDocuments" class="relation-list">
                    <div class="empty-state">Carregando backlinks...</div>
                </div>
            </section>
        </div>
        <details class="reader-details">
            <summary>Chunks (${chunks.length})</summary>
            <div class="chunk-list">
                ${chunks.map((chunk, index) => `
                    <article class="chunk-card">
                        <div class="chunk-index">Chunk ${index + 1}</div>
                        <pre>${escapeHtml(chunk.content || '')}</pre>
                    </article>
                `).join('')}
            </div>
        </details>
    `;

    const openRawContentBtn = document.getElementById('openRawContentBtn');
    openRawContentBtn.addEventListener('click', () => {
        const readerContent = document.getElementById('readerContent');
        readerContent.classList.toggle('is-raw');
        readerContent.innerHTML = readerContent.classList.contains('is-raw')
            ? `<pre>${escapeHtml(content)}</pre>`
            : renderMarkdownPreview(content);
    });

    loadDocumentRelations(doc.id);
}

async function loadDocumentRelations(documentId) {
    const relatedContainer = document.getElementById('relatedDocuments');
    const backlinkContainer = document.getElementById('backlinkDocuments');

    try {
        const res = await fetch(`${API_BASE}/documents/${documentId}/related`);
        if (!res.ok) throw new Error("Falha ao carregar relações");
        const data = await res.json();
        renderRelationList(relatedContainer, data.related || []);
        renderRelationList(backlinkContainer, data.backlinks || []);
    } catch (err) {
        relatedContainer.innerHTML = '<div class="empty-state">Não foi possível carregar notas relacionadas.</div>';
        backlinkContainer.innerHTML = '<div class="empty-state">Não foi possível carregar backlinks.</div>';
    }
}

function renderRelationList(container, items) {
    if (!items.length) {
        container.innerHTML = '<div class="empty-state">Nada encontrado.</div>';
        return;
    }

    container.innerHTML = items.map(item => `
        <button class="relation-item" data-document-id="${item.id}">
            <div class="relation-title">${escapeHtml(item.title || item.filepath || 'Documento')}</div>
            <div class="relation-path">${escapeHtml(item.filepath || '')}</div>
        </button>
    `).join('');

    container.querySelectorAll('.relation-item').forEach(item => {
        item.addEventListener('click', () => openDocument(item.getAttribute('data-document-id')));
    });
}

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    resultsContainer.innerHTML = '<div class="empty-state">Buscando na sua rede...</div>';

    try {
        const res = await fetch(`${API_BASE}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, limit: 10, vault: currentVault })
        });

        if (!res.ok) throw new Error("Erro na API");
        const data = await res.json();

        renderSearchResults(data.results);
    } catch (err) {
        resultsContainer.innerHTML = '<div class="empty-state danger">Falha ao conectar com o cofre. Verifique se o servidor está rodando.</div>';
    }
}

function renderSearchResults(results) {
    if (!results || results.length === 0) {
        resultsContainer.innerHTML = '<div class="empty-state">Nenhuma nota encontrada com esse significado. Tente outros termos.</div>';
        return;
    }

    resultsContainer.innerHTML = results.map(result => `
        <button class="result-card result-card-button" data-document-id="${result.id}">
            <div class="result-meta">
                <span class="badge-vault">${escapeHtml(result.vault || '')}</span>
                <span class="badge-path">${escapeHtml(result.filepath || '')}</span>
            </div>
            <p>${escapeHtml(result.content || '').replace(/\n/g, '<br>')}</p>
        </button>
    `).join('');

    resultsContainer.querySelectorAll('.result-card-button').forEach(item => {
        item.addEventListener('click', () => openDocument(item.getAttribute('data-document-id')));
    });
}

async function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    chatInput.value = '';

    appendMessageToChat('user', text);
    chatMessages.push({ role: "user", content: text });

    const loadingId = appendLoadingMessage();

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: chatMessages })
        });

        document.getElementById(loadingId).remove();

        if (!res.ok) throw new Error("Erro na resposta da AI");
        const data = await res.json();

        chatMessages.push({ role: "assistant", content: data.reply });
        appendMessageToChat('ai', data.reply);

    } catch (err) {
        document.getElementById(loadingId).remove();
        appendMessageToChat('ai', "Desculpe, ocorreu um erro ao acessar o seu cofre.");
    }
}

function appendMessageToChat(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}-message`;

    const avatar = role === 'user' ? '👤' : '✨';
    const formattedText = escapeHtml(text).replace(/(?:\r\n|\r|\n)/g, '<br>');

    div.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble">${formattedText}</div>
    `;

    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function appendLoadingMessage() {
    const id = `msg-${Date.now()}`;
    const div = document.createElement('div');
    div.className = `message ai-message`;
    div.id = id;
    div.innerHTML = `
        <div class="avatar">✨</div>
        <div class="bubble">...</div>
    `;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return id;
}

function renderMarkdownPreview(content) {
    const escaped = escapeHtml(content || '');
    const withLinks = escaped.replace(/\[\[(.*?)\]\]/g, '<span class="wiki-link">[[$1]]</span>');
    return `<pre>${withLinks}</pre>`;
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
