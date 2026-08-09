from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .base_settings import engine


class Base(DeclarativeBase):
    pass

class TransportStop(Base):
    __tablename__ = "ts_stops"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False, unique=True)


    def __repr__(self) -> str:
        return f"TransportStop(id={self.id!r}, name={self.name!r})"


Base.metadata.create_all(bind=engine)
