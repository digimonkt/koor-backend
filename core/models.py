from datetime import date

def upload_directory_path(instance, filename):
    """
    Directory path function: Return unique path name for file uploading.
    Example:- YYYT-MM-DD/instance_name/file_name
    """
    return '{0}/{1}/{2}'.format(date.today(), instance, filename)
