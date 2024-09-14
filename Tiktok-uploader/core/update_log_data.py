from database import session, engine
from models import LogData, Statistic

class UpdateLogData:
	def splitting_data(self, accounts:str) -> list:
		accounts = [account.split(";") for account in accounts.split("\n")]

		return accounts

	def update(self, accounts:str):
		accounts = self.splitting_data(accounts)

		LogData.__table__.create(bind=engine, checkfirst=True)
		Statistic.__table__.create(bind=engine, checkfirst=True)

		with session:
			for account in accounts:
				log_data_instance = LogData(login=account[0], password=account[1], proxy=account[2], session_id=account[3])
				log_data_instance.statistics = Statistic(statistic={})
				session.add(log_data_instance)

			session.commit()


