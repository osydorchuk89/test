# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants


Test task
"""
# TODO Import the necessary libraries


# TODO Write here is_palindrome function 

def is_palindrome(string):
    if type(string) == str:
        string = ''.join(char for char in string if char.isalnum()).lower()
        return string == string[::-1]
    else:
        return False
