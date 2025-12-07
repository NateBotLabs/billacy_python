# tests/services/test_invoice_service.py
from tests.base_test import *
from app.services.student_class_service import StudentClassService


class TestStudentClassService(BaseTest):

    def setup_method(self):
        self.service = StudentClassService()

    def test_create_student_class(self):
        name = "Primary One"
        description = "Ages from 9-10"
        tutor = "Mr Nathan"
        tuition_fee = 50000

        self.service.create_student_class(
            name, description, tutor, tuition_fee)

        saved_class = RepoRegistry.get(
            RepoName.STUDENT_CLASS).get_first_item()
        assert saved_class is not None
        assert saved_class.name == name
        assert saved_class.description == description
        assert saved_class.tutor == tutor
        assert saved_class.tuition_fee == tuition_fee

    def test_get_student_class(self):
        created_student_class = StudentClassFactory()

        repo_call = self.service.get_student_class(created_student_class.id)

        assert created_student_class is not None
        assert repo_call is not None
        assert created_student_class == repo_call
    
    def test_edit_student_class(self):
        created_student_class = StudentClassFactory()

        self.service.edit_student_class(created_student_class.id)

    def test_delete_student_classes(self):
        created_student_class = StudentClassFactory()

        self.service.delete_student_classes(created_student_class.id)
        repo_call = self.service.get_student_class(created_student_class.id)

        assert repo_call is None
    