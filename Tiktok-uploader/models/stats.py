from sqlalchemy import Column, Integer, String, ForeignKey, JSON, func, DateTime
from sqlalchemy.orm import relationship
from config import Configuration
from datetime import datetime


class Statistic(Configuration.Base):
	__tablename__ = 'Statistic'
	id = Column(Integer, primary_key=True)
	statistic = Column(JSON)
	updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
	log_id = Column(Integer, ForeignKey('LogData.id'))


	log_data = relationship("LogData", back_populates="statistics")


	def __repr__(self):
		return str({
			"id": self.id,
			"statistic": self.statistic,
			"updated_at": self.updated_at,
			"log_id": self.log_id

			})
