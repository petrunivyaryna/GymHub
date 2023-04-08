# GymHub

Застосунок декомпозований на файли run.py, __init__.py, forms.py, models.py, routes.py

## run.py
Цей модуль запускає програму

## __init__.py
Тут відбувається зчитування з файлу .env важливих конфігурацій для запуску програми. Також в цьому файлі імпортовується SQLAlchemy, Bcrypt, LoginManager та Mail для подальшої роботи з базами даних та поштою.

## routes.py
Це є головний файл у якому створюється можливість взаємодіяти між сторінками. Тут імпортовується багато бібліотек.

main - головна сторінка з кнопками зареєструватися та увійти. Також якщо натиснути на емблему сайту можна перейти на сторінку "Про нас". По кнопці інстаграм можна побачити інстаграм сторінку з актуальною інформацією про зал. Якщо виникають запитання - можете писати на пошту, гіперпосилання реалізоване.

home - сторінка про нас, коли користувач авторизований.

home_1 - сторінка про нас, коли користувач не авторизований.

register - сторінка для реєстрації. Тут є поля введення такі, як Імʼя, Пошта, Пароль і підтвердження його. Пошту програма автоматично перевіряє на існування. Якщо якесь поле заповнене неправильно, сайт вам про це підкаже.

login - сторінка для входу. Тут потрібно внести тільки пошту та пароль, якщо користувач бажає, то може залишитись у системі. Якщо користувач забув пароль до акаунту, то його можна перевірити за допомогою листа на пошті, обовʼязково перевірте свою скриньку.

logout - це реалізовано, якщо кориистувач бажає вийти з акаунту.

save_picture - ця функція потрібна для оновлення своєї фотографії на сторінці "Мій Профіль". Фото потрібно завантажити у форматі png, jpeg або jpg.

account - сторінка на якій можна побачити інформацію про акаунт, а також оновити пошту, імʼя, а також фото. 
На цій сторінці також показується інформація про вашу історію занять, а також заплановані. Також заняття модна скасувати, якщо ви цього бажаєте.

send_reset_email, reset_token та reset_request реалізовані для скидання та оновлання паролю за допомогою листа на пошті.

trainer - сторінка з сожливістю забранювати заняття у тренера.
Для вас представлено карусель з днями і годиинами, коли тренер працює, короткий опис та фото тренера. Збоку для вас є відповідні поля, де ви можете записатися на індивідуільне заняття.

abonement - сторінка для запису у тренажерниц зал. На ній описано ціни та для кого призначенні абонементи. Натиснувши на кнопку "Зареєструватися" вас перекине на гугл форму, де вже можна оформити абонемент.

## models.py
У цьому файлі реалізована підтримку бази даних та коректного збереження для Користувача та Тренування.

## forms.py
Саме тут реалізовано класи для полів заповнення на всьому сайті.
Серед них RegistrationForm, LoginForm, UpdateAccountForm RequestResetForm, ResetPasswordForm, ChooseTrainerForm
Тут реалізовано перевірки на правильність введення даних у поля. Наприклад, для пошти важливим є її існування, для вибору дати тренера чи ця дата відповідає тренеру і чи не обирається заняття з минулого.

# carousel.js
У цьому модулі реалізовно скрипт для каруселі на сторінці "Обрати тренера". Перемикатися можна як кнопками, так і точками під каруселлю.

# main.css 
Тут реалізовано весь css код для вебзастосунок