from bs4 import BeautifulSoup
from requests import get
import datetime
import json
import urllib3


class DataFetcher():

    '''
    Class prepared to scrap essential data from https://szpital.slask.eu:4433
    website and map it into json file fo further use.
    '''

    def __init__(self,url):
        self.__url = url
        self.main_page = BeautifulSoup(get(url, verify=False).content.decode('utf-8'),'html.parser')
        self.__data = self.__initialize_json()
        self.__find_wards()
    

    def _get_data(self):
        return self.__data

    def __initialize_json(self):
        result = {}

        _date = datetime.datetime.now()

        result['lastUpdate'] = {
            'date': str(_date).split(' ')[0],
            'day': _date.strftime("%A"),
            'time':str(_date).split(' ')[1][:8],
            'UTC': '+0000',
            'timezone': 'Coordinated Universal Time'
        }

        result['data'] = []

        return result


    def __find_wards(self):
        # Scrapping from main page names of wards and urls to their subpages
        wards = self.main_page.find_all("a", class_="report_department_link")
        for w in wards:
            ward = {"wardName":w.text, "url":f"https://szpital.slask.eu:4433{w['href']}", "counties":[]}
            self.__data['data'].append(ward)
        
        # Actual fetchin data form subpages
        for item in self.__data['data']:
            print(f"Processed ward: {item['wardName']}")
            ward_page = BeautifulSoup(get(item['url'], verify=False).content.decode('utf-8'), 'html.parser')
            counties = ward_page.find('table', class_="table").find_all('tr', recursive=False)[1:]
            for c in counties:
                item["counties"].append(self.__fetch_county_data(c))
                
    
    def __fetch_county_data(self,county):
        result = {}

        if county.find_all('td', recursive=False)[0].find('b') is not None:
            county_name = county.find_all('td', recursive=False)[0].find('b').text
            result['countyName'] = county_name # set the county name

            hospitals_info = county.find_all('td', recursive=False)[1].find_all('table', class_="table")
            result['hospitals'] = []

            for h_info in hospitals_info:
                result['hospitals'] += self.__fetch_hospitals_data(h_info)

        return result

    # fetch and set rest of important data
    def __fetch_hospitals_data(self,hospitals):
        result = []
        _type = hospitals.find_all('tr',recursive=False)[0].find('b').text

        hospitals = hospitals.find_all('tr',recursive=False)[1:]
        
        for h in hospitals:
            single_hospital = {}

            h_name = h.find('div', class_="report_hospital_name").text
            single_hospital["hospitalName"] = h_name
            single_hospital['type'] = _type

            timestamp = h.find_all('td',recursive=False)[2].text
            single_hospital["updateAt"] = timestamp


            free_beds = None
            try:
                free_beds = int(h.find('span', class_="report_number").text)
            except:
                free_beds = h.find('span', class_="report_number").text


            single_hospital["freePlaces"] = free_beds

            more_specific_data = h.find('div', class_="report_hospital_details")

            all_beds = more_specific_data.find('td',string="Ilość miejsc na oddziale:")
            if all_beds is not type(None):
                try:
                    all_beds = int(all_beds.parent.find_all('td')[1].text)
                except:
                    all_beds = all_beds.parent.find_all('td')[1].text
            else:
                all_beds = None
            single_hospital["allPlaces"] = all_beds

            telephone = more_specific_data.find('td',string="Telefon na oddział:")
            if telephone is not type(None):
                telephone = telephone.parent.find_all('td')[1].text 
            else:
                telephone = None
            single_hospital["telephone"] = telephone


            adress = more_specific_data.find('td',string="Adres:")
            if adress is not type(None): 
                adress = adress.parent.find_all('td')[1].text 
               
            else:
                adress = None
            single_hospital["adress"] = adress


            map_url = more_specific_data.find('td',string="Link do mapy:")
            if map_url is not None: 
                map_url = map_url.parent.find_all('td')[1].find('a')['href']

                
            else: 
                map_url = None
            single_hospital["mapUrl"] = map_url

            result.append(single_hospital)
        
        return result
            


if __name__ == "__main__":

    urllib3.disable_warnings()
    URL = "https://szpital.slask.eu:4433/page/"
    df = DataFetcher(URL)
    data = df._get_data()

    try:
        with open('data.json', 'w',encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
        print('\nSucces, file properly saved !')
    except:
        print('Something went wrong with saving file.')