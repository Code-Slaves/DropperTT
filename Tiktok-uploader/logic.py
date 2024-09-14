from core import UpdateLogData, UpdateStatistic
import os
from config import Configuration



def main() -> None:
	# Проверяем, существует ли файл
	if os.path.isfile(Configuration.logs_path):
		with open(Configuration.logs_path, "r") as f:
			logs = f.read()

			UpdateLogData().update(logs.strip())
		os.remove(Configuration.logs_path)

	UpdateStatistic.update()




