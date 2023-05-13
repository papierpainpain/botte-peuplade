from os.path import getsize


def tailf(file_):
    """Each value is content added to the log file since last value return"""

    last_size = getsize(file_)

    while True:
        cur_size = getsize(file_)

        if (cur_size != last_size):
            f = open(file_, 'r')
            f.seek(last_size if cur_size > last_size else 0)
            text = f.read()
            f.close()
            last_size = cur_size
            yield text
        else:
            yield ""
