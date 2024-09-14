from bs4 import BeautifulSoup
import requests


class GetStatistic:
    def __init__(self, name:str):
        self.statistic = self.get_sats(name)

    def convert_value_to_int(self, value):
        if value.endswith('K'):
            return int(float(value[:-1]) * 1000)
        elif value.endswith('M'):
            return int(float(value[:-1]) * 1000000)
        elif value.endswith('B'):
            return int(float(value[:-1]) * 1000000000)
        elif '.' in value:
            return int(float(value))
        else:
            return int(value)


    def get_sats(self, tiktok_username):
        try:
            source = requests.get(f'https://www.tiktok.com/@{tiktok_username}')
            source.raise_for_status()

            soup = BeautifulSoup(source.text, 'html.parser')
            user_info = soup.find('h3', class_="tiktok-12ijsdd-H3CountInfos e1457k4r0").find_all('div')
            user_total_following = user_info[0].find('strong').text
            user_total_followers = user_info[1].find('strong').text
            user_total_likes = user_info[2].find('strong').text

            user_total_followers = self.convert_value_to_int(user_total_followers)
            user_total_likes = self.convert_value_to_int(user_total_likes)

            video_container = soup.find('div', {'class': 'tiktok-yvmafn-DivVideoFeedV2 ecyq5ls0'})
            if video_container:
                videos = video_container.find_all('div', class_="tiktok-x6y88p-DivItemContainerV2 e19c29qe8")
            else:
                videos = []

            video_data = []
            user_total_views = 0
            for video in videos:
                views_elem = video.find('div', {'class': 'tiktok-11u47i-DivCardFooter e148ts220'}).find_all('strong')
                view = views_elem[0].text if views_elem else None

                views = self.convert_value_to_int(view) if view else None

                user_total_views += views


            user_data = {
                'Username': tiktok_username,
                'Total Followers': user_total_followers,
                'Total Video Likes': user_total_likes,
                'Total Video Views': user_total_views,
            }


            return user_data

        except Exception as e:
            return {}

