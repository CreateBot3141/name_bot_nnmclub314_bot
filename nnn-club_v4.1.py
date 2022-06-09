# Версия 4.1. 
# ОПИСАНИЕ БОТА: Читает данные с торент канала
# Улутшаем парсинг, добавляем классы
# Скорость и качество парснга

class proxy_test():
    def __init__(self):
        self.ip     = ''
        self.port   = ''
        self.proxy_list  = []
        self.nomer = 0
    def get_proxy (self):
        sql = "select ip from proxy where id > 29581 and rating > 0 ORDER BY rating DESC;"
        cursor.execute(sql)
        data = cursor.fetchall()  
        self.proxy_list = []  
        for rec in data: 
            ip = rec['ip']
            ip_proxy_and_port = ip.replace('http://','')
            nm = ip_proxy_and_port.find(':')
            ip_proxy    = ip_proxy_and_port[:nm]
            port_proxy  = ip_proxy_and_port[nm+1:]
            self.proxy_list.append([ip_proxy,port_proxy])
        self.ip   = self.proxy_list[self.nomer][0]
        self.port = self.proxy_list[self.nomer][1]
    def change (self):
        self.nomer = self.nomer + 1
        self.ip   = self.proxy_list[self.nomer][0]
        self.port = self.proxy_list[self.nomer][1]

    def save_good (self):
        import time
        print ('     [+] Повышаем рейтинг хорошего прокси',self.ip,self.port)
        unixtime = time.time ()
        sql = "UPDATE proxy SET rating = rating + 1,unixtime = "+str(unixtime)+" WHERE `ip` like '%"+str(self.ip)+":"+str(self.port)+"%'"
        cursor.execute(sql)
        db.commit()          

class parse_nnm_club_page_main ():
    
    def __init__(self,proxy):
        self.url    = ''
        self.title  = ''
        self.body   = ''
        self.code   = ''
        self.proxy  = proxy #     0        1     2      3         4          5         6         7     8    9      10
        self.news   = []  ## [nome_site,title1,title2,href4,url_picture,save_info,save_picture,title_find,title2,titlw3]
   
    def parser_page (self,url):
        self.url    = url
        self.title,self.code,self.body = get_page (self.url,self.proxy)
        return 

    def test_download_page (self,title):
        if title == self.title:
            ### Записываем прокси как хороший
            #self.proxy.save_good ()
            return 'Good'
        else:
            return 'Bad'

    def get_list_news (self):
        print ('        [+] №1: Получить список всех новостей на главной странице ...')    
        from bs4 import BeautifulSoup
        soup1 = BeautifulSoup(self.body.decode('windows-1251'), 'lxml')
        quotes1 = soup1.find_all('table',class_ = 'pline')
        for link1 in quotes1:
            title1      = ''
            title2      = ''
            nome_site   = ''
            href4       = ''
            url_picture = ''
            soup2 = BeautifulSoup(str(link1), 'lxml')
            quotes2 = soup2.find_all('td')
            nm = 0
            for link2 in quotes2:
                nm = nm + 1
                if nm == 1:
                   title1 = link2.text
                if nm == 3:
                   title2 = link2.text
            soup3 = BeautifulSoup(str(link1), 'lxml')
            quotes3 = soup3.find_all(class_ = 'pcatHead')
            nm = 0
            for link3 in quotes3:
                nm = nm + 1
                soup4 = BeautifulSoup(str(link3), 'lxml')
                quotes4 = soup4.find_all('a')                
                for link4 in quotes4:  
                    if nm == 1:
                        href4 = 'http://nnmclub.to/forum/'+link4.get('href')  
            nome_site = href4.replace('http://nnmclub.to/forum/viewtopic.php?t=','')
            soup5 = BeautifulSoup(str(link1), 'lxml')
            quotes5 = soup5.find_all(class_ = 'portalImg')
            nm = 0
            for link5 in quotes5:
                nm = nm + 1
                url_picture = unquote(link5.get('title'))
            if href4.find ('viewtopic.php?') != -1:
                self.news.append ([nome_site,title1,title2,href4,url_picture,'','','','','','',''])
                color_start,color_end = color (17)
                print (color_start,'        [+] №1:',nome_site,' - ',title1,': Получена',color_end)    

    def print_page (self): 
        #print ('    [+]',self.title,' - ',self.proxy.ip)  
        pass

    def parse_nnm_club_page_second (self,proxy):
        print ('        [+] №3: Парсер страниц по найденным ссылкам ...')    
        for new in self.news:
            if str(new[5]) == '0':  
                color_start,color_end = color (3)          
                print (color_start,'        [+] №3:',new[0],' - ',new[1],':id=',new[5],color_end)
                code = 0
                while code != 200:
                    title,code,body = get_page (new[3],proxy)
                    #print ('        [+]',title,' - ',code)
                from bs4 import BeautifulSoup
                soup1 = BeautifulSoup(body.decode('windows-1251'), 'lxml')
                quotes1 = soup1.find_all('span',class_ = 'nav')
                title2 = ''
                title3 = ''
                for link1 in quotes1:
                    soup2 = BeautifulSoup(str(link1), 'lxml')
                    quotes2 = soup2.find_all('a')
                    nomer = 0
                    for link2 in quotes2:
                        nomer = nomer + 1
                        if nomer == 1:
                            pass
                        if nomer == 2:    
                            title2 = link2.text
                        if nomer == 3:    
                            title3 = link2.text
                new[9]  = str(title2)
                new[10] = str(title3)
                magnet = ''
                soup3 = BeautifulSoup(body.decode('windows-1251'), 'lxml')
                quotes3 = soup3.find_all('a')
                for link3 in quotes3:
                    href4 = link3.get('href')
                    if str(href4).find ('magnet') != -1:         
                        magnet = str(href4)
                        #print ('        [+] magnet:',magnet) 
                new[11] = magnet        
            else: 
                color_start,color_end = color (16)
                print (color_start,'        [+] №3:',new[0],' - ',new[1],': Пропушена',new[5],color_end)   
    
    def test_list_news (self):
        print ('        [+] №2: Проверить что информация хратиться в нашей базе ...')
        for new in self.news:            
            sql = "select id,name from torrent where code = '"+str(new[0])+"' limit 1;"
            cursor.execute(sql)
            data = cursor.fetchall()
            id = 0
            name = 'save'
            for rec in data: 
                id   = rec['id']
                name = 'В базе'
            if id == 0:
                nm   = new[0]
            new[5] = str(id)
            new[6] = str(name)
            new[7] = ''
            
            if new[5] == 0:
                color_start,color_end = color (3)
                print (color_start,'        [+] №2:',new[0],' - ',new[1],': id=',new[5],color_end)
            else:    
                color_start,color_end = color (18)
                print (color_start,'        [+] №2:',new[0],' - ',new[1],': id=',new[5],color_end)

    def save_list_news (self):
        print ('        [+] №4: Скачивание необходимой картинки для новости ...')
        for new in self.news:
            #if str(new[5]) == '0':
            if 1==1:
                name_file_save = save_picture_file (new[4],new[0])                 
                new[7] = str(name_file_save)
                color_start,color_end = color (21)
                print (color_start,'        [+] №4:',new[0],' - ',new[1],': save =',new[6],color_end)
            else:
                pass # Картинка была скачена ранее ...

class user_telegram():
    def __init__(self, user_id):
        self.user_id = user_id
    
    def send_message(self,message_out):
        id_message_send = 0
        return id_message_send
      
class user_list ():
    def __init__(self,namebot):
        print ('    [+] №0: Загрузка клиентов для отправки ...')
        self.namebot   = namebot
        self.user_list = [user_telegram(-1001223464987)]
        self.token     = '' 

        #sql = "select token from bots where name = '{}' limit 1;".format(namebot)
        #cursor.execute(sql)
        #data = cursor.fetchall()
        #for rec in data: 
        #    self.token = rec['token']

        sql = "select token from bots where name = '{}' limit 1;".format(namebot)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            self.token = rec['token']

        list_accept = []
        list_accept.append ("399838806")
        
        #sql = "select user_id from bot_setting where namebot = '"+str(namebot)+"' and variable = 'Рассылка' and meaning = 'Отключена';"
        #cursor.execute(sql)
        #data = cursor.fetchall()  
        #for rec in data: 
        #    list_accept.append (rec['user_id'])

        #sql = "select id,user_id,username,first_name,last_name from bot_user where namebot = '"+str(namebot)+"' and (send_message = '' or send_message = 'Да');"
        #cursor.execute(sql)
        #data_user = cursor.fetchall()  
        #for rec_user in data_user: 
        #    accept = ''
        #    if list_accept.count(rec_user['user_id']) != 0:
        #        accept = 'Глобальное отключение'
        #    if accept == '' and rec_user['user_id'] != '':
        #        #print ('[+] Добавляем в списк',rec_user['user_id'],list_accept.count(rec_user['user_id']))
        #        self.user_list.append(user_telegram(rec_user['user_id']))
        #    else:
        #        pass

    def print_user_list (self):
        for user_telegram in self.user_list:
            pass
            #print ('    [+] ',user_telegram.user_id)

    def send_message_users (self,namebot,message,page):
        print ('        [+] №5: Отправляем сообшения подписанным клиентам ...')
        import telebot
        bot   = telebot.TeleBot(self.token) 
        for new in page.news:
            #if 1==1:
            if new[6] == 'save':
                color_start,color_end = color (3)
                print (color_start,'        [+] №5:',new[0],' - ',new[1],color_end)
                nm           = new[0]
                title_save   = new[1]
                main_text    = new[2]
                title02      = new[9] 
                title03      = new[10]
                magnet       = new[11] 
                name_file_save = new[7]
                id = save_news_in_base (nm,title_save,main_text,title02,title03,magnet,name_file_save)
                if id != 0:
                    title = new[1]
                    title = title.replace('<','')
                    title = title.replace('>','')
                    title2 = new[9]
                    title2 = title2.replace('<','')
                    title2 = title2.replace('>','')
                    title3 = new[10]
                    title3 = title3.replace('<','')
                    title3 = title3.replace('>','')
                    main = new[2]  
                    main = main.replace('<','')
                    main = main.replace('>','')
                    message_out = message
                    message_out = message_out.replace('%%code%%',str(new[0]))  
                    message_out = message_out.replace('%%title%%',str(title))  
                    message_out = message_out.replace('%%url%%',str(new[3]))
                    message_out = message_out.replace('%%title02%%',str(title2))
                    message_out = message_out.replace('%%title03%%',str(title3))
                    message_out = message_out.replace('%%magnet%%',str(new[11]))
                    message_out = message_out.replace('%%main%%',str(main))
                    if str(new[7]) != '':  
                        koll_user_good = 0
                        koll_user_bad  = 0                  
                        for user in self.user_list:
                           
                            if 1==1:                             
                                answer = iz_telegram.send_photo (user.user_id,namebot,str(new[7]))                                  
                                answer = iz_telegram.bot_send (user.user_id,namebot,message_out,'',0)

                            if answer == 'Не отправлен':
                                koll_user_bad  = koll_user_bad  + 1
                                color_start,color_end = color (12)
                                print (color_start,'            [+]',koll_user_bad,user.user_id,answer,color_end)
                            else:    
                                koll_user_good = koll_user_good + 1
                                color_start,color_end = color (3) 
                                print (color_start,'            [+] Задание: {:10s}   {:10s}   {:15s}   {:10s} '.format (str(koll_user_good),str(user.user_id),str(answer),'- Отправлен'),color_end)

                        print ('    [+] Отчет отправленных сообщений')
                        print ('    [+] Хороших:',koll_user_good)
                        print ('    [+] Плохих :',koll_user_bad)
                else:        
                    color_start,color_end = color (2)
                    print (color_start,'            [+] №5.1: Не удалось сохранить в базе данных. Нет картинки',color_end)

def connect ():
    import pymysql
    db = pymysql.connect(host = iz_data.host,
                            user = iz_data.user,
                            password = iz_data.password,
                            database = iz_data.database,
                            charset = iz_data.charset,
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()         
    return db,cursor

def get_page (url,proxy):
    
    proxy = '45.134.28.19:30016'

    from grab import Grab
    code  = 0
    body  = ''
    title = ''
    g = Grab()
    #proxy_data = str(proxy.ip)+str(':')+str(proxy.port)
    
    proxy_data = '45.134.28.19:30016'
    
    g.setup(proxy=proxy_data,proxy_userpwd='dm3nz_ya_ru:3d360c117a',proxy_type='http')
    try:
        g.go(url)
        title = g.doc.select('//title').text()
        code = g.doc.code
        body = g.doc.body
        title = title.strip()
    except Exception as e:
        #print ('        [-]',e) 
        title = "Сайт не отвечает"
        code  = 0
        body  = ''
    if title == '':
        title = "Нет Title"
    title = title.strip() 
    print ('[title]',title)    
    return title,code,body

def get_message (namebot,name_message):
    sql  = "SELECT message_rus,menu FROM bot_message where namebot = '"+str(namebot)+"' and name = '"+str(name_message)+"' limit 1"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        message_rus,menu = rec.values()
    return message_rus,menu    

def change (word):
    word = word.replace("'","<1>")
    word = word.replace('"',"<2>")
    word = word.replace('/',"<3>")
    word = word.replace(')',"<4>")
    word = word.replace('(',"<5>")
    return (word)

def save_picture_file (url_picture,nm):   
    #url_picture = url_picture.replace ('https://nnmclub.ch/forum/image.php?','')
    #url_picture = url_picture.replace ('link=','https:')    
    #print ("https://nnmstatic.win/forum/image.php?link=https://i4.imageban.ru/out/2022/06/04/577fed6d34a528dfcc06900b1e55cd52.jpg") 
    #url_picture = "https://nnmstatic.win/forum/image.php?link=https://i4.imageban.ru/out/2022/06/04/577fed6d34a528dfcc06900b1e55cd52.jpg" 
    name_file_save = '011_picture/save_picture_'+str(nm)+'.jpg'
    from  urllib.request import urlopen 
    try:
        urlt = urlopen(url_picture)
        f = urlt.read()
        open(name_file_save,"wb").write(f)
    except Exception as e:
        color_start,color_end = color (2)
        print (color_start,'[+] Ошибка скачивания файла:',e,color_end)
        print (color_start,'[+] Название файла:',url_picture,color_end)
        name_file_save = ''
    return name_file_save

def color (nomer):
    ### настройка цвета для вывода на экран
    if nomer == 0: c0  =  "\033[0;37m"  ## Белый
    #c1  =  "\033[1;30m"  ## Черный
    if nomer == 2: color_start =  "\033[0;31m"  ## Красный
    if nomer == 3: color_start =  "\033[0;32m"  ## Зеленый
    #c4  =  "\033[1;35m"  ## Magenta like Mimosa\033[1;m
    #c5  =  "\033[1;33m"  ## Yellow like Yolk\033[1;m'
    #c7  =  "\033[1;37m"  ## White
    if nomer == 8: color_start = "\033[1;33m"  ## Yellow
    #c9  =  "\033[1;32m"  ## Green
    #c10 =  "\033[1;34m"  ## Blue
    #c11 =  "\033[1;36m"  ## Cyan
    if nomer == 12: color_start =  "\033[1;31m"  ## Red
    #c13 =  "\033[1;35m"  ## Magenta
    #c14 =  "\033[1;30m"  ## Black
    #c15 =  "\033[0;37m"  ## Darkwhite
    if nomer == 16: color_start =  "\033[0;33m"  ## Darkyellow
    if nomer == 17: color_start =  "\033[0;32m"  ## Darkgreen
    if nomer == 18: color_start =  "\033[0;34m"  ## Darkblue
    #c19 =  "\033[0;36m"  ## Darkcyan
    #c20 =  "\033[0;31m"  ## Darkred
    if nomer == 21: color_start =  "\033[0;35m"  ## Darkmagenta
    #c22 =  "\033[0;30m"  ## Darkblack
    color_end =  "\033[0;0m"   ## Off
    return color_start,color_end


def iz_pause (wait):
    import time
    for number in range(wait):
        st_print = '[+] Ожидаем '+str(wait-number)+' сек.'
        dl_str = len (st_print)
        add_st = 30 - dl_str 
        for number in range(add_st):
            st_print = st_print + ' '
        print (st_print, end='')    
        ls = ''
        for k in range(30):
            ls = ls + '\b'
        print (ls, end='')
        time.sleep (1)


def save_news_in_base (nm,title_save,main_text,title02,title03,magnet,name_file_save):
    if name_file_save != '':
        title_save = change(title_save)   
        main_text  = change(main_text)
        title02    = change(title02)
        title03    = change(title03)
        sql = "INSERT INTO torrent (`code`,`name`,`text`,`title02`,`title03`,`magnet`,`name_file_save`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format (nm,title_save,main_text,title02,title03,magnet,name_file_save)
        cursor.execute(sql)
        db.commit()  
        lastid = cursor.lastrowid
        id   = lastid
        name = 'save'
    else:
        name = 'no picture'
        id   = 0 
    return id     

if __name__ == "__main__":
    import iz_data
    import iz_telegram
    from urllib.parse import unquote
    namebot =  iz_data.namebot 
    url     =  iz_data.url
    db,cursor = connect ()
    proxy = ''
    #proxy = proxy_test ()
    #proxy.get_proxy ()
    user_list = user_list (namebot) 
    page = parse_nnm_club_page_main (proxy)
    page.parser_page (url)
    #page.print_page () 
    answer = page.test_download_page ("Торрент-трекер :: NNM-Club")
    while  answer == 'Bad':
        proxy.change ()
        page.parser_page (url)
        answer = page.test_download_page ("Торрент-трекер :: NNM-Club") 
        page.print_page ()        
    page.get_list_news ()
    #page.print_news ()  
    page.test_list_news ()
    page.parse_nnm_club_page_second (proxy)
    page.save_list_news ()    
    message_out,menu = get_message (namebot,'Публикация')
    user_list.send_message_users (namebot,message_out,page)
    db.close
    print (iz_data.message001)
    iz_data.time.sleep (60*15)
    #iz_pause (60*15)










