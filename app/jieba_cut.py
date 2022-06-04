import numpy as np
import pandas as pd
import jieba


class Jieba_Cut():
    def __init__(self, df: pd.DataFrame, stopWord: str, userDict: str):
        self.df = df
        self.stopword = self._get_Stopwordslist(stopWord)
        jieba.load_userdict(userDict)
        jieba.case_sensitive = True

    def cut(self):
        self.Words = []
        for r in self.df.iterrows():
            _word = []
            r = r[1]
            jobContent = r['jobContent']
            jobOthers = r['jobOthers']
            jobCategory = r['jobCategory']
            _word.append('') if self._nan(jobContent) else self._jieba(
                _word, jobContent, self.stopword)
            _word.append('') if self._nan(jobOthers) else self._jieba(
                _word, jobOthers, self.stopword)
            _word.append('') if self._nan(jobCategory) else self._jieba(
                _word, jobCategory, self.stopword)
            self.Words.append('、'.join(_word))

        self.df['jiebaCut'] = self.Words
        return self.df

    def _get_Stopwordslist(self, filepath):
        stopwords = [line.strip() for line in open(
            filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def _nan(self, word: str) -> bool:
        if type(word) == type(1.5) and np.isnan(word):
            return True
        else:
            return False

    def _jieba(self, container: list, word: str, stopword: str) -> list:
        l = jieba.cut(word)
        for w in l:
            if w in stopword or w in ['\n', ' ']:
                continue
            else:
                container.append(w)
        return None

    def __repr__(self) -> str:
        print('Module for Jieba 104 project')
