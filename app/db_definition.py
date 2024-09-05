from typing_extensions import Annotated
from typing import List, Optional, Dict, Any
from sqlalchemy import String, Float, ForeignKey, ARRAY, TEXT, INT, BOOLEAN
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.orm.exc import DetachedInstanceError

#table names
MANGA_TABLE_NAME = 'manga'
EPISODE_TABLE_NAME = 'episode'

# customized type overrides
str10 = Annotated[str, 5]
str36 = Annotated[str, 36]
str50 = Annotated[str, 50]
str200 = Annotated[str, 200]

# mapped column overrides
uuid_pk = Annotated[str, mapped_column(String(36), primary_key=True, nullable=False, unique=True)]

class Base(DeclarativeBase):
    type_annotation_map = {
        str10: String(10),
        str36: String(36),
        str50: String(50),
        str200: String(200),
    }

class Manga(Base):
    __tablename__ = MANGA_TABLE_NAME

    manga_id: Mapped[uuid_pk]
    manga_name: Mapped[str50] = mapped_column(nullable=False, unique=True)
    manga_link: Mapped[str200] = mapped_column(nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<Manga {self.manga_id}>'

class Episode(Base):
    __tablename__ = EPISODE_TABLE_NAME

    episode_id: Mapped[uuid_pk]
    manga_id: Mapped[str36] = mapped_column(ForeignKey('manga.manga_id'), nullable=False)
    episode_name: Mapped[str10] = mapped_column(nullable=False, unique=True)
    episode_link: Mapped[str200] = mapped_column(nullable=False, unique=True)
    episode_tag: Mapped[str10] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f'<Episode {self.episode_id}>'