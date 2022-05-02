if __name__ == "__main__":
    with open('1234 - corrupted.txt') as f:
        for i, s in enumerate(f):
            print(i, s)