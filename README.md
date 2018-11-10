# python scraping

### BeautifulSoup

```python=
bs = BeautifulSoup(html.read(), 'html.parser')
```

```python=
# like indexOf()
# same with find_all(limit=1)
bs.find(tag, attributes, recursive, text, limit, keywords)

bs.find_all(tag, attrbutes, recursive, text, keywords)
```

```python=
get_text() # get in tag text
.children() # 所有子節點
.parent() # 父節點
next_siblings() #下一個
previous_siblings() #上一個
tag.attrs['src'] # get attrbutes

```

### Regular Expression (regex)


| Column 1 | Column 2 |
| -------- | -------- | 
| *     | 任何數量的上個字元包括0個|
 |(cc)* | 偶數次出現cc，記得包括0次|
 |(d\|e)| d 或 e 都可以 |
 
 

| Column 1 | Column 2 | Column 3 | Column 4 |
| -------- | -------- | -------- | -------- |
| *     | 符合前一個字元、表示式或方括弧字元集合，出現零次或多次     | a\*b\*     | aaaaaaa, aaaabbbb, bbbbbb     |
|+|符合前一個字元、表示式或方括弧字元集合，出現一次或多次|a+b+| aaaaaaab, aaabbbbbb, abbbbbbb|
|[ ]|符合括號內任一字元(也就是裡面字元隨便一個)|[A-Z]*|APPLE, CAPITALS, CAT|
|( )|子表示式群組(正規表達式評價順序之內會優先處理)|(a\*b)\*|aaabaab, abaaab, ababaaaaab|
|{m,n}|符合前一個字元、表示式或方括弧字元集合，出現 m 到 n 次(包含 m 與 n )|a{2,3}b{2,3}|aabbb, aaabbb, aabb|
|[^]|符合任何一個不在括號內的字元|[^A-Z]\*|apple, lowercase, qwerty|
|\||等於邏輯運算子 or|b(a\|i\|e)d|bad, bid, bed|
|.|符合任何單一字元(包含符號、數字、空格等)|b.d|bad, bzd, bcd|
|^|代表一個字元或子表達式出現在字串開頭|^a|apple, asdf, a|
|\\|跳脫字元|None|None|
|\$|常放在最後代表字串結尾。沒有他的話最後都像加了" .\* "|[A-Z]\*[a-z]\*\$|ABCabc, zzzyx, Bob|
|?!|不包含。|^((?![A-Z]).)\*$|no-caps-here, $ymb01s a4e f!ne|




```python=
# lambda tag: len(tag.attrs) == 2 其為 True find_all() 會回傳該標籤
bs.find_all(lambda tag: len(tag.attrs) == 2) # 找出所有 attributes 等於 2 的tag

```