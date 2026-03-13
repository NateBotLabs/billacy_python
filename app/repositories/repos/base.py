"""Base repository with generic CRUD operations."""

from app.connection.setup import DatabaseSetup


class BaseRepository:
    """Generic CRUD operations for all models."""

    def __init__(self, model_class):
        self.model_class = model_class
        self.session = DatabaseSetup.get_session()

    def get_all(self, filter=None):
        """Retrieve all records of the model."""
        query = self.session.query(self.model_class)
        if filter is not None:
            query = query.filter(filter)
        return query.all()

    def get_by_id(self, pk):
        """Retrieve a record by its ID."""
        return self.session.get(self.model_class, pk)

    def get_first_item(self):
        """Get one item from the """
        return self.session.query(self.model_class).first()

    def get_latest(self, condition_field, order_by_field):
        """Get the latest record based on a condition field."""
        return self.session.query(self.model_class).filter(condition_field).order_by(order_by_field.desc()).first()

    def delete_by_ids(self, pks):
        """Delete multiple StudentClass records by their IDs."""
        session = self.session
        try:
            session.query(self.model_class).filter(self.model_class.id.in_(
                pks)).delete(synchronize_session='fetch')
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def insert(self, obj):
        """Insert a new record into the database."""
        try:
            self.session.add(obj)
            self.session.commit()
            # optional, ensures obj has updated fields (like auto-generated id)
            self.session.refresh(obj)
            return obj
        except Exception as e:
            self.session.rollback()
            raise e

    def bulk_insert(self, data_list):
        """Bulk insert multiple records using mappings (dicts) without loading into memory.

        Args:
            data_list (list): List of dictionaries with column values.

        Returns:
            None
        """
        if not data_list:
            return
        try:
            self.session.bulk_insert_mappings(self.model_class, data_list)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, obj):
        """Delete a record from the database."""
        try:
            self.session.delete(obj)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, obj):
        """Commit changes to a record in the database."""
        try:
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except Exception as e:
            self.session.rollback()
            raise e
