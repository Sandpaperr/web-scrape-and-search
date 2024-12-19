""" TODO: this index starts from the file, 
the one I need starts from a string probably. 
I need to either pass the soup (recommended)
or the soup.text
"""
def index_text_file(file):
    d = dict()
    for line in file:
        words = line.lower().strip().split(" ")
        for word in words:
            if word == "":
                continue
            if word in d:
                d[word] = d[word] + 1
            else:
                d[word] = 1
    
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))


file_test = "test.txt"

text = open(file_test, "r")
print(index_text_file(text))