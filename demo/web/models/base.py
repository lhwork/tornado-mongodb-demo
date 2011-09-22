from mongokit import Document

class BaseDocument(Document):
    use_dot_notation = True
    dot_notation_warning = True

