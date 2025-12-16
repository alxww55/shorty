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

    let errorMessage = 'Unexpected error';
    if (typeof detail === 'string') {
        errorMessage = detail;
    } else if (Array.isArray(detail)) {
        errorMessage = detail.join(', ');
    }

    createdText.innerHTML = '';
    const span = document.createElement('span');
    span.className = 'text-sm text-red-400 font-medium flex items-center gap-2';

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'w-4 h-4');
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('viewBox', '0 0 20 20');

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('fill-rule', 'evenodd');
    path.setAttribute('d', 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z');
    path.setAttribute('clip-rule', 'evenodd');
    svg.appendChild(path);

    const text = document.createTextNode(errorMessage);

    span.appendChild(svg);
    span.appendChild(text);
    createdText.appendChild(span);
    result.textContent = '';
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
            const checkmarkSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            checkmarkSvg.setAttribute('class', 'w-5 h-5');
            checkmarkSvg.setAttribute('fill', '#06df72');
            checkmarkSvg.setAttribute('viewBox', '0 0 24 24');
            checkmarkSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            checkmarkSvg.innerHTML = '<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"></path>';

            const originalChild = copyButton.firstChild;
            copyButton.innerHTML = '';
            copyButton.appendChild(checkmarkSvg);
            copyButton.classList.add('bg-green-500/40', 'border-green-500');
            copyButton.classList.remove('bg-green-500/20', 'border-green-500/50');

            setTimeout(() => {
                copyButton.innerHTML = '';
                copyButton.appendChild(originalChild.cloneNode(true));
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

            const span = document.createElement('span');
            span.className = 'text-sm text-green-400 font-medium flex items-center gap-2';

            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('class', 'w-4 h-4');
            svg.setAttribute('fill', 'currentColor');
            svg.setAttribute('viewBox', '0 0 20 20');
            svg.innerHTML = '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>';

            const text = document.createTextNode('Your short link is ready!');

            span.appendChild(svg);
            span.appendChild(text);
            createdText.innerHTML = '';
            createdText.appendChild(span);

            renderShortenedUrl(responseJson);
            showMessagesWithLink();
        } catch {
            hideMessages();
        }
    } else if ([409, 422, 500].includes(status)) {
        showMessagesError(detail);
    }
});
