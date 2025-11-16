from etl.load import load_to_s3 as m


def main():
    print('Module file:', getattr(m, '__file__', '<unknown>'))
    print('upload_file docstring:\n', m.upload_file.__doc__)


if __name__ == '__main__':
    main()
