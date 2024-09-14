from models import Statistic, LogData
from database import session, engine
from sqlalchemy.orm.attributes import flag_modified
from core.get_tt_stats import GetStatistic


class UpdateStatistic:
	@staticmethod
	def update():
		with session:
			all_log_data = session.query(LogData).all()

			for log_data_instance in all_log_data:
				log_data_instance.statistics.statistic = GetStatistic(log_data_instance.login).statistic

				flag_modified(log_data_instance.statistics, "statistic")

			session.commit()





