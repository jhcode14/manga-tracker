from typing_extensions import Annotated
from sqlalchemy import ForeignKey, UUID, Text, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship

import uuid

# table names
MANGA_TABLE_NAME = "manga"
EPISODE_TABLE_NAME = "episode"

# mapped column overrides
uuid_pk = Annotated[
    str,
    mapped_column(
        UUID, primary_key=True, nullable=False, unique=True, default=uuid.uuid4
    ),
]


class Base(DeclarativeBase):
    type_annotation_map = {
        uuid.UUID: UUID(as_uuid=True),
        str: Text,
    }


class Manga(Base):
    __tablename__ = MANGA_TABLE_NAME

    manga_id: Mapped[uuid_pk]
    manga_name: Mapped[str] = mapped_column(Text, nullable=False)
    manga_link: Mapped[str] = mapped_column(Text, nullable=False)
    manga_pfp_loc: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("manga_name", "manga_link", name="uq_manga_name_link"),
    )

    # Declare relationship w/ it's episodes (cascade delete)
    episodes: Mapped[list["Episode"]] = relationship(
        "Episode", back_populates="manga", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Manga {self.manga_id}>"


class Episode(Base):
    __tablename__ = EPISODE_TABLE_NAME

    episode_id: Mapped[uuid_pk]
    manga_id: Mapped[str] = mapped_column(ForeignKey("manga.manga_id"), nullable=False)
    episode_name: Mapped[str] = mapped_column(Text, nullable=False)
    episode_link: Mapped[str] = mapped_column(Text, nullable=False)
    episode_tag: Mapped[str] = mapped_column(Text)
    episode_date_added: Mapped[str] = mapped_column(Text)
    episode_chapter_number: Mapped[int] = mapped_column(Integer)

    manga: Mapped[Manga] = relationship("Manga", back_populates="episodes")

    def __repr__(self) -> str:
        return f"<Episode {self.episode_id}>"
