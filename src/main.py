from driver import driver

if __name__ == '__main__':
    driverInst = driver()
    lines = ["a sample", "a sample line", "sample line. and more"]
    for line in lines:
        print(driverInst.drive(line)[0])