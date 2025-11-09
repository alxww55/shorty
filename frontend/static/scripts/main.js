const codeInput = document.getElementById('shortened_code')
const createdText = document.getElementById('created_link')
const result = document.getElementById('result')
const messageContainer = document.getElementById('message-container')

function hideMessages() {
    messageContainer.style.display = 'none'
    createdText.textContent = ''
    result.textContent = ''
    codeInput.style.borderColor = ''
    createdText.style.color = ''
    result.style.marginTop = '0'
}

function showMessagesWithLink() {
    messageContainer.style.display = 'block'
    result.style.marginTop = '1em'
}

function showMessagesError() {
    messageContainer.style.display = 'block'
    createdText.style.color = '#c90627'
    codeInput.style.borderColor = '#c90627'
    result.style.marginTop = '0'
}

function renderShortenedUrl(data) {
    const urlPrefix = document.getElementById('server_url').textContent
    result.textContent = urlPrefix + data.shortened_code
}

document.body.addEventListener('htmx:beforeRequest', hideMessages)

document.body.addEventListener('htmx:afterRequest', (evt) => {
    const status = evt.detail.xhr.status

    if (status === 201) {
        try {
            const response = JSON.parse(evt.detail.xhr.responseText)
            codeInput.value = ''
            codeInput.style.borderColor = '#3770ee'
            createdText.style.color = '#4ade80'
            createdText.textContent = 'Your short link is ready! Click to copy.'
            renderShortenedUrl(response)
            showMessagesWithLink()
        } catch {
            hideMessages()
        }
    }

    if (status === 409) {
        showMessagesError()
        createdText.textContent = 'This alias is already taken. Try another one.'
        result.textContent = ''
    }

    if (status === 500) {
        showMessagesError()
        createdText.textContent = 'Invalid alias. Only these symbols are allowed: . % & : / - _ ?'

    }
})

