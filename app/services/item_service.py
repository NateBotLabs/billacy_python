"""Service layer for Item operations."""
from app.repositories.registry import RepoRegistry, RepoName
from app.models.item import Item
from app.utils.logger import logger


class ItemService:
    """Class providing services for Item operations."""

    def __init__(self):
        return

    def get_all_items(self):
        """Retrieve all non-deleted items."""
        return RepoRegistry.get(RepoName.ITEM).get_all(
            filter=(Item.deleted == False)
        )

    def create_item(self, name, quantity, price):
        """Create a new item."""
        logger.info(
            "Creating item: name=%s, quantity=%s, price=%s",
            name, quantity, price
        )

        item = Item(
            name=name,
            quantity=quantity,
            price=price
        )
        return RepoRegistry.get(RepoName.ITEM).insert(item)

    def delete_items(self, item_ids):
        """
        Soft-delete items by IDs.
        """
        logger.info("Soft deleting items with IDs: %s", item_ids)

        if not isinstance(item_ids, list):
            item_ids = [item_ids]

        repo = RepoRegistry.get(RepoName.ITEM)
        for item_id in item_ids:
            item = repo.get_by_id(item_id)
            if item:
                item.deleted = True
                repo.update(item)

    def get_item(self, item_id):
        """Get item by ID."""
        logger.info("Getting item ID %s", item_id)
        return RepoRegistry.get(RepoName.ITEM).get_by_id(item_id)

    def edit_item(self, item_id, name=None, quantity=None, price=None):
        """Edit an existing item."""
        logger.info(
            "Editing item ID %s with values: name=%s, quantity=%s, price=%s",
            item_id, name, quantity, price
        )

        repo = RepoRegistry.get(RepoName.ITEM)
        item = repo.get_by_id(item_id)

        if not item or item.deleted:
            logger.warning("Item with ID %s not found or deleted.", item_id)
            return None

        if name is not None:
            item.name = name
        if quantity is not None:
            item.quantity = quantity
        if price is not None:
            item.price = price

        return repo.update(item)
