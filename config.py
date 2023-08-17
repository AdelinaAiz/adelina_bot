from enum import Enum

token = '6574375480:AAFDzPR6245hCD7zY9B-OTReCmf_fLKcvBU'
db_file = 'database.vdb'


class States(Enum):
    s_all = '0'  # до нажатия кнопки ПОСЛУШАТЬ
    s_listen = '1'  # после нажатия

