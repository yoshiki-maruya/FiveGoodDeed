import os
import json
from model.sentence_list import SentenceList

def get_json_data() -> SentenceList:
    json_open = open('english_data.json', 'r')
    json_data = json.load(json_open)
    sentence_list = SentenceList(sentences=json_data)
    return sentence_list
  
def main():
    json_data = get_json_data()
    print(json_data.sentences[0].no)

if __name__ == "__main__":
    main()
  