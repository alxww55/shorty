const urlInput = document.getElementById('original_url');
const codeInput = document.getElementById('shortened_code');
const createdText = document.getElementById('created_link');
const result = document.getElementById('result');
const messageContainer = document.getElementById('message-container');
const serverUrlElem = document.getElementById('server_url');

function hideMessages() {
    messageContainer.style.display = 'none';
    createdText.textContent = '';
    result.textContent = '';
    urlInput.style.borderColor = '';
    codeInput.style.borderColor = '';
    createdText.style.color = '';
    result.style.marginTop = '0';
}

function showMessagesWithLink() {
    messageContainer.style.display = 'block';
    result.style.marginTop = '1em';
}

function showMessagesError(detail) {
    messageContainer.style.display = 'block';
    createdText.style.color = '#c90627';
    result.style.marginTop = '0';

    if (typeof detail === 'string') {
        createdText.textContent = detail;
        result.textContent = '';
    } else if (Array.isArray(detail)) {
        createdText.textContent = detail.join('\n');
        result.textContent = '';
    } else {
        createdText.textContent = 'Unexpected server error';
        result.textContent = '';
    }
}

function renderShortenedUrl(data) {
    if (!data || !data.shortened_code) return;
    const urlPrefix = serverUrlElem ? serverUrlElem.textContent : '';
    result.textContent = urlPrefix + data.shortened_code;
}

document.body.addEventListener('htmx:beforeRequest', hideMessages);

document.body.addEventListener('htmx:afterRequest', (evt) => {
    const xhr = evt.detail.xhr;
    const status = xhr.status;

    let responseJson = {};
    try {
        responseJson = JSON.parse(xhr.responseText || '{}');
    } catch {
        responseJson = {};
    }

    const detail = responseJson.detail || 'Unexpected server error';

    if (status === 201) {
        try {
            codeInput.value = '';
            createdText.style.color = '#4ade80';
            createdText.textContent = 'Your short link is ready! Click to copy.';
            renderShortenedUrl(responseJson);
            showMessagesWithLink();
        } catch {
            hideMessages();
        }
    } else if ([409, 422, 500].includes(status)) {
        showMessagesError(detail);
    }
});
