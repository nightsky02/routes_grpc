from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String
from services.routes.db.base_settings import engine


class Base(DeclarativeBase):
    pass


class Route(Base):
    __tablename__ = "routes"


    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(nullable=False)
    number: Mapped[int]
    start_point: Mapped[str] = mapped_column(String(100), nullable=False)
    end_point: Mapped[str] = mapped_column(String(100), nullable=False)
    stop_id: Mapped[int] = mapped_column(nullable=False)


Base.metadata.create_all(engine)