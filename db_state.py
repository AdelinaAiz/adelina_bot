from vedis import Vedis
import config


# Часть команд должна быть реализована кнопками, другая часть - текстом.
# Поэтому дадим пользователю возможность вводить текст с просьбой прислать войс.
# Но такая возможность должна появиться только после нажатия на кнопку ПОСЛУШАТЬ,
# далее последует инструкция, впоследствии он в любое время сможет попросить бот прислать ему войс.
# Состояние будет меняться только при первом нажатии на кнопку ПОСЛУШАТЬ (0 -> 1) и при команде \start (1 -> 0)
def get_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.s_all.value


# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except KeyError:
            return False
