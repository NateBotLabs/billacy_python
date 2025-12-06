"""Service layer for StudentClass operations."""
from app.repositories.repos.student_class_repository import StudentClassRepository
from app.models.student_class import StudentClass
from app.utils.logger import logger

"""Class providing services for StudentClass operations."""
class StudentClassService:
    def __init__(self):
        self.student_class_repo = StudentClassRepository()

    def get_all_classes(self):
        """Retrieve all student classes."""
        return self.student_class_repo.get_all()

    def create_class(self, name, description, tutor, tuition_fee):
        """Create a new student class."""
        logger.info("Creating class: %s, %s, %s, %s",
                    name, description, tutor, tuition_fee)
        student_class = StudentClass(
            name=name, description=description, tutor=tutor, tuition_fee=tuition_fee)
        return self.student_class_repo.insert(student_class)

    def delete_student_class(self, class_ids):
        """Delete student classes by their IDs."""
        logger.info("Deleting classes with IDs: %s", class_ids)
        return self.student_class_repo.delete_by_ids(class_ids)
