import enum

class InvoiceStatus(enum.Enum):
    PENDING = 'pending'
    PAID = 'paid'
    OVERDUE = 'overdue'