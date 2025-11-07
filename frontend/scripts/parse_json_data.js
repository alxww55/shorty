function renderShortenedUrl(data) {
    const urlPrefix = document.getElementById('server_url').textContent
    const shortenedCode = urlPrefix + data.shortened_code

    document.getElementById('result').textContent = shortenedCode
}

document.body.addEventListener('htmx:afterRequest', (evt) => {
    try {
        const response = JSON.parse(evt.detail.xhr.responseText)
        renderShortenedUrl(response)
    } catch (e) {
        console.error('HTMX JSON parse error:', e)
    }
})