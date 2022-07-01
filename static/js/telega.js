function tg(chat_id, token, message) {
    const URL_API = `https://api.telegram.org/bot${token}/sendMessage`;
    const CHAT_ID = chat_id
    const MESSAGE = message
    document.getElementById("tag").addEventListener("submit", function (e) {
        e.preventDefault();

        axios.post(URL_API, {
            chat_id: CHAT_ID,
            parse_mode: "html",
            text: message,
        })
    })
}