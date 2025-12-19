const urlInput = document.getElementById('original_url');
const codeInput = document.getElementById('shortened_code');
const createdText = document.getElementById('created_link');
const result = document.getElementById('result');
const messageContainer = document.getElementById('message-container');
const serverUrlElem = document.getElementById('server_url');
const copyButton = document.getElementById('copy-button');
const resultContainer = document.getElementById('result-container');

const ICON_PATH_CHECKMARK = 'M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z';
const ICON_PATH_COPY = 'M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z';

function createIconSvg(path, color = '#06df72') {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'w-5 h-5');
    svg.setAttribute('fill', color);
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

    const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    pathEl.setAttribute('d', path);
    svg.appendChild(pathEl);
    return svg;
}

function createSvgPath(d, fillRule = null) {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    if (fillRule) path.setAttribute('fill-rule', fillRule);
    return path;
}

function createMessageSpan(text, iconPath, iconClass = 'w-4 h-4', textClass = 'text-sm text-red-400 font-medium flex items-center gap-2') {
    const span = document.createElement('span');
    span.className = textClass;

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', iconClass);
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('viewBox', '0 0 20 20');
    svg.appendChild(createSvgPath(iconPath, 'evenodd'));

    span.appendChild(svg);
    span.appendChild(document.createTextNode(text));
    return span;
}

function resetCopyButtonToCopyIcon() {
    copyButton.innerHTML = '';
    copyButton.appendChild(createIconSvg(ICON_PATH_COPY));
    copyButton.classList.remove('bg-green-500/40', 'border-green-500');
    copyButton.classList.add('bg-green-500/20', 'border-green-500/50');
}

function hideMessages() {
    messageContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    createdText.textContent = '';
    result.textContent = '';
    // НЕ сбрасываем кнопку здесь, чтобы не мешать копированию
}

function showMessagesWithLink() {
    messageContainer.style.display = 'block';
    resultContainer.style.display = 'block';
    // Сбрасываем кнопку только когда показываем НОВУЮ ссылку
    resetCopyButtonToCopyIcon();
}

function showMessagesError(detail) {
    messageContainer.style.display = 'block';
    resultContainer.style.display = 'none';

    let errorMessage = detail instanceof Array ? detail.join(', ') : (typeof detail === 'string' ? detail : 'Unexpected error');
    const errorPath = 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z';

    createdText.innerHTML = '';
    createdText.appendChild(createMessageSpan(errorMessage, errorPath));
    result.textContent = '';
    // При ошибке тоже сбрасываем кнопку
    resetCopyButtonToCopyIcon();
}

function renderShortenedUrl(data) {
    if (!data || !data.shortened_code) return;
    const urlPrefix = serverUrlElem ? serverUrlElem.textContent : '';
    result.textContent = urlPrefix + data.shortened_code;
}

function copyToClipboard() {
    const text = result.textContent;
    if (!text) return;

    navigator.clipboard.writeText(text).then(() => {
        copyButton.innerHTML = '';
        copyButton.appendChild(createIconSvg(ICON_PATH_CHECKMARK));
        copyButton.classList.add('bg-green-500/40', 'border-green-500');
        copyButton.classList.remove('bg-green-500/20', 'border-green-500/50');
    });
}

// Инициализация кнопки при загрузке
document.addEventListener('DOMContentLoaded', function () {
    resetCopyButtonToCopyIcon();
});

copyButton.addEventListener('click', copyToClipboard);
result.addEventListener('click', copyToClipboard);

document.body.addEventListener('htmx:beforeRequest', function (evt) {
    // Проверяем, что это запрос на создание новой ссылки, а не другой
    const target = evt.detail.target;
    if (target && (target.id === 'result-container' || target.id === 'message-container')) {
        hideMessages();
    }
});

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
            const successPath = 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z';

            createdText.innerHTML = '';
            createdText.appendChild(createMessageSpan('Your short link is ready!', successPath, 'w-4 h-4', 'text-sm text-green-400 font-medium flex items-center gap-2'));
            renderShortenedUrl(responseJson);
            showMessagesWithLink(); // Здесь сбрасываем кнопку
        } catch {
            hideMessages();
        }
    } else if ([409, 422, 500].includes(status)) {
        showMessagesError(detail); // Здесь тоже сбрасываем кнопку
    }
});