import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import time

keyword = '實習 intern'
pages = range(1, 151)

# 迴圈搜尋結果頁數
outputDf = pd.DataFrame()
for page in pages:
    payload = {}
    headers = {
        'Cookie': 'ALGO_EXP_12509=G; ALGO_EXP_6019=B; TS016ab800=01180e452dfa63747ce99dd5c2b4a4bb2bc66583e690ad73f27a9af6c3bf67543536e1bf8f9c2a58eb0f3feb73e1ae083fc732196927a8782982276514379bf905ecf4ea09cf0fd73d82ff62e7f5d58fdd5a741fab'
    }
    url = f"https://www.104.com.tw/jobs/search/?ro=0&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&order=14&asc=0&page={page}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
    r = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(r.text, 'lxml')

    # 取得搜尋返回結果
    jobList = soup.select('article.b-block--top-bord')
    # 取得職缺公布時間
    jobAnnounceDate = [elem.select(
        'span.b-tit__date')[0].text.replace('\n', '').strip() for elem in jobList]
    # 取得職缺名稱
    jobTitles = [elem.select('a.js-job-link')[0].text for elem in jobList]
    # 取得職缺公司名稱
    jobCompanyName = [elem.select('a')[1].text.replace(
        '\n', '').strip() for elem in jobList]
    # 取得職缺公司頁面資訊連結
    jobCompanyUrl = ['https:' +
                     elem.select('a')[1]['href'] for elem in jobList]
    # 取得職缺公司所屬產業類別
    jobCompanyIndustry = [elem.select('li')[2].text for elem in jobList]
    # 取得待遇資訊
    jobSalary = [elem.select('div.job-list-tag.b-content')
                 [0].select('span')[0].text for elem in jobList]

    # 整理其他工作資訊(工作地點, 年資要求, 學歷要求)
    jobOtherInfo = [elem.select(
        'ul.b-list-inline.b-clearfix.job-list-intro.b-content')[0] for elem in jobList]
    # 取得工作地點
    jobLocation = [elem.select('li')[0].text for elem in jobOtherInfo]
    # 取得年資要求
    jobRqYear = [elem.select('li')[1].text for elem in jobOtherInfo]
    # 取得學歷要求
    jobRqEducation = [elem.select('li')[2].text for elem in jobOtherInfo]

    # 取得職缺網址資訊
    jobDetailUrl = ['https:' + elem.select('a')[0]['href'] for elem in jobList]
    # 迴圈職缺網址資訊取得更詳細資訊
    jobContent = list()
    jobCategory = list()
    jobRqDepartment = list()
    jobSpecialty = list()
    jobOthers = list()
    for i, iJobDetailUrl in enumerate(jobDetailUrl):
        time.sleep(0.5)
        print(f"第{page}頁：第{i}個職缺")
        # 詳細資訊需透過額外的ajax爬取
        iUrl = 'https://www.104.com.tw/job/ajax/content/' + \
            re.search('job/(.*)\?', iJobDetailUrl).group(1)

        # 設定header
        headers = {
            'Referer': iJobDetailUrl,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                          '(KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
        }

        r = requests.request("GET", iUrl, headers=headers, data=payload)

        # 取得網頁資料
        response = r.json()
        response.get('error')

        # 取得工作內容
        jobContent = response['data']['jobDetail']['jobDescription']
        '   '.join(jobContent.split('\n'))
        # 取得職務類別
        jobCategory = ','.join(
            [elem['description'] for elem in response['data']['jobDetail']['jobCategory']])

        # 取得科系要求
        jobRqDepartment = ','.join(response['data']['condition']['major'])
        # 取得擅長工具
        jobSpecialty = ','.join(
            [elem['description'] for elem in response['data']['condition']['specialty']])
        # 取得其他條件
        jobOthers = response['data']['condition']['other']
        '  '.join(jobOthers.split('\n'))

    # 組合資訊成資料表並儲存
    # 組合資訊成資料表並儲存
    iOutputDf = pd.DataFrame({'jobAnnounceDate': jobAnnounceDate,
                              'jobTitles': jobTitles,
                              'jobCompanyName': jobCompanyName,
                              'jobCompanyUrl': jobCompanyUrl,
                              'jobCompanyIndustry': jobCompanyIndustry,
                              'jobContent': jobContent,
                              'jobCategory': jobCategory,
                              'jobSalary': jobSalary,
                              'jobLocation': jobLocation,
                              'jobRqYear': jobRqYear,
                              'jobRqEducation': jobRqEducation,
                              'jobRqDepartment': jobRqDepartment,
                              'jobSpecialty': jobSpecialty,
                              'jobOthers': jobOthers,
                              'jobDetailUrl': jobDetailUrl})
    outputDf = pd.concat([outputDf, iOutputDf])

# 刪除jobAnnounceDate為空值之列(代表該筆資料屬於104廣告職缺 與搜尋職缺較不相關)
outputDf = outputDf[outputDf.jobAnnounceDate != '']

# 輸出csv檔案
now = datetime.datetime.now()
fileName = now.strftime('%Y%m%d%H%M%S') + '104人力銀行_' + keyword + '_爬蟲搜尋結果.csv'
outputDf.to_csv(fileName, encoding='utf-8-sig', index=False)
