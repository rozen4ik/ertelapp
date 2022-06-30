//это нужно заполнить
const botToken = '5439612252:AAGu4uOExlw007uu7vG-wTjuZYSQkEuYnW4';
// const webAppUrl = 'https://script.google.com/macros/s/AKfycbxHXOnEA3jD9G8RbAujirxHsaBeLSy6uP8m9AHV4E8vq_YyxF0/exec';
const ssID = '1USfWniBGouHUaHXZpFvPli7SNJqqBreEeKO80rXWf3M';

const telegramUrl = 'https://api.telegram.org/bot' + botToken;

// function setWebhook() {
//   var response = UrlFetchApp.fetch(telegramUrl + '/setWebhook?url=' + webAppUrl);
//   Logger.log(response.getContentText());
// }
//
// function deleteWebhook() {
//   var response = UrlFetchApp.fetch(telegramUrl + '/deleteWebhook?url=' + webAppUrl);
//   Logger.log(response.getContentText());
// }
//
// function sendMessage(chatId, message) {
//   UrlFetchApp.fetch(telegramUrl + '/sendMessage', {
//                     method: 'post',
//                     contentType: 'application/json',
//                     payload: JSON.stringify({
//                     chat_id: chatId,
//                     text: message,
//                     parse_mode: 'Markdown'
//                     })
// })
// }

function sendMessageKeyboard(chatId, message, keyBoard){
  UrlFetchApp.fetch(telegramUrl + '/sendMessage', {
                    method: 'post',
                    contentType: 'application/json',
                    payload: JSON.stringify({
                    chat_id: chatId,
                    text: message,
                    reply_markup: {
                    keyboard: keyBoard,
                    resize_keyboard: true,
                    one_time_keyboard: true
                    }
                    })
})
}

function sendMessageInlineMenu(chatId, message, inlineKeyboard){
  UrlFetchApp.fetch(telegramUrl + '/sendMessage', {
                    method: 'post',
                    contentType: 'application/json',
                    payload: JSON.stringify({
                    chat_id: chatId,
                    text: message,
                    reply_markup: {
                    inline_keyboard: inlineKeyboard
                    }
                    })
})
}

function sendMessageKeyboardRemove(chatId, message){
  UrlFetchApp.fetch(telegramUrl + '/sendMessage', {
                    method: 'post',
                    contentType: 'application/json',
                    payload: JSON.stringify({
                    chat_id: chatId,
                    text: message,
                    reply_markup: {
                    remove_keyboard: true
                    }
                    })
})
}