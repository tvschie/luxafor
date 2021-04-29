#!/bin/python3

import argparse
import luxafor
import time

def main():
    parser = argparse.ArgumentParser(description='Change Luxafor colour')
    parser.add_argument('color', choices=['green', 'yellow', 'red', 'blue', 'white', 'off'], help='color to change to')
    args = parser.parse_args()

    l = luxafor.LuxaFor()

    ## Normal working of script, set predefined color
    l.predefined_color(args.color)

    ## Example 1 Police Animation:
    # l.animate_police(10)

    ## Example 2 Set Custom Color:
    # l.set_color('#A7226E')
    # time.sleep(1)
    # l.set_color('#EC2049')
    # time.sleep(1)
    # l.set_color('#F26B38')
    # time.sleep(1)
    # l.set_color('#F7DB4F')
    # time.sleep(1)
    # l.set_color('#2F9599')


if __name__ == '__main__':
     main()

