import pandas as pd
import time
import requests
import re
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup

def scrape_race_results(race_id_list, pre_race_results=[]):
    race_results = pre_race_results
    race_results={}
    for race_id in tqdm(race_id_list):
        if race_id in race_results.keys():
            continue
        try:
            url = "http://db.netkeiba.com/race/" + race_id
            race_results[race_id] = pd.read_html(url)[0]
            time.sleep(1)
        except IndexError:
            continue
        except:
            break
    return race_results



def scrape_race_results2(race_id_list, pre_race_results=[]):
    race_results = pre_race_results
    race_results={}
    for race_id in tqdm(race_id_list):
        if race_id in race_results.keys():
            continue
        try:
            url = "http://db.netkeiba.com/race/" + race_id
            df = pd.read_html(url)[0]

            #horse_idとjockey_idをスクレイピング
            html = requests.get(url)
            html.encoding = 'ECU-JP'
            soup = BeautifulSoup(html.content, "html.parser")
            #horse_id
            horse_id_list = []
            horse_a_list = soup.find('table', attrs={'summary':'レース結果'}).find_all('a',attrs={'href':re.compile('^/horse')})
            for a in horse_a_list:
                horse_id = re.findall(r'\d+', a['href'])
                horse_id_list.append(horse_id[0])
            #jockey_id
            jockey_id_list = []
            jockey_a_list = soup.find('table', attrs={'summary':'レース結果'}).find_all('a',attrs={'href':re.compile('^/jockey')})
            for a in jockey_a_list:
                jockey_id = re.findall(r'\d+', a['href'])
                jockey_id_list.append(jockey_id[0])

            df['horse_id'] = horse_id_list
            df['jockey_id'] = jockey_id_list
            race_results[race_id] = df
            time.sleep(1)
        except AttributeError:
            continue
        except IndexError:
            continue
        except:
            break
    return race_results
