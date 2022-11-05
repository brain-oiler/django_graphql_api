
def document_file_validator(value):
    import os
    from django.core.exceptions import ValidationError
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.xlsx', '.xls', '.txt']
    if not extension.lower() in valid_extensions:
        raise ValidationError(
            f"""Unsupported file extension {extension}\
            must be {valid_extensions}""")


def audio_file_validator(value):
    import os
    from django.core.exceptions import ValidationError
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.mtm', '.ec3']
    if not extension.lower() in valid_extensions:
        raise ValidationError(
            f"""Unsupported file extension {extension}\
            must be {valid_extensions}""")


def video_file_validator(value):
    import os
    from django.core.exceptions import ValidationError
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.mov', '.wmv', '.avi', '.mkv']
    if not extension.lower() in valid_extensions:
        raise ValidationError(
            f"""Unsupported file extension {extension}\
            must be {valid_extensions}""")
