from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from index.indexForms import MainForm
from datetime import datetime, timedelta
import ntplib
from datetime import datetime, timezone
import re

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit_login = SubmitField('Войти')
    submit_register = SubmitField('Зарегистрироваться')


bp_index = Blueprint('bp_index', __name__)

@bp_index.route('/index', methods=['GET', 'POST'])
def index():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org', version=3)

    # Преобразуем NTP время в datetime
    ntp_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    ntp_time = ntp_time + timedelta(hours=4)
    #is_correct_date = ntp_time.date() == datetime(2026, 1, 1).date()
    is_correct_date = ntp_time.date() == datetime(2025, 12, 26).date()

    text = "Текст закрыт до Нового года, типо, да..."
    if is_correct_date:
        text = """
            Если этот текст есть, то уже 2026 год! 
            Привет, эм, короче, ты наверное думаешь, а нахер я так сделал.
            Ну, написал этот текст там, который ты сейчас очень внимательно (но наверное нет) читаешь.
            Просто мне как обычно в том числе и страшно тебе так написать, потому что тебе придется мне что-то ответить:
            вообще тут не должно быть ничего страшного в тексте по факту, но я думаю тебя в целом достает
            видеть от меня сообщения и вообще вспоминать о моем существовании)
            
            Но это нормально, я бы тоже не хотел вспоминать, что я зачем-то существую, но я то вынужден терпеть
            себя каждый день.
            Блин, наверное я все равно напишу тебе в телегу, потому что я думаю, что ты забудешь это прочитать,
            просто потому что ты обычно все забываешь, ладно, давай к основному тексту:
            
            В общем, хочу поздравить тебя с Новым годом,
            я думаю, тебе было непросто в этом году, разные сборы, переезд, да ты и сама знаешь лучше меня.
            Но то что вижу я, и, надеюсь так-то, что это правда, что тебе в целом хорошо и у тебя всё в жизни замечательно!
            Потому что ты так спокойно к этому относишься, меня это немного вдохновляет. 
            
            Ты вообще очень крутая, веселая и всегда смешно шутишь, и с тобой всегда так комфортно общаться, ну для
            меня даже в реальности, а я ваще особо не общаюсь с людьми и не хочу. 
            Тебе со мной не очень конечно комфортно, но я надеюсь что ты 
            хотя бы не сильно на меня из-за этого злишься, не думай, что я тебя не слышу, просто иногда я 
            скучаю по приятному вайбу.
            Пусть у тебя будет всё так же замечательно, потому что ты способна на что угодно, 
            и самое важное, что ты этого заслуживаешь.
            Я могу много говорить о том, какая ты крутая, но давай чтобы тебя не смущать, скажу кратко:
            Желаю тебе новых побед, жизненного спокойствия, чтобы ты хорошо к себе относилась и ценила свои заслуги,
            потому что со стороны я вижу твои экстраординарные способности.
            Я знаю, что мои действия иногда кажутся тебе не совсем доверительными, я понимаю, но хочу чтобы ты знала,
            что если тебе в чем-то нужна помощь, то я всегда готов помочь тебе,
            я очень рад, что я тебя знаю, спасибо тебе и 
            с Новым годом!)  
            
            Post Scriptum. Мои планы на Новый год: постараться не умереть (как же он старается)
        
        """

    max_words = 15
    updated_text = []
    cnt = 0
    current_text = ""
    words = text.split(' ')

    for x in words:
        if x == "":
            continue
        if cnt < max_words:
            cnt += 1
            current_text = current_text + " " + x
        else:
            updated_text.append(current_text.strip())
            current_text = x
            cnt = 1
    if cnt > 0:
        updated_text.append(current_text.strip())

    updated_text = clean_text_lines(updated_text)
    updated_text = make_list(' '.join(updated_text))

    return render_template("index.html", title='Главная страница', text=updated_text)


def clean_text_lines(text_list):
    result = []
    for text in text_list:
        lines = text.split('\n')
        cleaned = [line.lstrip() for line in lines]
        result.append('\n'.join(cleaned))
    return result


def make_list(words, max_words=15):
    result = []
    cnt = 0
    current_text = ""
    for x in words.split(' '):
        x = x.replace('\n',' ')
        x = x.strip()
        x = re.sub(r'\s{2,}', ' ', x)
        if x == ""  :
            continue
        if cnt < max_words:
            cnt += 1
            current_text = current_text + " " + x
        else:
            current_text = current_text.strip()
            current_text = current_text + " "
            result.append(current_text)
            current_text = x
            cnt = 1
    if cnt > 0:
        result.append(current_text.strip())
    return result
