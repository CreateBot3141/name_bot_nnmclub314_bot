
### Создать новость по ID в базе данных
def get_message_in_base (message_id,user_id,namebot):
    import iz_func
    import iz_telegram
    markup      = ''
    message_out = ''
    db,cursor = iz_func.connect ()
    sql = "select id,name,title02,title03,code,magnet,`text`,name_file_save from torrent where id = '"+str(message_id)+"' limit 1;"
    print ('    [+] sql:',sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,title02,title03,code,magnet,main,name_file_save = rec.values()
        title    = iz_func.change_back (name) 
        title02  = iz_func.change_back (title02)
        title03  = iz_func.change_back (title03) 
        main     = iz_func.change_back (main)

        print ('        [+] Информация полученная из базы данных')
        print ('            [+] name',title)
        print ('            [+] title02',title02)
        print ('            [+] title03',title03)        
        url  = 'http://nnmclub.to/forum/viewtopic.php?t='+str(code)   
        name_file_save = '/home/izofen/Studiya/Parser/nnm/'+str(name_file_save)    
        print ('            [+] picture',name_file_save)

        message_out,menu = iz_telegram.get_message (user_id,'Публикация',namebot)
        message_out = message_out.replace('%%code%%',str(code))  
        message_out = message_out.replace('%%title%%',str(title))  
        message_out = message_out.replace('%%url%%',str(url))
        message_out = message_out.replace('%%title02%%',str(title02))
        message_out = message_out.replace('%%title03%%',str(title03))
        message_out = message_out.replace('%%magnet%%',str(magnet))
        message_out = message_out.replace('%%main%%',str(main))
    return message_out,markup,name_file_save

def send_message_in_base (user_id,namebot,message_out,markup,picture):
    import iz_telegram
    T2 = iz_telegram.send_photo (user_id,namebot,picture)    
    T3 = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)
    return T2,T3        

def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome,refer,user_id_refer,FIO_id):
    import iz_func
    import iz_game
    import iz_main
    import time
    import iz_telegram
    db,cursor = iz_func.connect ()

    label = 'send'
    if message_in.find ('/start') != -1:
        import iz_game
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''
        label = 'no send' 
        
    if message_in.find ('golos_OK') != -1:
        label = 'no send'
        pass  

    if message_in.find ('golos_BAD') != -1:
        label = 'no send'  
        pass

    if message_in.find ('Контакты') != -1:
        label = 'no send'  
        message_out,markup = iz_telegram.get_kontakt (user_id,namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)

    if message_in.find ('Next_') != -1:
        label = 'no send'
        word = message_in.replace('Next_','')
        db,cursor = iz_func.connect ()
        sql = "select id,`lost`,`see`,`strong`,`name`,`while` from sql_name where id = '"+str(word)+"' limit 1;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id_L,lost_L,see_L,strong_L,name_L,while_L = rec.values()
        n_all    = 0                      
        n_lost   = 0
        n_see    = 0
        n_next   = 0
        p_lost   = lost_L+1
        p_see    = see_L-1
        p_strong = 'DESC'
        if name_L == 'Поиск торент раздач': 
            sql = "select id,name from torrent where title03 = '"+str(while_L)+"'ORDER BY id DESC;"
        if name_L == 'Поиск ключевого слова': 
            sql = "select id,name  from torrent where name like '%"+str(while_L)+"%' ORDER BY id DESC;"
        if name_L == 'Поиск последних записей': 
            sql = "select id,name from torrent where 1=1 ORDER BY id DESC;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            n_all = n_all + 1
            id,name = rec.values()
            if n_all < p_lost: 
                n_lost  = n_lost  + 1

            if n_all >= p_lost and n_all <= p_lost+p_see:     
                n_see = n_see + 1
                #iz_game.nnmclub314_bot_message (id,user_id,namebot)

            if n_all > p_lost+p_see:  
                n_next = n_next + 1

        if n_next != 0:
            message_out = ''
            message_out = message_out + 'Продолжить поиск' + '\n'
            message_out = message_out + 'Всего найдено: ' + str(n_all)   + '\n'
            message_out = message_out + 'Пропушено   : '  + str(n_lost)  + '\n'
            message_out = message_out + 'Показано    : '  + str(n_see)   + '\n'
            message_out = message_out + 'Не показано : '  + str(n_next)  + '\n'
            message_out = message_out + 'Направление : '  + str(p_strong)+ '\n'
            from telebot import types
            markup = types.InlineKeyboardMarkup(row_width=4)
            menu01 = "Вперед"
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "Next_"+str(word))
            markup.add(mn01)
            answer = iz_func.bot_send (user_id,message_out,markup,namebot)    
            sql = "UPDATE sql_name SET `lost` = "+str(n_lost+n_see)+" WHERE `id` = '"+str(word)+"'"
            cursor.execute(sql)
            db.commit()
    
    if message_in == '/help':
         label = 'no send'
         pass

    if message_in == '/send_stop':
         label = 'no send'
         iz_telegram.save_variable (user_id,namebot,"Рассылка",'Отключена')
         message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Рассылка отключена",'S',0)

    if message_in == '/send_start':
         label = 'no send'
         iz_telegram.save_variable (user_id,namebot,"Рассылка",'Включена')
         message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Рассылка включена",'S',0)

    if message_in.find ('/new_') != -1:
        label = 'no send'
        word = message_in.replace('/new_','')
        word = 10
        try:
            sql = "select id,name from torrent where 1=1 ORDER BY id DESC limit "+str(word)+";"
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception as e:
            print ('[errror]',e)
            sql = "select id,name from torrent where 1=1 ORDER BY id DESC limit 10;"
            cursor.execute(sql)
            data = cursor.fetchall()
        for rec in data: 
            id,name = rec.values()
            message_out,markup,name_file_save = get_message_in_base (id,user_id,namebot)
            #print ('    [+] name_file_save:',name_file_save)
            send_message_in_base (user_id,namebot,message_out,markup,name_file_save)

    if message_in == 'Coin Farmer':
        label = 'no send' 
        import iz_game
        iz_game.game_farmer (user_id,namebot,"start",message_id,refer)
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''

    if message_in.find ('game_farmer_')     != -1:
        import iz_game        
        label = 'no send' 
        iz_game.game_farmer (user_id,namebot,message_in,message_id,refer)
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''

    if message_in  == 'Настройка' or message_in  == 'Back_setting':
        label = 'no send'  
        message_out,menu = iz_telegram.get_message (user_id,'Настройка новостей',namebot)
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        sql = "select DISTINCT title02 from nnmclub314_bot_Categoraya where 1=1;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            menu01 = rec['title02']
            sql = "select id,title02 from nnmclub314_bot_Categoraya where title02 = '"+str(menu01)+"' limit 1;"
            cursor.execute(sql)
            data2 = cursor.fetchall()
            for rec2 in data2: 
                id,title02 = rec2.values()
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "setting_"+str(id))
            markup.add(mn01)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Описание настройки','S',message_id) 

    if message_in.find ('setting_') != -1:
        label = 'no send'                    
        word = message_in.replace('setting_','')
        sql = "select id,title02 from nnmclub314_bot_Categoraya where id = '"+str(word)+"' limit 1;"
        cursor.execute(sql)
        data2 = cursor.fetchall()
        title02 = ''
        for rec2 in data2: 
            id,title02 = rec2.values()
        sql = "select id,title02,title03 from nnmclub314_bot_Categoraya where title02 = '"+str(title02)+"';"
        cursor.execute(sql)
        data = cursor.fetchall()
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        for rec in data: 
            id,title02,title03 = rec.values()
            sql = "select id,accept from nnmclub314_bot_Accept where user_id = '"+str(user_id)+"' and title02 = '"+title02+"' and title03 = '"+title03+"';"
            cursor.execute(sql)
            accept = 'Высылать'
            data2 = cursor.fetchall()
            for rec2 in data2: 
                id_a,accept = rec2.values()
            accept = iz_telegram.get_namekey (user_id,namebot,accept)
            menu01 = accept + "  " +title03
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "pokazatel_"+str(id))
            markup.add(mn01)
        menu01 = iz_telegram.get_namekey (user_id,namebot,'Назад') 
        mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "Back_setting")
        markup.add(mn01)
        message_out,menu = iz_telegram.get_message (user_id,'Настройка',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in.find ('pokazatel_') != -1:
        label = 'no send'
        db,cursor = iz_func.connect ()
        word = message_in.replace('pokazatel_','')                    
        sql = "select id,title02 from nnmclub314_bot_Categoraya where id = '"+str(word)+"' limit 1;"
        cursor.execute(sql)
        data2 = cursor.fetchall()
        for rec2 in data2: 
            id,title02 = rec2.values()
        sql = "select id,title02,title03 from nnmclub314_bot_Categoraya where title02 = '"+str(title02)+"';"
        cursor.execute(sql)
        data = cursor.fetchall()
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        for rec in data: 
            id,title02,title03 = rec.values()
            sql = "select id,accept from nnmclub314_bot_Accept where user_id = '"+str(user_id)+"' and title02 = '"+title02+"' and title03 = '"+title03+"';"
            cursor.execute(sql)
            accept = ''
            data2 = cursor.fetchall()
            for rec2 in data2: 
                id_a,accept = rec2.values()
            if str(id) == word:
                if accept == '':
                    accept = 'Запрет'
                    sql = "INSERT INTO nnmclub314_bot_Accept (`user_id`,`title02`,`title03`,`accept`,`catalog`) VALUES ('{}','{}','{}','{}','')".format (user_id,iz_func.change (title02),iz_func.change (title03),accept)
                    print ('[+] sql',sql)
                    cursor.execute(sql)
                    db.commit()
                else:
                    accept = 'Высылать'
                    sql = "UPDATE nnmclub314_bot_Accept SET accept = '' WHERE `id` = '"+str(id_a)+"'"
                    cursor.execute(sql)
                    db.commit()
            if accept == '':        
                accept = 'Высылать'
            accept = iz_telegram.get_namekey (user_id,namebot,accept)    
            menu01 = accept + "  " +title03
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "pokazatel_"+str(id))
            markup.add(mn01)
        menu01 = iz_telegram.get_namekey (user_id,namebot,'Назад') 
        mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "Back_setting")
        markup.add(mn01)            
        message_out = 'Настройки'    
        #answer = iz_func.bot_send (user_id,message_out,markup,namebot)    
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in.find ('/off_message_') != -1:
        label = 'no send'     
        word = message_in.replace('/off_message_','')
        db,cursor = iz_func.connect ()
        title02 = ''
        title03 = ''
        sql = "select id,title02,title03 from nnmclub314_bot_Categoraya where id = "+str(word)+";"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id_c,title02,title03 = rec.values()
        accept = 'Поиск'
        sql = "select id,accept from nnmclub314_bot_Accept where user_id = '"+str(user_id)+"' and title02 = '"+title02+"' and title03 = '"+title03+"';"
        cursor.execute(sql)
        data2 = cursor.fetchall()
        for rec2 in data2: 
            id_a,accept = rec2.values()
        if accept == 'Поиск':
            sql = "INSERT INTO nnmclub314_bot_Accept (`user_id`,`title02`,`title03`,`accept`) VALUES ('{}','{}','{}','{}')".format (user_id,title02,title03,'Запрет')
            cursor.execute(sql)
            db.commit()
        else:   
            sql = "UPDATE nnmclub314_bot_Accept SET accept = 'Запрет' WHERE `id` = '"+str(id_a)+"'"
            cursor.execute(sql)
            db.commit()
        markup = ''
        iz_telegram.save_variable (user_id,namebot,'title02',title02)
        iz_telegram.save_variable (user_id,namebot,'title03',title03)
        iz_telegram.send_message (user_id,namebot,'Отключеное сообщение','S',0)

    if message_in.find ('/on_message_') != -1:
        label = 'no send'     
        word = message_in.replace('/on_message_','')
        db,cursor = iz_func.connect ()
        title02 = ''
        title03 = ''
        sql = "select id,title02,title03 from nnmclub314_bot_Categoraya where id = "+str(word)+";"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id_c,title02,title03 = rec.values()
        accept = 'Поиск'
        sql = "select id,accept from nnmclub314_bot_Accept where user_id = '"+str(user_id)+"' and title02 = '"+title02+"' and title03 = '"+title03+"';"
        cursor.execute(sql)
        data2 = cursor.fetchall()
        id_a = 0
        for rec2 in data2: 
            id_a,accept = rec2
        if accept == 'Поиск':
            sql = "INSERT INTO nnmclub314_bot_Accept (`user_id`,`title02`,`title03`,`accept`,`catalog`) VALUES ('{}','{}','{}','{}','')".format (user_id,title02,title03,'')
            cursor.execute(sql)
            db.commit()
        else:  
            try:        
                sql = "UPDATE nnmclub314_bot_Accept SET accept = '' WHERE `id` = '"+str(id_a)+"'"
                print ('[sql]',sql)
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                pass
        markup = ''
        iz_telegram.save_variable (user_id,namebot,'title02',title02)
        iz_telegram.save_variable (user_id,namebot,'title03',title03)        
        iz_telegram.send_message (user_id,namebot,'Включение сообщения','S',0)

    if message_in == 'Поиск' or message_in == 'back_find':
        label = 'no send'
        message_out,menu = iz_telegram.get_message (user_id,'Введите поиск',namebot)
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        db,cursor = iz_func.connect ()
        sql = "select DISTINCT title02 from nnmclub314_bot_Categoraya where 1=1;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            menu01 = rec['title02']
            sql = "select id,title02 from nnmclub314_bot_Categoraya where title02 = '"+str(menu01)+"' limit 1;"
            cursor.execute(sql)
            data2 = cursor.fetchall()
            for rec2 in data2: 
                id,title02 = rec2.values()
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "categoriya_"+str(id))
            markup.add(mn01)
        menu01 = 'Последние'
        mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "end_list")
        markup.add(mn01)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Описание поиска','S',message_id) 
        #message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Поиск временно отключен','S',message_id)

    if message_in.find ('categoriya_') != -1:
        label = 'no send'                    
        word = message_in.replace('categoriya_','')
        db,cursor = iz_func.connect ()
        sql = "select id,title02 from nnmclub314_bot_Categoraya where id = '"+str(word)+"' limit 1;"
        cursor.execute(sql)
        data2 = cursor.fetchall()
        for rec2 in data2: 
            id,title02 = rec2.values()
        sql = "select id,title02,title03 from nnmclub314_bot_Categoraya where title02 = '"+str(title02)+"';"
        cursor.execute(sql)
        data = cursor.fetchall()
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        for rec in data: 
            id,title02,title03 = rec.values()
            menu01 = title03
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "strateg_"+str(id))
            markup.add(mn01)
        menu01 = iz_telegram.get_namekey (user_id,namebot,'Назад') 
        mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "back_find")
        markup.add(mn01)
        message_out,menu = iz_telegram.get_message (user_id,'Категория поиска',namebot)     
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)   

    if message_in == 'Каталог':
        label = 'no send'
        message_out,markup = iz_telegram.get_katalog (user_id,namebot)        
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)

    if message_in.find ('strateg_') != -1:
        label = 'no send'
        word = message_in.replace('strateg_','')
        sql = "select id,title02,title03 from nnmclub314_bot_Categoraya where id = '"+str(word)+"' limit 1;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,title02,title03 = rec.values()
        n_all   = 0                      
        n_lost  = 0
        n_see   = 0
        n_next  = 0
        p_lost   = 0
        p_see    = 3
        p_strong = 'DESC'
        sql = "select id,name from torrent where title03 = '"+str(title03)+"'ORDER BY id DESC;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            n_all = n_all + 1
            id,name = rec.values()
            if n_all < p_lost: 
                n_lost  = n_lost  + 1
            if n_all >= p_lost and n_all <= p_lost+p_see:     
                n_see = n_see + 1
                message_out,markup,name_file_save = get_message_in_base (id,user_id,namebot)
                send_message_in_base (user_id,namebot,message_out,markup,name_file_save)
            if n_all > p_lost+p_see:  
                n_next = n_next + 1                    
        if n_next != 0:        
            sql = "INSERT INTO sql_name (`lost`,`see`,`strong`,`name`,`while`,bad,good,komment) VALUES ({},{},'{}','{}','{}',0,0,'')".format (p_see,p_see,p_strong,'Поиск торент раздач',title03)
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            message_out = ''
            message_out = message_out + 'Продолжить поиск' + '\n'
            message_out = message_out + 'Всего найдено: ' + str(n_all)   + '\n'
            message_out = message_out + 'Пропушено   : '  + str(n_lost)  + '\n'
            message_out = message_out + 'Показано    : '  + str(n_see)   + '\n'
            message_out = message_out + 'Не показано : '  + str(n_next)  + '\n'
            message_out = message_out + 'Направление : '  + str(p_strong)+ '\n'
            from telebot import types
            markup = types.InlineKeyboardMarkup(row_width=4)
            menu01 = "Вперед"
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "Next_"+str(lastid))
            markup.add(mn01)
            answer = iz_func.bot_send (user_id,message_out,markup,namebot)    

    if label == 'send':
        message_out = 'Поиск в названии торента: '+str(message_in)
        markup = ''                      
        #answer = iz_func.bot_send (user_id,message_out,markup,namebot)    
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)
                                
        n_all   = 0                      
        n_lost  = 0
        n_see   = 0
        n_next  = 0
        p_lost   = 0
        p_see    = 3
        p_strong = 'DESC'

        db,cursor = iz_func.connect ()
        sql = "select id,name  from torrent where name like '%"+str(iz_func.change(message_in))+"%' ORDER BY id DESC;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,name = rec.values()
            n_all = n_all + 1
            if n_all < p_lost: 
                n_lost  = n_lost  + 1

            if n_all >= p_lost and n_all <= p_lost+p_see:     
                n_see = n_see + 1
                #iz_game.nnmclub314_bot_message (id,user_id,namebot)
                #send_message (id,user_id,namebot)
                message_out,markup,name_file_save = get_message_in_base (id,user_id,namebot)
                send_message_in_base (user_id,namebot,message_out,markup,name_file_save)

                if n_all > p_lost+p_see:  
                    n_next = n_next + 1
                    if n_next != 0:        
                        sql = "INSERT INTO sql_name (`lost`,`see`,`strong`,`name`,`while`,bad,good,komment) VALUES ({},{},'{}','{}','{}',0,0,'')".format (p_see,p_see,p_strong,'Поиск ключевого слова',message_in)
                        cursor.execute(sql)
                        db.commit()
                        lastid = cursor.lastrowid
                        message_out = ''
                        message_out = message_out + 'Продолжить поиск' + '\n'
                        message_out = message_out + 'Всего найдено: ' + str(n_all)   + '\n'
                        message_out = message_out + 'Пропушено   : '  + str(n_lost)  + '\n'
                        message_out = message_out + 'Показано    : '  + str(n_see)   + '\n'
                        message_out = message_out + 'Не показано : '  + str(n_next)  + '\n'
                        message_out = message_out + 'Направление : '  + str(p_strong)+ '\n'
                        from telebot import types
                        markup = types.InlineKeyboardMarkup(row_width=4)
                        menu01 = "Вперед"
                        mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "Next_"+str(lastid))
                        markup.add(mn01)
                        answer = iz_func.bot_send (user_id,message_out,markup,namebot)    

    db.close












