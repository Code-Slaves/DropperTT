from sqlalchemy.orm import declarative_base

class Configuration:
	#regarding the "run" file in the root directory.
	db_path = "db_storage/database.db"
	Base = declarative_base()

	#path for uniqulizer video
	out_vid_path = "temp_storage/output.mp4"
	in_vid_path = "temp_storage/input.mp4"

	logs_path = "logs/logs.txt"
