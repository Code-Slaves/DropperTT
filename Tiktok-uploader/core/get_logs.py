from models import LogData
from database import session, engine

def proxy_split(proxy:str):
	# Разделяем строку по символу ':' и распаковываем результаты
	ip, port, login, password = proxy.split(':')

	# Формируем строку с IP и портом
	ip_port = f"{ip}:{port}"

	# Формируем словарь с логином и паролем
	auth = f"{login}:{password}"

	return f"{auth}@{ip_port}"



def get_logs():
	with session:
		return session.query(LogData).all()
