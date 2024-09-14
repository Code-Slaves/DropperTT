from core import get_title, get_logs, proxy_split, get_tags
from logic import main
from uniqueizer import Unique
from config import Configuration
from TikTokUploader import uploadVideo
import time

main()

novalid_accounts = []


for log in get_logs():
	proxy = proxy_split(log.proxy)

	proxy_dict = {
    'http': f'http://{proxy}'
    }

	session_id = log.session_id
	title = get_title()
	tags = get_tags()
	video = Unique(video_path_input=Configuration.in_vid_path, video_path_output=Configuration.out_vid_path).baytes

	try:
		repl = uploadVideo(session_id=session_id, video=video, title=title, tags=tags, proxy=proxy_dict)
	except Exception as e:
		raise e
		#novalid_accounts.append(session_id)

	time.sleep(120)




print(novalid_accounts)






