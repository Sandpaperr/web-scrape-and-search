(This project is being developed as an extension of the solution I created for the Web App module coursework at the University of Leeds. Building on the initial implementation, I am currently enhancing its functionality, design, and overall scope to create a more robust and polished application.)

a search tool that finds pages containing certain search terms in a website.

The search tool can:
1) Crawl the pages of a website.
2) Create an inverted index of all word occurrences in the pages of the website.
3) Allow the user to find pages containing certain search terms.


Usage:
1) set up the target website URL to crawl and other params in src/global_variables.py 
2) after running main.py the user will be prompted to insert one of the following commands in the terminal:
   - build:
       This command instructs the search tool to crawl the website, 
       build the index, and save the resulting index intothe file system. 
       For simplicity you can save the entire index into one file.
     
   - load:
       This command loads the index from the file system. Obviously, 
       this command will only work if the index has previously been created using 
       the ‘build’ command.
     
   - print:
       This command prints the inverted index for a particular word, 
       for example:print nonsensewill print the inverted index for the word 
       ‘nonsense.’
  
   - find:
      This command is used to find a certain query phrase in the inverted 
      index and returns a list of all pagescontaining this phrase, for example:find indifferencewill 
      return a list of all pages containing the word ‘indifference, while
      find good friendswill return all pages containing the words ‘good and ‘friends.
