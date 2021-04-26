# FRAKE: Fusional Real-time Automatic Keyword Extraction
This package is a Fusional Real-time method keyword extraction on text extracted from single documents to select the most important keywords of a text. Our method consists of a combination of two models: graph centrality features and textural features. The proposed method has been used to extract the best keyword among the candidate keywords with an optimal combination of graph centralities, such as degree, betweenness, eigenvector, and closeness centrality, and textural, such as Casing, Term position, Term frequency normalization, Term different sentence, Part Of Speech tagging. There have also been attempts to distinguish keywords from candidate phrases and consider them on separate keywords. In addition to the python package here described, we also make available a [web app](https://kw.zehtab.ir/)



## Installation
 you can install this package using pip
  ```
  $ pip install FRAKE-extractor
  ```

## How to use
you can use very simply 😀
```python
import FRAKE

text = "Google is acquiring data science community Kaggle. Sources ..."

kw = FRAKE.KeywordExtractor(lang='en',hu_hiper=0.4,Number_of_keywords=10)

print(kw.extract_keywords(text))
>>>  {'kaggle': 29.4,
        'google': 22.04,
        'data science machine competitions': 13.11,
        'Google acquiring data science Kaggle': 10.86,
        'data community': 8.33,
        'data': 5.72,
        'service running': 5.62,
        'platform': 3.86,
        'service': 3.79,
        'sources': 2.9}
```
or you can run [example.ipynb](https://github.com/AidinZe/FRAKE/tree/main/example) file
