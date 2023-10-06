const loginForm = document.querySelector('.signup__form');
const login = document.querySelector('.input-login');
const password = document.querySelector('.input-password');
const confirmPassword = document.querySelector('.input-confirm-password');
const email = document.querySelector('.input-email');
const EMAIL_REGEXP = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;

loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    removeValidation();
    checkFieldsLength();
    checkEmailFormat();
    checkPasswordsMatch();
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

  //Проверка, что пароли совпадают
  const checkPasswordsMatch= function () {
    if (confirmPassword.value !== password.value) {
      const error = generateError('Пароли не совпадают');
      confirmPassword.parentElement.insertBefore(error, confirmPassword);
    }
  }

  //Проверка длины полей
  const checkFieldsLength = function () {
    if (login.value.length > 50 || login.value.length < 1) {
      const error = generateError('Длина от 1 до 50 символов');
      login.parentElement.insertBefore(error, login);
    }
    if (password.value.length > 50 || password.value.length < 1) {
      const error = generateError('Длина от 1 до 50 символов');
      password.parentElement.insertBefore(error, password);
    }
    if (email.value.length > 150 || email.value.length < 1) {
      const error = generateError('Длина от 1 до 150 символов');
      email.parentElement.insertBefore(error, email);
    }
  }

 //Валидация почты
 const checkEmailFormat = function () {
    if (!(EMAIL_REGEXP.test(email.value))) {
      const error = generateError('Неверный формат почты');
      email.parentElement.insertBefore(error, email);
    }
 }

