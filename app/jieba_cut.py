import numpy as np
import pandas as pd
import jieba
import re
import json


class Jieba_Cut():
    def __init__(self, df: pd.DataFrame):
        self.df = df
        print("斷點6：?????????????????")
        import os
        print('第一層', os.listdir('.'))
        print('第二層', os.listdir('app'))
        print('第三層', os.listdir(r'app/doc'))
        self.jobD = json.load(
            open(r'app/doc/jobD.json', 'r', encoding='utf-8'))
        print("斷點7：?????????????????")
        jieba.case_sensitive = True

    def cut(self, stopWord: str, userDict: str):
        self.stopword = self._get_Stopwordslist(stopWord)
        jieba.load_userdict(userDict)
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

        self.df['jobType'] = self._category()  # 分類

        self.df['jiebaCut'] = self.Words

    def pd2frequency(self, filter: str):

        if filter == '':
            temp = self.df
        else:
            temp = self.df[self.df['jobType'].str.contains(filter) == True]
        container = {}
        for i in temp['jiebaCut'].values:
            row = i.split('、')
            for w in row:
                container[w] = container.get(w, 0) + 1

        freqTable = pd.DataFrame(
            {'Word': container.keys(), 'Values': container.values()})
        freqTable.sort_values('Values', ascending=False, inplace=True)
        return freqTable

    def getBarData(self, filter: str):
        twd = []
        twd_len = []
        freqTable = self.pd2frequency(filter)
        for i in freqTable['Word'].values:
            wd = re.findall('[\u4e00-\u9fa5]+', i)
            if len(wd) == 0:
                wd = ''
                twd_len.append(0)
            else:
                wd = wd[0]
                twd_len.append(len(wd))
            twd.append(wd)

        freqTable['twWord'] = twd
        freqTable['len'] = twd_len
        output = freqTable[(freqTable['twWord'] != '') & (freqTable['len'] == 2)][[
            'Word', 'Values']][:30].values.tolist()
        return ([i[0] for i in output], [i[1] for i in output])

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
            w = w.strip()
            if w in stopword or w in ['\n', ' ', '=', '\\', '|', '.', '/', '＝']:
                continue
            else:
                if len(re.findall('[\u4e00-\u9fa5\a-Z\0-9\-\_]+', w)) == 0:
                    continue
                container.append(w)
        return None

    def _category(self) -> list:
        row = ['' for i in range(len(self.df))]
        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['資訊工程']) == True) & (self.df['jobCategory'].str.contains('測試員') == False))[0]:
            row[i] += '、資訊工程'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['數據分析']) == True) | (self.df['jobContent'].str.contains('數據') == True) | (self.df['jobTitles'].str.contains('數據') == True))[0]:
            row[i] += '、數據分析'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['行銷企劃']) == True) & (self.df['jobCategory'].str.contains('技術|工程') == False))[0]:
            row[i] += '、行銷企劃'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['行政助理']) == True) & (self.df['jobCategory'].str.contains('技術|工程') == False))[0]:
            row[i] += '、行政助理'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['藝術設計']) == True) & (self.df['jobCategory'].str.contains('軟體設計|網頁設計|韌體設計|程式設計|IC設計|半導體|硬體') == False))[0]:
            row[i] += '、藝術設計'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['餐飲']) == True) & (self.df['jobCategory'].str.contains('軟體設計|網頁設計|韌體設計|程式設計') == False))[0]:
            row[i] += '、餐飲'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['服務']) == True) & (self.df['jobCategory'].str.contains('軟體設計|網頁設計|韌體設計|程式設計') == False))[0]:
            row[i] += '、服務'

        for i in np.where((self.df['jobCategory'].str.contains(self.jobD['技術與操作']) == True) & (self.df['jobCategory'].str.contains('軟體設計|網頁設計|韌體設計|程式設計|工程') == False))[0]:
            row[i] += '、技術與操作'

        for i in np.where(((self.df['jobCategory'].str.contains(self.jobD['教育']) == True) & (self.df['jobCategory'].str.contains('軟體設計|網頁設計|韌體設計|程式設計|工程') == False) |
                           ((self.df['jobTitles'].str.contains('國中|高中|雙語|幼稚園|課後|學校|教職|家教|課業') == True) & (self.df['jobTitles'].str.contains('專案|企劃|行銷|產品|清潔|') == False))))[0]:
            row[i] += '、教育'

        return [i[1:] for i in row]

    def __repr__(self) -> str:
        print('Module for Jieba 104 project')
