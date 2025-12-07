"""Service layer for StudentClass operations."""
from app.repositories.registry import RepoRegistry, RepoName
from app.models.student_class import StudentClass
from app.utils.logger import logger


class StudentClassService:
    """Class providing services for StudentClass operations."""

    def __init__(self):
        return

    def get_all_classes(self):
        """Retrieve all student classes."""
        return RepoRegistry.get(RepoName.STUDENT_CLASS).get_all()

    def create_student_class(self, name, description, tutor, tuition_fee):
        """Create a new student class."""
        logger.info("Creating class: %s, %s, %s, %s",
                    name, description, tutor, tuition_fee)
        student_class = StudentClass(
            name=name, description=description, tutor=tutor, tuition_fee=tuition_fee)
        return RepoRegistry.get(RepoName.STUDENT_CLASS).insert(student_class)

    def delete_student_classes(self, class_ids):
        """Delete student classes by their IDs."""
        logger.info("Deleting classes with IDs: %s", class_ids)
        if not isinstance(class_ids, list):
            class_ids = [class_ids]
        return RepoRegistry.get(RepoName.STUDENT_CLASS).delete_by_ids(class_ids)

    def get_student_class(self, class_id):
        """Get student class from repository"""
        logger.info("Getting student class from database")
        return RepoRegistry.get(RepoName.STUDENT_CLASS).get_by_id(class_id)

    def edit_student_class(self, class_id, name=None, description=None, tutor=None, tuition_fee=None):
        """Edit an existing student class. Only provided fields will be updated."""
        logger.info("Editing student class ID %s with values: name=%s, description=%s, tutor=%s, tuition_fee=%s",
                    class_id, name, description, tutor, tuition_fee)

        repo = RepoRegistry.get(RepoName.STUDENT_CLASS)
        student_class = repo.get_by_id(class_id)

        if not student_class:
            logger.warning("Student class with ID %s not found.", class_id)
            return None  # or raise an exception

        # Update only provided fields
        if name is not None:
            student_class.name = name
        if description is not None:
            student_class.description = description
        if tutor is not None:
            student_class.tutor = tutor
        if tuition_fee is not None:
            student_class.tuition_fee = tuition_fee

        # Save changes
        return repo.update(student_class)
