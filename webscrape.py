from operator import le
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
    dstring=event.find('h3',class_="field-label",text="\n    Runtime  ").next_sibling.strip()
    h_index,m_index=dstring.find('h'),dstring.find('m')
    if h_index!=-1 and m_index!=-1:
        dstring=dstring.split(' ')
        dstring = dstring[0]+':'+dstring[2]
    elif h_index !=-1:
        dstring = dstring[0]+':'+'0'
    elif m_index !=-1:
        dstring= '0:'+dstring[0]
    else: dstring = '0:0'
    delta_dt=datetime.strptime(dstring,"%H:%M")
    delta = timedelta(hours=delta_dt.hour,minutes=delta_dt.minute)
    return start+delta

# --each event tuple is (name of event, start datetime, end datetime)
event_tuples_sp22 = []
for event in events_sp22:
    name = get_name(event)
    start = get_start(event)
    end = get_end(event, start)
    event_tuples_sp22.append((name, start, end))




    
    

