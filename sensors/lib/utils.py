import base64

__all__ = [
    'create_file_base64'
]

def create_file_base64(contents, file_name):
    """
    Create a file with the base64 encoded parameter contents and return the file name

    :param contents: base64 encoded file contents
    :type contents: ``str``
    :param file_name: file name
    :type fulename: ``str``

    :return: file name
    :rtype: ``str``
    """
    if contents == None:
        return None
    file = open(file_name, 'w')
    file.write(base64.b64decode(contents).decode('utf-8'))
    file.close()
    return file_name
