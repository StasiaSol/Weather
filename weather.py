import requests
from bs4 import BeautifulSoup as BS
from tkinter import *

class Weather:
    def __init__(self,link):
        self.link = link
        r = requests.get(self.link).text    #получили код страницы в виде текста
        self.soup = BS(r, 'html.parser')
    def get_cities(self):
        links = self.soup.find_all('a')
        return links
    
class Window:
    def __init__(self,links):
        self.root = Tk()
        self.root.geometry('400x600')
        self.root.title('Прогноз погоды')
        self.check = []
        self.listbox = Listbox(self.root,width=70)
        self.listbox.grid(row=0, column = 0, columnspan=2)
        self.set_scrol(links)
        # self.label = Label(self.root, wraplength=800, font=("Trebuchet MS", 11))
        # self.label.grid(row=0, column=0, columnspan=2)
        # self.set_text(links)
        self.entry = Entry(self.root, width=50)
        self.entry.grid(row=1, column=0, sticky='E')
        self.btn = Button(self.root, text="Ввод", command=lambda x=links: self.check_input(links))
        self.btn.grid(row=1, column=1, sticky='W')
        self.label = Label(self.root, wraplength=400, font=("Trebuchet MS", 11))
        self.label.grid(row=2, column=0, columnspan=2)
    def set_text(self, links):
        text = ""
        for city in links:
            self.check.append(city)
            text += city + ', '
        text = text[:-2]
        self.label.configure(text=text)
    def set_scrol(self, links):
        text = []
        for city in links:
            self.check.append(city)
            text.append(city)
        variable = StringVar(value=text)
        self.listbox.configure(listvariable=variable)
    def check_input(self, links):
        choice = self.entry.get()
        if not choice :
            index = self.listbox.curselection()[0]
            # print(index)
            choice = tuple(links.keys())[index]
            # print(choice)    
            self.entry.configure(textvariable= choice )
        if choice not in self.check:
            return  
        self.parse_weather(links[choice])
    def parse_weather(self,link):
        try:
            w = Weather(link) 
            # print(w.__dict__)
            data = w.soup.find('div',{'id':'archiveString'})
            temp = data.find('span', {'class': 't_0'}).text
            text = data.find('div', {'class': 'ArchiveInfo'})
            text = text.text.replace("Архив погоды на метеостанции", "")
        except AttributeError : 
            temp = ''
            text = 'Информация не найдена. \nAtribute'
        except UnboundLocalError:
            temp = ''
            text = 'Информация не найдена'
        self.label.configure(text=temp + "\n" + text)

if __name__ == '__main__':
    w = Weather('https://rp5.ru/Погода_в_России')
    #print(w.soup)   #получили код страницы
    data_w = w.get_cities()
    links = {}
    for block in data_w:
        tex = block.__str__()
        name = block.get_text()
        if name not in ('','Мобильная версия','Главная','Новости','О сайте','Частые вопросы (FAQ)','Контакты','Беларусь','Литва','Россия','Украина',
                        'Все страны','>>>','См. на карте','Посмотреть',' 21 сент. 2023','Посмотреть'):
            
            tex = tex[tex.find('href="'):][6:]
            last  = tex.find('"')
            tex = tex[:last]
            links[name] = 'https://rp5.ru'+tex
            # print(name)
    window = Window(links)
    window.root.mainloop()