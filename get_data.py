import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd


# link = f"https://jobmp3.ru/"

# music_info = []
# for i in range(1,4289):
#     print(i)
#     responce = requests.get(f'{link}music/page/{i}/').text
#     soup = BeautifulSoup(responce, "html.parser")
#     block = soup.find('div', class_='sect-content')
#     all_music = block.find_all('div', class_='track-item fx-row fx-middle js-item')

#     for music in all_music:
#         try:
#             music_name = music.get('data-title')
#             music_link = music.get('data-track')
#             x = music_name.split(' - ')
#             author = x[0]
#             name = x[1]

#             music_info.append([name, author, music_link])
#         except:
#             pass

engine = create_engine('sqlite:///data.db', echo=False)

# Bazaviy jadval objectini chaqirib olish
Base = declarative_base()

# Sessiyani hosil qilib olish
Session = sessionmaker(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = "AllMusic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    author = Column(String)
    link = Column(String)

    def __repr__(self):
        return f"{self.author}{self.name}{self.link}"

Base.metadata.create_all(engine)

# for x in range(len(music_info)):
#     session.add(Table(name = music_info[x][0],author = music_info[x][1],link =music_info[x][2]))


session.commit()