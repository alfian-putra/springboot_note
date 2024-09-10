#!/usr/bin/python3

import os

ls = os.listdir()

for i in ls :
    if i.split(".")[-1]=="md":
        print(f"[]({i}) \n")