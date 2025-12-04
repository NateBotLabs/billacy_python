"""Repository for User model, inherits generic CRUD from BaseRepository."""
from app.models.student_class import StudentClass
from .base import BaseRepository


class StudentClassRepository(BaseRepository):
    """Repository for StudentClass model, inherits generic CRUD from BaseRepository."""

    def __init__(self):
        super().__init__(StudentClass)

    def delete_by_ids(self, class_ids):
        """Delete multiple StudentClass records by their IDs."""
        session = self.session
        try:
            session.query(self.model_class).filter(self.model_class.id.in_(
                class_ids)).delete(synchronize_session='fetch')
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
