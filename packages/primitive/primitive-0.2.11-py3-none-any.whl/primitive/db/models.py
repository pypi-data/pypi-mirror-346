from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, Query
from typing import Optional, Generic, TypeVar, Callable, Type, List, Union, Dict, Any
from .sqlite import Session
from .base import Base

T = TypeVar("T", bound="Base")


class Manager(Generic[T]):
    def __init__(self, model_cls_lambda: Callable[[], Type[T]]) -> None:
        self.model_cls_lambda = model_cls_lambda
        self.filters: Dict[str, Any] = {}

    def create(self, **kwargs) -> T:
        with Session() as session:
            model = self.model_cls_lambda()
            obj = model(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def filter_by(self, **kwargs) -> "Manager[T]":
        self.filters = kwargs
        return self

    def all(self) -> List[T]:
        with Session() as session:
            model = self.model_cls_lambda()
            query = session.query(model)
            query.filter_by(**self.filters)
            self.filters.clear()
            return query.all()

    def first(self) -> Union[T, None]:
        with Session() as session:
            model = self.model_cls_lambda()
            query = session.query(model)
            query.filter_by(**self.filters)
            self.filters.clear()
            return query.first()

    def update(self, update: Dict[Any, Any]) -> Query[T]:
        with Session() as session:
            model = self.model_cls_lambda()
            query = session.query(model).filter_by(**self.filters)

            if query.count() > 0:
                query.update(update)
                session.commit()
                return query
            else:
                raise ValueError(f"{model.__name__} not found")

    def delete(self) -> None:
        with Session() as session:
            model = self.model_cls_lambda()
            query = session.query(model).filter_by(**self.filters)

            if query.count() > 0:
                query.delete()
                session.commit()
            else:
                raise ValueError(f"{model.__name__} not found")


class JobRun(Base):
    __tablename__ = "JobRun"

    id = Column(Integer, primary_key=True)
    job_run_id: Mapped[str] = mapped_column(String, nullable=False)
    pid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    objects: Manager["JobRun"] = Manager(lambda: JobRun)

    def __repr__(self):
        return f"<JobRun(id={self.id} job_run_id={self.job_run_id}, pid={self.pid})>"
