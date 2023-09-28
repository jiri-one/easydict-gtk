from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from orjson_storage import ORJSONStorage
import difflib
import re

db = TinyDB("eng-cze.json", storage=CachingMiddleware(ORJSONStorage))
eng_cze = db.table("eng_cze")
MyQuery = Query()
whole_word = eng_cze.search(MyQuery.eng.search(r"\bshit\b", flags=re.IGNORECASE))
print(len(whole_word))
fulltext = eng_cze.search(MyQuery.eng.search("shit", flags=re.IGNORECASE))
print(len(fulltext))
# for x in whole_word:
# print(x)

whole_word_with_matchratio = []
for result in whole_word:
    ratio = difflib.SequenceMatcher(None, result["eng"], r"shit").ratio()
    # whole_word_with_matchratio.append(result.append("ratio": ratio))
    whole_word_with_matchratio.append([result, ratio])

print(sorted(whole_word_with_matchratio, key=lambda x: x[1], reverse=True))
