function tg_task_push_employee(chat_id, token_tg_bot, message) {
    const URL_API = `https://api.telegram.org/bot${token_tg_bot}/sendMessage`;
    const CHAT_ID = chat_id
    const MESSAGE = message


    document.getElementById("tag").addEventListener("submit", function (e) {
        e.preventDefault();

        axios.post(URL_API, {
            chat_id: CHAT_ID,
            parse_mode: "html",
            text: MESSAGE,
        })
    })
}
