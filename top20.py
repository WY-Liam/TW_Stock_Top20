def top_20(x):
    import pandas as pd
    
    import requests 
    
    from bs4 import BeautifulSoup as bs
    
    import time
    
    import sqlite3
    
    
    try:
        date = str(x)

        date = pd.to_datetime(date).strftime('%Y%m%d')
    
        url = ("https://www.twse.com.tw/exchangeReport/MI_INDEX20?response=html&date=%s" %date)
    
        headers = {
        'content-type': 'text/html; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }
    
        res = requests.get(url = url, headers = headers)

        res = res.content

        soup = bs(res, 'lxml')
    
        t3 = soup.find_all('tr')
    
        target_cols = t3[1].text.replace('\n', ',').split(',')[1 : -1]
    
        dfs = pd.DataFrame()
    
        for i in range(2, 22):
            dfs[str(i)] = t3[i].text.replace(',', '').split('\n')[1:-1]
    
        target_list = dfs.values.tolist()
    
        dfs_target = pd.DataFrame()
        for i in range(len(target_list)):
            dfs_target[str(target_cols[i])] = target_list[i]
    
        dfs_target.index = dfs_target['排名']
    
        dfs_target = dfs_target.drop(columns = ['排名'])
        
        sqlname = 'top20.db'
        
        db = sqlite3.connect(sqlname)
        
        dfs_target.to_sql(date, db, if_exists = 'replace')
        
        time.sleep(10)

        print(date, '-> successful')
        
    except:
        print(date, '-> fail')

if __name__ == '__main__':
    top_20