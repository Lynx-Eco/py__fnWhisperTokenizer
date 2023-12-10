def read_and_print_file():
    with open('test/data/inputs.txt', 'r') as file:
        for line in file:
            print(line.strip())

if __name__ == '__main__':
    read_and_print_file()