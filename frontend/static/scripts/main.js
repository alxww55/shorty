const urlInput = document.getElementById('original_url');
const codeInput = document.getElementById('shortened_code');
const createdText = document.getElementById('created_link');
const result = document.getElementById('result');
const messageContainer = document.getElementById('message-container');
const serverUrlElem = document.getElementById('server_url');
const copyButton = document.getElementById('copy-button');

function hideMessages() {
    const resultContainer = document.getElementById('result-container');
    messageContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    createdText.textContent = '';
    result.textContent = '';
}

function showMessagesWithLink() {
    const resultContainer = document.getElementById('result-container');
    messageContainer.style.display = 'block';
    resultContainer.style.display = 'block';
}

function showMessagesError(detail) {
    const resultContainer = document.getElementById('result-container');
    messageContainer.style.display = 'block';
    resultContainer.style.display = 'none';

    if (typeof detail === 'string') {
        createdText.innerHTML = `<span class="text-sm text-red-400 font-medium flex items-center gap-2"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>${detail}</span>`;
        result.textContent = '';
    } else if (Array.isArray(detail)) {
        createdText.innerHTML = `<span class="text-sm text-red-400 font-medium flex items-center gap-2"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>${detail.join(', ')}</span>`;
        result.textContent = '';
    } else {
        createdText.innerHTML = `<span class="text-sm text-red-400 font-medium flex items-center gap-2"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>Unexpected error</span>`;
        result.textContent = '';
    }
}

function renderShortenedUrl(data) {
    if (!data || !data.shortened_code) return;
    const urlPrefix = serverUrlElem ? serverUrlElem.textContent : '';
    result.textContent = urlPrefix + data.shortened_code;
}

function copyToClipboard() {
    const text = result.textContent;
    if (text) {
        navigator.clipboard.writeText(text).then(() => {
            const originalSvg = copyButton.innerHTML;
            copyButton.innerHTML = '<svg class="w-5 h-5" fill="#06df72" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"></path></svg>';
            copyButton.classList.add('bg-green-500/40', 'border-green-500');
            copyButton.classList.remove('bg-green-500/20', 'border-green-500/50');

            setTimeout(() => {
                copyButton.innerHTML = originalSvg;
                copyButton.classList.remove('bg-green-500/40', 'border-green-500');
                copyButton.classList.add('bg-green-500/20', 'border-green-500/50');
            }, 2000);
        });
    }
}

copyButton.addEventListener('click', copyToClipboard);
result.addEventListener('click', copyToClipboard);

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
            createdText.innerHTML = '<span class="text-sm text-green-400 font-medium flex items-center gap-2"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>Your short link is ready!</span>';
            renderShortenedUrl(responseJson);
            showMessagesWithLink();
        } catch {
            hideMessages();
        }
    } else if ([409, 422, 500].includes(status)) {
        showMessagesError(detail);
    }
});
