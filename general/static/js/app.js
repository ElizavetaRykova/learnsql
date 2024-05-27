document.addEventListener('DOMContentLoaded', () => {

    const tabs = () => {
        const head = document.querySelector('.result__header')
        const body = document.querySelector('.result__body')

    const getActiveTabName = () => { 
        return head.querySelector('.result__tab-header_active').dataset.tab
    }

    const setActiveContent = () => { 
        if (body.querySelector('.result__tab-content_active')) {
          body.querySelector('.result__tab-content_active').classList.remove('result__tab-content_active')
        }
        body.querySelector(`[data-tab=${getActiveTabName()}]`).classList.add('result__tab-content_active') 
    }

    if (!head.querySelector('.result__tab-header_active')) {
        head.querySelector('.result__tab-header').classList.add('result__tab-header_active')
    }
    setActiveContent(getActiveTabName())

    head.addEventListener('click', e => {
      const caption = e.target.closest('.result__tab-header')
      if (!caption) return
      if (caption.classList.contains('result__tab-header_active')) return

      if (head.querySelector('.result__tab-header_active')) {
        head.querySelector('.result__tab-header_active').classList.remove('result__tab-header_active')
      }

      caption.classList.add('result__tab-header_active')

      setActiveContent(getActiveTabName())
    })
  }

  tabs()

})

var acc = document.getElementsByClassName("task__support-button");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}

//проверка на заполненность поля перед отправкой комментария
const addComment = document.querySelector('.question__support-button');
addComment.addEventListener('click', function (e) {
  e.preventDefault();
  removeValidation();
  checkFieldsPresence();
})

const generateError = function (text) {
  const error = document.createElement('div');
  error.classList.add('error');
  error.style.color = '#B60000';
  error.innerHTML = text;
  return error;
}

const successMessage = function (text) {
    const success = document.createElement('div');
    success.classList.add('success');
    success.style.color = '#B60000';
    success.style.marginTop = '15px';
    success.innerHTML = text;
    return success;
  }

const removeValidation = function () {
  const errors = document.querySelectorAll('.error');
  for (let i = 0; i < errors.length; i++) {
    errors[i].remove()
  }
  const success = document.querySelectorAll('.success');
  for (let i = 0; i < success.length; i++) {
    success[i].remove()
  } 
}

const checkFieldsPresence = function () {
  const comment = document.querySelector('.task__question-comment-text');
  if (!comment.value.length) {
    const error = generateError('Введите комментарий');
    comment.parentElement.insertBefore(error, comment);
  }
  else {
    const message = document.querySelector('.task__question');
    const success = successMessage('Комментарий добавлен');
    message.parentElement.insertBefore(success, message);
  }
}
