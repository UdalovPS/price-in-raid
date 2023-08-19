import json


data = {'eng': {
    'lng': 'eng',
    'instruction': 'Instruction',
    'download': 'Download',
    'login': 'Login',
    'register': 'Register',
    'password': 'Password',
    'email': 'Email',
    'password2': 'Password confirmation',
    'create_btn': "CREATE",
    'login_btn': 'Log In',
    'logout': 'Logout',
    'profile': 'Profile',
    'login_log': 'Login',
    'not_register': 'Not register?',
    'alredy_registered': 'Already registered?',
    'ip': 'IP address',
    'assess_date': 'Date to assess',
    'change_password': 'Change password',
    'extend_sub': 'Extend subscribe',
    'old_password': 'Old password',
    'new_password': 'New password',
    'new_password_conf': 'New password confirmation',
    'drop': 'Drop password',
    'drop_btn': "Drop",
    'forget': 'forget password?'
  },
  'rus': {
    'lng': 'rus',
    'instruction':  'Инструкция',
    'download': 'Скачать',
    'login': 'Войти',
    'register': 'Регистрация',
    'password': 'Пароль',
    'email': 'Почта',
    'password2': 'Подтверждение пароля',
    'create_btn': "СОЗДАТЬ",
    'login_btn': 'ВОЙТИ',
    'logout': 'Выйти',
    'profile': 'Профиль',
    'login_log': 'Логин',
    'not_register': 'Не зарегистрирован?',
    'alredy_registered': 'Уже зарегистрирован?',
    'ip': 'IP адрес',
    'assess_date': 'Дата доступа',
    'change_password': 'Изменить пароль',
    'extend_sub': 'Продлить подиску',
    'old_password': 'Старый пароль',
    'new_password': 'Новый пароль',
    'new_password_conf': 'Подтверждения пароля',
    'drop': 'Сбросить пароль',
    'drop_btn': "Сбросить",
    'forget': 'Забыл пароль?'
  }
}

with open('../static_files/web_text.json', 'w') as f:
    json.dump(data, f)
