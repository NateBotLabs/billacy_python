# app/services/user_service.py
from app.repositories.registry import RepoName, RepoRegistry
from app.utils.logger import logger
from app.models.user import User


class UserService:
    def __init__(self):
        return

    def get_all_users(self):
        return RepoRegistry.get(RepoName.USER).get_all()

    def create_user(self, first_name, last_name, email, class_id):
        user = User(first_name=first_name, last_name=last_name,
                    email=email, class_id=class_id)
        return RepoRegistry.get(RepoName.USER).insert(user)

    def edit_user(self, first_name,  last_name, email, class_id, user_id):
        """Edit an existing student. Only provided fields will be updated."""

        logger.info("Updating student with First name %s Last Name %s email address %s class id %s", first_name, last_name, email, class_id)
        repo = RepoRegistry.get(RepoName.USER)
        student = repo.get_by_id(user_id)

        if not student:
            logger.warning("Student with ID %s not found.", user_id)
            return None  # or raise an exception

        if first_name is not None:
            student.first_name = first_name
        if last_name is not None:
            student.last_name = last_name
        if email is not None:
            student.email = email
        if class_id is not None:
            student.class_id = class_id
        
        return repo.update(student)

    
    def delete_user(self, user_ids):
        """Delete student classes by their IDs."""
        logger.info("Deleting classes with IDs: %s", user_ids)
        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        return RepoRegistry.get(RepoName.USER).delete_by_ids(user_ids)