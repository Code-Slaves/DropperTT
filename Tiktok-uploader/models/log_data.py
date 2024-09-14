from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config import Configuration
from datetime import datetime



class LogData(Configuration.Base):
    __tablename__ = 'LogData'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    proxy = Column(String, unique=True)
    session_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    statistics = relationship("Statistic", back_populates="log_data", uselist=False)

    def __repr__(self):
        return str({
            "id": self.id,
            "login": self.login,
            "password": self.password, 
            "session_id": self.session_id,
            "created_at": self.created_at
        })






