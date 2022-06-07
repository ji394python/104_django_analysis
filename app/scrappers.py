import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


class Scrape_104():

    def __init__(self, keyword: str, maxPage: int):
        self.keyword = keyword
        self.maxPage = maxPage

    def _checkConnect(self, url, headers):
        '''
            check crawler status
        '''
        try:
            response = requests.get(url, headers=headers)
            checkSuccess = True
            return response, checkSuccess
        except Exception as e:
            print('下載失敗!')
            response = None
            checkSuccess = False
            return response, checkSuccess

    def scrape(self):
        outputDf = pd.DataFrame()

        # Crawler Start
        for page in range(1, self.maxPage+1):

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                '(KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
            }

            url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=' + self.keyword + \
                '&expansionType=area,spec,com,job,wf,wktm&order=14&asc=0&page=' + \
                str(page) + '&mode=s&jobsource=2018indexpoc'

            # Parameter
            # keyword: 搜尋關鍵字
            # isnew: 更新日期 / 例如: 本日最新=0 二週內=14 一個月內=30
            # s9:上班時段 / 例如: 日班=1 晚班=2
            # page: 搜尋結果第N頁
            # 此處搜尋條件設定為: 無

            checkSuccess = False
            tryNums = 0
            while not checkSuccess:
                response, checkSuccess = self._checkConnect(url, headers)
                if not checkSuccess:
                    if tryNums == 5:
                        break
                    tryNums += 1
                    print('本次下載失敗 程式暫停3秒')
                    time.sleep(3)

            if tryNums == 10:
                print('下載失敗次數累積10次 結束程式')
                break

            if '搜尋條件無符合工作機會' in response.text:
                print('搜尋結果已到底 無工作職缺資訊可下載 爬蟲終止!')
                break
            soup = BeautifulSoup(response.text, 'html.parser')

            jobList = soup.select('article.b-block--top-bord')  # 搜尋返回結果
            jobAnnounceDate = [elem.select(
                'span.b-tit__date')[0].text.replace('\n', '').strip() for elem in jobList]  # 職缺公布時間
            jobTitles = [elem.select('a.js-job-link')
                         [0].text for elem in jobList]  # 職缺名稱
            jobCompanyName = [elem.select('a')[1].text.replace(
                '\n', '').strip() for elem in jobList]  # 職缺公司名稱
            jobCompanyUrl = [
                'https:' + elem.select('a')[1]['href'] for elem in jobList]  # 職缺公司頁面資訊連結
            jobCompanyIndustry = [elem.select(
                'li')[2].text for elem in jobList]  # 職缺公司所屬產業類別
            jobSalary = [elem.select('div.job-list-tag.b-content')
                         [0].select('span')[0].text for elem in jobList]  # 待遇資訊
            jobApplyNums = [elem.select(
                '.gtm-list-apply')[0].text[:-2] for elem in jobList]  # 應徵人數
            jobOtherInfo = [elem.select('ul.b-list-inline.b-clearfix.job-list-intro.b-content')[0]
                            for elem in jobList]  # 整理其他工作資訊(工作地點, 年資要求, 學歷要求)
            jobLocation = [elem.select(
                'li')[0].text for elem in jobOtherInfo]  # 工作地點
            jobRqYear = [elem.select(
                'li')[1].text for elem in jobOtherInfo]  # 年資要求
            jobRqEducation = [elem.select(
                'li')[2].text for elem in jobOtherInfo]  # 學歷要求

            jobDetailUrl = ['https:' +
                            elem.select('a')[0]['href'] for elem in jobList]  # 職缺網址資訊
            # 迴圈職缺網址資訊更詳細資訊
            jobContent, jobCategory, jobRqDepartment, jobSpecialty, jobOthers = [], [], [], [], []
            for i, iJobDetailUrl in enumerate(jobDetailUrl):

                print('爬取第' + str(page) + f'頁：第{i+1}個職缺 ' +
                      str(i+1) + ' / ' + str(len(jobDetailUrl)))

                # 詳細資訊需透過額外的ajax爬取
                iUrl = 'https://www.104.com.tw/job/ajax/content/' + \
                    re.search('job/(.*)\?', iJobDetailUrl).group(1)

                # 設定header
                headers = {
                    'Referer': iJobDetailUrl,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                    '(KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
                }

                checkSuccess = False
                tryNums = 0
                while not checkSuccess:
                    response, checkSuccess = self._checkConnect(iUrl, headers)
                    if not checkSuccess:
                        if tryNums == 5:
                            break
                        tryNums += 1
                        print('本次下載失敗 程式暫停3秒')
                        time.sleep(3)

                if tryNums == 10:
                    print('下載失敗次數累積10次 結束程式')
                    break

                # 網頁資料
                response = response.json()

                # 判斷是否有error: 職務不存在
                if response.get('error'):
                    jobContent.append('')
                    jobCategory.append('')
                    jobRqDepartment.append('')
                    jobSpecialty.append('')
                    jobOthers.append('')

                else:
                    jobContent.append(
                        response['data']['jobDetail']['jobDescription'])  # 工作內容
                    jobCategory.append(','.join(
                        [elem['description'] for elem in response['data']['jobDetail']['jobCategory']]))  # 職務類別
                    reparment = ','.join(
                        response['data']['condition']['major'])
                    if reparment == '':
                        reparment = '不拘'

                    jobRqDepartment.append(reparment)  # 科系要求
                    jobSpecialty.append(','.join(
                        [elem['description'] for elem in response['data']['condition']['specialty']]))  # 擅長工具
                    jobOthers.append(
                        response['data']['condition']['other'])  # 其他條件

                # 暫停秒數避免爬太快
                time.sleep(0.5)

            # 組合資訊成資料表並儲存
            iOutputDf = pd.DataFrame({'jobAnnounceDate': jobAnnounceDate,
                                      'jobTitles': jobTitles,
                                      'jobCompanyName': jobCompanyName,
                                      'jobCompanyUrl': jobCompanyUrl,
                                      'jobCompanyIndustry': jobCompanyIndustry,
                                      'jobContent': jobContent,
                                      'jobCategory': jobCategory,
                                      'jobApplyNums': jobApplyNums,
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
        outputDf.drop_duplicates(['jobTitles', 'jobCompanyName'], inplace=True)

        return outputDf
        # 輸出csv檔案
