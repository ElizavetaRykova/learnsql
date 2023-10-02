const loginForm = document.querySelector('.signin__form');
loginForm.addEventListener('submit', function (e) {
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

const removeValidation = function () {
  const errors = document.querySelectorAll('.error');
  for (let i = 0; i < errors.length; i++) {
    errors[i].remove()
  }
}

const checkFieldsPresence = function () {
  const login = document.querySelector('.input-login');
  const password = document.querySelector('.input-password');
  if (!login.value.length) {
    const error = generateError('Введите логин');
    login.parentElement.insertBefore(error, login);
  }
  if (!password.value.length) {
    const error = generateError('Введите пароль');
    password.parentElement.insertBefore(error, password);
  }
}