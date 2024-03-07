import check
if __name__ == '__main__':
    with open('urls.txt', 'r') as file:
        urls = file.read().splitlines()
    check.start(urls)
