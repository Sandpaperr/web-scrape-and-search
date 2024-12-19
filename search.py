import re

from tabulate import tabulate
from terminal_commands import build, find, command_print, load
from global_variables import *
from pathlib import Path
from general import is_nonempty_json_file

"""
build
This command instructs the search tool to crawl the website, 
build the index, and save the resulting index intothe file system. 
For simplicity you can save the entire index into one file.

load
This command loads the index from the file system. Obviously, 
this command will only work if the index has previously been created using 
the ‘build’ command.

print
This command prints the inverted index for a particular word, 
for example:print nonsensewill print the inverted index for the word 
‘nonsense.’

find
This command is used to find a certain query phrase in the inverted 
index and returns a list of all pagescontaining this phrase, for example:find indifferencewill 
return a list of all pages containing the word ‘indifference, while
find good friendswill return all pages containing the words ‘good and ‘friends.
"""

COMMANDS_TO_PRINT = [
            ("build", "(first command to use) crawl the website and create the file with the index."),
            ("load", "(second command to use) load the index file into the software as a dictionary"),
            ("print word", "(after load) prints all the positions of the word 'word' in each URL"),
            ("find query", "(after load) search the word or string amongst all the URL, score them and print them in order"),
            ("show", "print again all the available commands and descriptions"),
            ("quit", "Quit the program.")
        ]

# print formatted command description
for command, description in COMMANDS_TO_PRINT:
    print(f"{command:<15} {description}")

build_flag = False
load_flag = False
inverted_index = {}
while True:

    # check if build is needed 
    if is_nonempty_json_file(INVERTED_INDEX_FILE):
        build_flag = True

    user_prompt = input("Insert command: ").lower()

    words = user_prompt.split()


    if len (words) != 0:

        if words[0] == "build":
            build()
            build_flag = True
            load_flag = False


        elif words[0] == "load" and build_flag:
            index_file_path = Path(INVERTED_INDEX_FILE)
            if index_file_path.exists():
                inverted_index = load()
                if len(inverted_index) == 0:
                    print ("index is empty, try building first")
                else:
                    print("Load completed. You can now use all the other commands")
                    load_flag = True
            else:
                print("index file not found")

        elif words[0] == "print" and load_flag:

            if len(words) == 2:

                sanitized_text = re.sub(r"[^a-zA-Z0-9\s]", "", words[1])

                token_stats = command_print(inverted_index, sanitized_text)
                if token_stats:
                    
                    data = [(page, ', '.join(map(str, positions))) for page, positions in token_stats.items()]

                    # check if positions str is too long, if it is, split it     
                    for i in range(len(data)):
                        page, positions = data[i]
                        if len(positions) > 30:
                            positions_list = positions.split(', ')
                            new_positions = ''
                            line_length = 0                           
                            for position in positions_list:
                                if line_length + len(position) + 2 > 30:  # Check if adding position would exceed 30 characters
                                    new_positions += '\n'  # Add newline character
                                    line_length = 0
                                new_positions += position + ', '  # Add position and comma
                                line_length += len(position) + 2
                            data[i] = (page, new_positions[:-2])  # Remove trailing comma and space
                    
                    splitted_data = []
                    while len(data) > 0:
                        if len(data) > 40:
                            splitted_data.append(data[:40])
                            data = data[40:]
                        else:
                            splitted_data.append(data)
                            data = []
                    
                    print(f"Chosen word: {sanitized_text}")

                    for data_formatted in splitted_data:
                        print(tabulate(data_formatted, headers=["Rank", "URL"], tablefmt="heavy_grid"))
                else:
                    print(f"word '{sanitized_text}' not found in the index")
            else:
                print("Invalid command. Usage: 'print token'. Only one word after 'print' is allowed")


        elif words[0] == "find" and load_flag:

            query = " ".join(words[1:])
            result_list = find(inverted_index, query)

            if result_list:
                # create tuples for tabulate
                data = [(i + 1, page) for i, page in enumerate(result_list)]
                
                splitted_data = []
                while len(data) > 0:
                    if len(data) > 40:
                        splitted_data.append(data[:40])
                        data = data[40:]
                    else:
                        splitted_data.append(data)
                        data = []
            
                
                if len(splitted_data) == 0:
                    print(f"No URLs from the index contain the word(s) '{query}'")
                else:
                    for data_formatted in splitted_data:
                        print(tabulate(data_formatted, headers=["Rank", "URL"], tablefmt="heavy_grid"))
 
                
            



        elif user_prompt == "show":
            for command, description in COMMANDS_TO_PRINT:
                print(f"{command:<15} {description}")

        elif user_prompt == "quit":
            break

        else:
            print("Command not valid, try again.")
            print( "Make sure you build first then load and only after that you can use the other commands")
            print()

 