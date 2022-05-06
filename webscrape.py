import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# get spring 22 archive web page 
sp22url="https://cinema.cornell.edu/film-archive/spring-2022"
sp22page=BeautifulSoup(
    requests.get("https://cinema.cornell.edu/film-archive/spring-2022").text,'lxml')
cards_sp22=sp22page.find_all('article',class_='card card--event')
links_sp22=["https://cinema.cornell.edu"+
            card.find('a')['href'] for card in cards_sp22]

events_sp22=[BeautifulSoup(requests.get(link).text,'lxml') for link in links_sp22]

# -- helper methods to parse event page --
get_name = lambda event:event.find('h1',class_="pageTitle").text.strip()
get_start = lambda event:datetime.fromisoformat(event.find('span',class_="date-display-single")['content'])
def get_end(event,start: datetime):
    delta_string=event.find('h3',class_="field-label",text="\n    Runtime  ").next_sibling.strip()
    delta_dt=datetime.strptime(delta_string,"%H hr %M min")
    delta = timedelta(hours=delta_dt.hour,minutes=delta_dt.minute)
    return start+delta

event_tuples_sp22 = [(get_name(event),get_start(event),get_end(event)) for event in events_sp22]




    
    

