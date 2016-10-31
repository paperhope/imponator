#!/usr/bin/python3
import json
import requests

url = "http://localhost:5000/item"

def whats_done():
    answer = dict()
    answer["Who"] = input("Who did the thing?\n")
    answer["What"] = input("What is the thing?\n")
    answer["Why"] = input("Why did you do the thing?\n")

    return answer


def send_answer(answer):
    #print(answer)
    r = requests.post(url, json=answer)
    
if __name__ == "__main__":
    answer = whats_done()
    send_answer(answer)
