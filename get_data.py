from re import T
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
#     session.add(Table(name = music_info[x][0], author = music_info[x][1], link = music_info[x][2]))


session.commit()