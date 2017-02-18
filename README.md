# code2pdf

A script to build a PDF from a list of source files and a description.txt. This is useful for Doug Ferguson's classes at Johns Hopkins as he requires code to be submitted in PDF format. Feel free to fork and submit pull requests for any features you would like to see added. 

## Usage 

`python code2pdf.py path/to/config.json path/to/description.txt`

Script expects a config file `config.json` in the current directory, or one can be passed as the first argument. It makes the most sense to just have `config.json` and `description.txt` in the root of your project folder, and run the script from there.

### config.json

* A list of files in the order you want them to appear

* The path to a text file containing your description / design

* A heading to put your name, class, and date (date will be auto replaced)

```
{
    "files": [
        "cminus/lexer.mll",
        "cminus/ast.ml",
        "cminus/parser.mly",
        "cminus/codegen.ml",
        "cminus/main.ml",
        "cminus/samples/io.c",
        "cminus/samples/fact/fact.tny",
        "cminus/samples/fact/fact.ll",
        "cminus/README.md", 
        "cminus/_tags", 
        "code2pdf/code2pdf.py"
    ],
    "description_file": "description.txt",
    "heading": [
        "Douglas Gastonguay-Goddard",
        "Compiler Design - Ferguson",
        "[DATE]"
    ]
}
```

## Dependencies 

`pip install reportlab`