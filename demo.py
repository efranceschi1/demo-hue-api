from gethue import GetHue
import logging


def main():
    hue = GetHue()
    print(hue.execute_hive_sync("show databases"))
    print(hue.execute_hive_sync("show tables"))
    print(hue.execute_hive_sync("select * from sample_07"))


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    main()
