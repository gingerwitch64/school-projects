from platform import python_version

def main():
    pass

if __name__ == "__main__" and python_version().split(".")[0] >= 3 or python_version().split(".")[1] >= 10:
    main()
