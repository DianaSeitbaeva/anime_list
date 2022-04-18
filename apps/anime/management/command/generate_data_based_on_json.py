from typing import Optional
from datetime import datetime

from requests import get as r_get
from requests.models import Response

from django.core.management.base import BaseCommand

from anime.models import (
    Description,
    Title,
    ReleaseDate,
    Anime,
    Genre,
)


class Command(BaseCommand):
    """Custom command for filling up database from JSON."""

    help = 'Custom command for filling up database from JSON.'

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        pass

    def __get_generated_release_date(
        self,
        start_date: str
    ) -> Optional[ReleaseDate]:
        """Generates ReleaseDate object."""

        # Apr 6, 2016, 18:25 (JST)

        month_map: dict = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12',
        }
        published: str = start_date.split(' (')[0]
        date: Optional[datetime] = None

        month: str = published[0:3]        # 'Apr'
        month_num: str = month_map[month]  # '04'
        published = published.replace(
            month,
            month_num
        )
        month_day: str
        year: str
        time: str
        month_day, year, time = published.split(',')

        year = year.replace(' ', '')
        time = time.replace(' ', '')

        _: str
        day: str
        _, day = month_day.split(' ')

        day_str: str = ''.join(
            [
                '0',
                day
            ]
        )
        result: str = f'{day_str}/{month_num}/{year} {time}'

        print('# ------------------------------------------------')
        print(result)

        # release_date: Optional[ReleaseDate] = \
        #     ReleaseDate.objects.get_or_create(
        #         published=published,
        #         date=date
        #     )
        # return release_date

    def _generate_anime(self) -> None:
        """Generates Anime objects."""

        anime_public_resource_url: str = \
            'https://raw.githubusercontent.com/asarode/anime-list/master/data/data.json'  # noqa

        # Делаем запрос в открытый источник методом GET
        #
        response: Response = r_get(anime_public_resource_url)

        if response.status_code != 200:
            return None

        data: list = response.json()

        obj: dict
        for obj in data:

            # title: Title = \
            #     Title.objects.get_or_create(
            #         name=obj['title']['text'],
            #         link=obj['title']['link']
            #     )
            # description: Description = \
            #     Description.objects.get_or_create(
            #         text_en=obj['description']
            #     )
            release_date: ReleaseDate = \
                self.__get_generated_release_date(
                    obj['start_date']
                )
            # anime: Anime = \
            #     Anime.objects.get_or_create(
            #         studio=obj['studio'],
            #         rating=obj['hype'],
            #         title=title,
            #         description=description,
            #         release_date=release_date
            #     )
            # genre.add(anime)

            # obj['studio']
            # obj['genres']
            # obj['hype']
            # obj['description']
            # obj['title']
            # obj['start_date']

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling."""

        start: datetime = datetime.now()

        self._generate_anime()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
