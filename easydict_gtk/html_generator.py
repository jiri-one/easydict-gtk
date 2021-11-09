import difflib
import re
# imports from my other files with classes and methods
from .settings import cwd, cwd_images, eng_cze, where

def db_search(language, text, fulltext):
    if fulltext == False: 
        text = rf'\b{text}\b'
    results = eng_cze.search(where(language).search(text, flags=re.IGNORECASE))
    results_with_matchratio = []
    for result in results:
        ratio = difflib.SequenceMatcher(None, result[language], text).ratio()
        results_with_matchratio.append([result, ratio])
    return sorted(results_with_matchratio, key=lambda x: x[1], reverse=True)

class CreateHtml:
    def __init__(self):
        self.default_html = f"""
        <!DOCTYPE html>
        <html>
        <body style="background-color:#2d2d2d;", oncontextmenu="return false">
        <p style="font-size: 22px;text-align:center;"><b><span style="color: #ffffff;">Welcome to EasyDict</span></b></p>
        <p style="text-align:center;"><img src="{str(cwd_images / "ed_icon.png")}"></p>
        <p style="font-size: 22px;text-align:center;"><span style="color: #ffffff;">The first open source translator which is completely open with dictionary data too.</span></p>
        </body>
        </html>"""    
    
    def __call__(self, results, language):
        self.language = language
        self.second_language = [lang for lang in ["cze", "eng"] if lang != language][0]
        html_string = """
        <!DOCTYPE html>
        <html>
        <body style="background-color:#2d2d2d;", oncontextmenu="return false">
        """        
        for row in results:
            html_string = html_string + self.create_html(row[0])
        html_string = html_string + """
        </body>
        </html>
        """
        return html_string
    
    def create_html(self, row):
        """Create html code for one row."""
        if "notes" in row.keys():
            self.notes =  ", " + row["notes"]
        else:
            self.notes = ""
        if "special" in row.keys():
            self.special = ", "  + row["special"]
        else:
            self.special = ""
       
    
        html = f"""
        <p style="font-size: 22px"><b><span style="color: #ffffff;">{row[self.language]}</span></b>
        <br>&emsp;<span style="color: #ffffff;">{row[self.second_language]}{self.notes}{self.special}</span>
        </p>
        """
        return html

#vystup = CreateHtml(mydoc)
#print(vystup)

#html = f"""
#<p style="font-size: 22px"><b>{row["eng"]}</b>
#<br>&emsp;{row["cze"]}
#&emsp;{row["notes"]}
#&emsp;{row["special"]}</p>"""