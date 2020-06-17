#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
try:
    from Tkinter import *
    import ttk
    import tkFileDialog
    import re
    from grab import Grab
    from string import Template
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    from sqlalchemy.orm import mapper
    import threading
    import time
    import logging
    import shutil
except ImportError:
    print>>sys.__stderr__, "** IDLE can't import some modules. **\n"\
                           "** Your Python may not be configured for Spider. **"
    sys.exit(1)
country_dict = {'Canada': 34, 'East Timor': 200, 'Turkmenistan': 197, 'Saint Helena': 178, 'Vatican': 211, 'Lithuania': 119, 'Cambodia': 103, 'Ethiopia': 62, 'Aruba': 14, 'Swaziland': 190, 'Palestine': 163, 'Argentina': 11, 'Bolivia': 27, 'Cameroon': 42, 'Burkina Faso': 20, 'Ghana': 74, 'Saudi Arabia': 172, 'Japan': 100, 'Cape Verde': 47, 'Northern Mariana Islands': 132, 'Slovenia': 179, 'Guatemala': 82, 'Kuwait': 109, 'Jordan': 99, 'Dominica': 53, 'Liberia': 117, 'Maldives': 137, 'Norfolk': 145, 'Jamaica': 98, 'Oman': 153, 'Tanzania': 205, 'Martinique': 133, 'Albania': 6, 'French Guiana': 73, 'Niue': 151, 'Monaco': 124, 'New Zealand': 152, 'Yemen': 225, 'Jersey': 222, 'Bahamas': 29, 'Greenland': 76, 'Samoa': 219, 'United Arab Emirates': 2, 'Guam': 83, 'Kosovo': 240, 'India': 93, 'Azerbaijan': 15, 'Lesotho': 118, 'Guernsey and Alderney': 224, 'Saint Vincent and the Grenadines': 212, 'Kenya': 101, 'South Korea': 108, 'Tajikistan': 195, 'Turkey': 201, 'Afghanistan': 3, 'Bangladesh': 18, 'Mauritania': 134, 'Solomon Islands': 173, 'Turks and Caicos Islands': 191, 'Saint Lucia': 114, 'San Marino': 183, 'Kyrgyzstan': 102, 'Mongolia': 131, 'France': 68, 'Bermuda': 25, 'Namibia': 142, 'Somalia': 185, 'Peru': 155, 'Laos': 112, 'Nauru': 150, 'Seychelles': 174, 'Vanuatu': 217, 'Central Africa': 36, 'Cook Islands': 40, 'Benin': 24, 'Federated States of Micronesia': 66, 'Cuba': 46, 'Montenegro': 231, 'Saint Kitts and Nevis': 106, 'Togo': 193, 'China': 43, 'Armenia': 7, 'Dominican Republic': 54, 'Ukraine': 206, 'Bahrain': 22, 'Tonga': 199, 'Indonesia': 90, 'Libya': 122, 'Finland': 63, 'Mauritius': 136, 'Liechtenstein': 115, 'Belarus': 32, 'British Virgin Islands': 214, 'Mali': 129, 'Russia': 170, 'Bulgaria': 21, 'United States': 208, 'Romania': 169, 'Angola': 9, 'Cayman Islands': 110, 'Trinidad and Tobago': 202, 'Cyprus': 48, 'Sweden': 176, 'Qatar': 167, 'Malaysia': 140, 'Austria': 12, 'Vietnam': 216, 'Mozambique': 141, 'Uganda': 207, 'Hungary': 89, 'Niger': 144, 'Isle of Man': 223, 'Bosnia-Herzegovina': 16, 'Brazil': 28, 'Falkland Islands': 65, 'Faroe Islands': 67, 'Guinea': 78, 'Panama': 154, 'Costa Rica': 45, 'Luxembourg': 120, 'American Samoa': 238, 'Andorra': 1, 'Chad': 192, 'Norway': 221, 'Gibraltar': 75, 'Ivory Coast': 39, 'Pakistan': 159, 'Palau': 165, 'Nigeria': 146, 'Virgin Islands of the United States': 215, 'Ecuador': 56, 'Czech Republic': 49, 'Brunei': 26, 'Australia': 13, 'Iran': 95, 'Algeria': 55, 'El Salvador': 188, 'Tuvalu': 203, 'Antigua & Barbuda': 4, 'Marshall Islands': 127, 'Chile': 41, 'Puerto Rico': 162, 'Belgium': 19, 'Kiribati': 104, 'Haiti': 88, 'Belize': 33, 'Sierra Leone': 182, 'Georgia': 72, 'Wallis & Futuna': 218, 'Gambia': 77, 'Philippines': 158, 'Guinea Bissau': 84, 'Sao Tome And Principe': 187, 'Moldova': 125, 'Netherlands Antilles': 8, 'Croatia': 87, 'French Polynesia': 156, 'Thailand': 194, 'Switzerland': 38, 'Grenada': 71, 'Iraq': 94, 'Portugal': 164, 'Estonia': 57, 'Uruguay': 209, 'Mexico': 139, 'Lebanon': 113, 'South Africa': 228, 'Uzbekistan': 210, 'Tunisia': 198, 'Djibouti': 51, 'Rwanda': 171, 'Spain': 61, 'Colombia': 44, 'Reunion': 168, 'Burundi': 23, 'Slovakia': 181, 'Taiwan': 204, 'Fiji': 64, 'Barbados': 17, 'Madagascar': 126, 'Italy': 97, 'Bhutan': 30, 'Sudan': 175, 'Nepal': 149, 'Saint Pierre & Miquelon': 161, 'Malta': 135, 'Democratic Republic of the Congo': 35, 'Netherlands': 148, 'Suriname': 186, 'Anguilla': 5, 'Venezuela': 213, 'Israel': 92, 'Iceland': 96, 'Zambia': 229, 'Senegal': 184, 'Papua New Guinea': 157, 'Malawi': 138, 'Zimbabwe': 230, 'Germany': 50, 'Denmark': 52, 'Saint Martin': 239, 'Kazakhstan': 111, 'Poland': 160, 'Eritrea': 60, 'Ireland': 91, 'Mayotte': 226, 'Montserrat': 241, 'New Caledonia': 143, 'Macedonia': 128, 'North Korea': 107, 'Paraguay': 166, 'Latvia': 121, 'Guyana': 85, 'Syria': 189, 'Guadeloupe': 79, 'Morocco': 123, 'Honduras': 86, 'Myanmar': 130, 'Equatorial Guinea': 80, 'Egypt': 58, 'Nicaragua': 147, 'Singapore': 177, 'Serbia': 227, 'Comoros': 105, 'United Kingdom': 70, 'Congo': 37, 'Sahara': 59, 'Greece': 81, 'Sri Lanka': 116, 'Gabon': 69, 'Botswana': 31}
country_list = ('Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central Africa', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Faroe Islands', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey and Alderney', 'Guinea', 'Guinea Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk', 'North Korea', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Sahara', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre & Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome And Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican', 'Venezuela', 'Vietnam', 'Virgin Islands of the United States', 'Wallis & Futuna', 'Yemen', 'Zambia', 'Zimbabwe')
usa_state_dict = {'__all__': 0, 'Mississippi': 3390, 'Palau': 3637, 'Oklahoma': 3402, 'Delaware': 3373, 'Minnesota': 3389, 'Illinois': 3379, 'Arkansas': 3369, 'New Mexico': 3397, 'Indiana': 3380, 'Maryland': 3386, 'Louisiana': 3384, 'Idaho': 3378, 'Wyoming': 3416, 'Federated States of Micronesia': 3632, 'Tennessee': 3408, 'Arizona': 3368, 'Iowa': 3381, 'Michigan': 3388, 'Kansas': 3382, 'Utah': 3410, 'Virginia': 3412, 'Oregon': 3403, 'Connecticut': 3372, 'Montana': 3392, 'California': 3370, 'Massachusetts': 3387, 'West Virginia': 3414, 'South Carolina': 3406, 'New Hampshire': 3395, 'Wisconsin': 3415, 'Vermont': 3411, 'Georgia': 3376, 'North Dakota': 3400, 'Pennsylvania': 3404, 'Puerto Rico': 3636, 'Florida': 3375, 'Alaska': 3367, 'Kentucky': 3383, 'Hawaii': 3377, 'Marshall Islands': 3634, 'Nebraska': 3393, 'Missouri': 3391, 'Ohio': 3401, 'Alabama': 3366, 'New York': 3398, 'American Samoa': 3631, 'Virgin Islands': 3638, 'South Dakota': 3407, 'Colorado': 3371, 'New Jersey': 3396, 'Guam': 3633, 'Washington': 3413, 'North Carolina': 3399, 'District of Columbia': 3374, 'Mariana Islands': 3635, 'Texas': 3409, 'Nevada': 3394, 'Maine': 3385, 'Rhode Island': 3405}
usa_state_list = ('__all__', 'Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Federated States of Micronesia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Mariana Islands', 'Marshall Islands', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming')
default_subject = 'Hello, dear $name !!!'
class User(object):
    def __init__(self, name, userid, key):
        self.name = name
        self.userid = userid
        self.key = key
        
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.userid, self.key)
class SpiderGUI(object):
    def __init__(self):
        self.sawe_search = 1
        self.sawe_country ='' 
        self.sawe_state = ''
        self.sent = 0
        self.total = 0
        self.time = 0
        self.timeout = 30
        self.minChars = 200
        self.run = False
        self._run = False
        self.cookies_file = 'cookies.json'
        letter = ur'letter.txt'
        self.table_name = 'default'
        
        self.engine = create_engine('sqlite:///database.db', echo=False)
        Session = sessionmaker(bind=self.engine)
        Session.configure(bind=self.engine)
        self.metadata = MetaData()
        self.session = Session()
        self.table = Table(self.table_name, self.metadata,Column('id', Integer, primary_key=True),Column('name', String), Column('fullname', String),Column('userid', String),Column('key', String))
        self.metadata.create_all(self.engine)
        mapper(User, self.table)
        
        self.g = Grab()
        self.tk = Tk()
        self.note = ttk.Notebook(self.tk)
        self.tk.geometry('650x306')
        #self.tk.iconbitmap(default='icon.ico')
        self.tk.title("Spyder search engine")
        
        ### ВЕРХНЯЯ ПАНЕЛЬ ### 
        
        self.Frame = Frame(self.tk, width = 460, height = 62)
        self.Frame.pack(side = 'top', fill = 'x')
        # строка статуса рассылки
        
        self.lb = ttk.Label(self.Frame, text='Welcome to the afa sender ...')
        self.lb.place(x = 3, y = 3)
        self.lb8 = ttk.Label(self.Frame, text='00:00:00', font="Arial 25 bold")
        self.lb8.place(x = 25, y = 20)
        # строка прогресс бара
        
        self.lb1 = ttk.Label(self.Frame, text='waiting ...')
        self.lb1.place(x = 400, y = 0, width = 250)
        
        # прогресс бар

        
        self.Bar = ttk.Progressbar(self.Frame, orient=HORIZONTAL, mode='determinate', length=250)
        self.Bar.place(x = 400, y = 17)
        # кнопка старт/стоп
        
        self.runBtn = ttk.Button(self.Frame, text = 'Start',command=self.spider_run)
        self.runBtn.place(x = 495, y = 38)
        # кнопка выход
        
        self.quitBtn = ttk.Button(self.Frame, text = 'Quit',command=self.spider_quit)
        self.quitBtn.place(x = 575, y = 38)
        # вкладки
        
        self.tab1 = Frame(self.note)
        self.tab3 = Frame(self.note)
        self.note.add(self.tab1, text = "Main")
        self.note.add(self.tab3, text = "Letter")
        self.note.pack(fill="both", expand="yes", side = 'top')
        # testMode = True
        
        self.mode = BooleanVar()
        self.modeBtn = ttk.Checkbutton(self.tab1, text="Test mode", variable=self.mode, onvalue=True, offvalue=False).place(x = 3, y = 3)
        # enable logging
        
        self.log = BooleanVar()
        #self.log.set(True)
        self.logBtn = ttk.Checkbutton(self.tab1, text='Enable logging',variable=self.log, onvalue=True, offvalue=False).place(x = 3, y = 23)
        # load_cookies
        
        self.cookies = BooleanVar()
        self.cookies.set(True)
        self.cookiesBtn = ttk.Checkbutton(self.tab1, text="load cookies",variable=self.cookies, command=self.lform, onvalue=True, offvalue=False).place(x = 3, y = 43)
        #   fromAge
        
        lb3 = ttk.Label(self.tab1, text="Age from search").place(x = 3, y = 75)
        self.from_age = IntVar()
        self.from_age.set(18)
        self.from_ageBox = ttk.Combobox(self.tab1,width = 2,textvariable=self.from_age)
        self.from_ageBox['values'] = range(18,100)
        self.from_ageBox.place(x =150 , y = 75)
        #   toAge
        
        lb4 = ttk.Label(self.tab1, text="to").place(x = 200, y = 75)
        self.to_age = IntVar()
        self.to_age.set(99)
        self.to_ageBox = ttk.Combobox(self.tab1,width = 2,textvariable=self.to_age)
        self.to_ageBox['values'] = range(18,100)
        self.to_ageBox.place(x =225 , y = 75)
        # del database
        
        self.delbaseBtn = ttk.Button(self.tab1, text = 'del database',command=self.delbase).place(x = 450, y = 175)
        # state
        
        self.lb7 = ttk.Label(self.tab1,text="State for search")
        self.state = StringVar()
        self.stateBox = ttk.Combobox(self.tab1,width = 25,textvariable=self.state)
        
        self.lb7.place(x = 3, y = 125)
        self.state.set('__all__')
        self.stateBox['values'] = usa_state_list
        self.stateBox.place(x = 153, y = 125)
        # country
        
        lb5 = ttk.Label(self.tab1,text="Country for search").place(x = 3, y = 100)
        self.country = StringVar()
        self.country.set('United States')
        self.countryBox = ttk.Combobox(self.tab1,width = 25,textvariable=self.country)
        self.countryBox['values'] = country_list
        self.countryBox.bind('<<ComboboxSelected>>', self.set_state)
        self.countryBox.place(x = 153, y = 100)
        # run search
        
        self.searchBtn = ttk.Button(self.tab1, text = 'run search',command=self.search_run)
        self.searchBtn.place(x = 550, y = 175)
        # text box
        
        txtpanelFrame = Frame(self.tab3, bg = 'white')
        txtpanelFrame.pack(side = 'bottom', fill = 'x')
        self.textbox = Text(self.tab3, font='Verdana 10', wrap='word')
        self.textbox.insert('1.0', 'Message header must contain the variable "$name" instead of the recipient!')
        scrollbar = Scrollbar(self.tab3)
        scrollbar['command'] = self.textbox.yview
        self.textbox['yscrollcommand'] = scrollbar.set
        self.textbox.pack(side = 'left', fill = 'both', expand = 1) 
        scrollbar.pack(side = 'right', fill = 'y')
        
        tloadBtn = ttk.Button(txtpanelFrame, text = 'Load',command=self.load_letter)
        tloadBtn.pack(side = 'right')
        
        tloadBtn = ttk.Button(txtpanelFrame, text = 'Save',command=self.save_letter)
        tloadBtn.pack(side = 'right')
        
        tloadBtn = ttk.Button(txtpanelFrame, text = 'Apply',command=self.apply_letter)
        tloadBtn.pack(side = 'right')
        # lady id
        
        lb9 = ttk.Label(self.tab1, text='ladyId:').place(x = 450, y = 3)
        self.ladyId = ttk.Entry(self.tab1)
        #self.ladyId.insert(0,'100820')
        self.ladyId.place(x = 500, y = 3)
        ### ПАНЕЛЬ СТАТУСА ###

        self.lb6 = ttk.Label(self.tab1, text="Waiting for user activity ...")
        self.lb6.pack(side = 'bottom', fill = 'x')
    def ladyId_set(self):
        if self.ladyId.get()!='':
            return self.ladyId.get()
        else:
            print 'ENTER LADY ID, EMPTY !!!'
            self.run = False
            self._run = False     
    def delbase(self):
        try:
            print 'Deleting database ...'
            self.lb6["text"] = 'Deleting database ...'
            c = self.session.query(User).count()
            if c !=0:
                self.table.drop(self.engine)
                self.session.commit()
                self.metadata.create_all(self.engine)
                print 'OK ...'
            else:
                print 'Database is empty...'
            self.session.commit()
        except Exception:
            print 'Database acess error'
    def applybase(self):
        #self.delbase()
        base_list.append(self.base_name.get())
        print 'Create a new database ...'
        self.lb6["text"] = 'Create a new database %s...' % self.table_name
        self.baseBox['values'] = base_list
    def set_state(self,*args):
        print self.country.get()
        if self.country.get() == 'United States':
            self.lb7.place(x = 3, y = 125)
            self.state.set('__all__')
            self.stateBox['values'] = usa_state_list
            self.stateBox.place(x = 153, y = 125)
        else:
            self.lb7.place_forget()
            self.stateBox.place_forget()
    def country_set(self):
        return country_dict[self.country.get()]
    def state_set(self):
        if self.country.get() == 'United States' and self.state.get() != '__all__':
            string =  '--state-'+str(usa_state_dict[self.state.get()])
            return string
        else:
            return ''
    def start(self):
        #self.self_basetes()
        #self.unicode_test()
        self.tk.mainloop()
    def unicode_test(self):
        print "self.unicode_test()"
        self.ladyId.insert(0,'100820')
        self.log.set(True)
        self.men_search(62)
        self.self_basetes()
    def test(self):
        try:
            self.g.go('http://office.loveme.com')
        except Exception:
            print>>sys.__stderr__, '** Could not connect to the network **\n** Check you internet connection **'
            sys.exit(1)
        self.ladyId_set()
        tmp = self.textbox.get('1.0', 'end')
        if len(tmp) < self.minChars:
			self.run = False
			print 'LOAD A VALID LETTER !!!'
			print '****'*7
    def spider_run(self):
        if self.run == False:
			self.run = True
			self.test()
			self.runBtn["text"] = "Stop"
			if self.run:
			    threading.Thread(target=self.spider).start()
			else:
			    self.runBtn["text"] = "Start"
        else:
            print '\nKilling spider ...'
            self.lb6["text"] = 'Killing spider ...'
            self.runBtn["text"] = "Start"
            self.run = False 
            self.sent=0
    def spider_quit(self):
        print ('Quit (%d) ' % self.mode.get())
        self.tk.destroy()
        sys.exit(1)
    def check_base(self):
        try:
            c = self.session.query(User).filter_by(key='0').count()
            if c != 0:
                self.total = c
                print 'Database contains %s records ...' % self.total
            else:
                print '** Database is empty, Run search !!! **'
                self.lb["text"] = 'Database is empty, run search !!!'
                self.run = False
            self.session.commit()
        except Exception:
            print 'Database acess error'
    def spider(self):
        self.set_mode()
        self.set_log()
        self.set_timeout()
        self.load_cookies()
        self.check_base()
        runtime = 0
        _iter = 0
        self.letter = self.textbox.get('1.0', 'end')
        mes = self.letter.split('\n')
        s = mes[0]
        if s.find('$name') != -1:
            self._subject = s
        else:
            self._subject = default_subject
            print 'Please enter a valid email subject!'
            self.lb6["text"] = 'Please enter a valid email subject!'
        del mes[0]
        self.body = '\n'.join(mes)
        for instance in self.session.query(User).filter_by(key='0'):
            if self.run:
                _tmp = time.clock()
                _iter += 1
                self.name = instance.name
                self.menId = instance.userid
                self.key = instance.key
                s = Template(self._subject)
                self.subject = s.substitute(name = self.name)
                try:
                    self.send_letter()
                except Exception:
					print 'Sender function crashed, try again after 20s ...'
					time.sleep(20)
					self.send_letter()
                instance.key = True
                self.session.commit()
                run = time.clock()-_tmp
                runtime += run
                fulltime = (runtime / _iter) * self.total
                #fulltime = (int(runtime)/ int(_iter)) * int(self.total)
                remaining = (fulltime - runtime)
                self.Bar["maximum"] = fulltime
                self.Bar["value"] = runtime
                self.lb["text"] = 'Sent letters to %s of %s men %s men missing' % (_iter,self.total,(_iter-self.sent))
                self.lb8["text"] = self.seconds_to(remaining)
                self.lb1["text"] = 'Need %s / Last %s / Run %s' % (self.seconds_to(fulltime), self.seconds_to(remaining), self.seconds_to(runtime))
                print 'Time need %s, remaining %s, process run %s cpu %s' % (self.seconds_to(fulltime), self.seconds_to(remaining), self.seconds_to(runtime),self.seconds_to(run))
            else:
                print ' *** ' * 16
                print 'Session aborted, exit ...'
                break
        print '\nSending letters completed ...'
        print ' *** ' * 16
        self.lb6["text"] = 'Sending letters completed ...'
        self.runBtn["text"] = "Start"
        self.lb8["text"] = self.seconds_to(0)
        self.run = False
        self.sent=0
        self.session.commit()
    def self_basetes(self):
        for instance in self.session.query(User).all():
            print instance.userid,  repr(instance.name), instance.key
    def seconds_to(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))
    def send_letter(self):
        self.session.commit()
        print '\n================================ RESTART ================================\n'
        print '** Sending letter to %s %s ... **' % (repr(self.name),self.menId)
        self.lb6["text"] = '** Sending letter to %s %s ... **' % (repr(self.name),self.menId)
        uri = 'http://office.loveme.com/send?mid='+str(self.menId)+'&wid='+str(self.ladyId_set())+'&_RETURN=http%3A%2F%2Foffice.loveme.com%2Fsearch_men_results%3Fq%3D'+str(self.from_age.get())+'--age_to-' + str(self.to_age.get())+'--country-'+str(self.country_set())+'%26women_id%3D'+str(self.ladyId_set())
        try:
            print 'GET URL'
            self.g.go(uri)
            print 'Self network test OK'
        except Exception:
            print 'Exept error, host is down, try get %s page after timeout 5s ...' % repr(self.name)
            time.sleep(5)
            print 'Try again ...'
            self.g.go(uri)
            print 'OK'
        if self.g.search(u'User does not want to receive intro letters!') or self.g.search(u'Already sent an intro letter to this man.'):
            print ('** BAD user %s id %s **' % (repr(self.name),self.menId) )
            self.lb6["text"] = '** BAD user %s id %s **' % (repr(self.name),self.menId)
            return False
        self.g.set_input('mbox_subject', self.subject)
        self.g.set_input('mbox_body', self.body)
        if self.mode.get():
            print '** Sending letter to %s %s (TEST MODE) ... **' % (repr(self.name),self.menId)
            self.lb6["text"] = '** Sending letter to %s %s (TEST MODE) ... **' % (repr(self.name),self.menId)
            self.sent+=1
        else:
            try:
                print 'SUBMIT REQUEST'
                self.g.submit()
            except Exception:
                print 'SERVER NOT RESPONSE!!! TIMEOUT 5s ..'
                time.sleep(5)
                print 'GO NEXT ..'
                self.g.go(uri)
                print 'HOOK OK  ..'
            print 'SUBMIT OK'
            self.sent+=1
    def load_cookies(self):
        cookies = self.cookies_file
        try:
            self.g.load_cookies(cookies)
        except Exception:
            print>>sys.__stderr__, '** Could not load cookie **\n** Click login check botton**'
            self.lb["text"] = 'Need login !!!'
            sys.exit(1)   
        print ('Loading cookie from file (%s) ...' % cookies)
        self.lb6["text"] = 'Loading cookie from file (%s) ...' % cookies
    def lform(self):
        self.form = Tk()
        self.form.geometry('200x100')
        #self.form.iconbitmap(default='icon.ico')
        self.form.title("Login")
        label = ttk.Label(self.form, text='login:', font='Arial 10 bold').place(x = 0, y = 5)
        label2 = ttk.Label(self.form, text='pass:', font='Arial 10 bold').place(x = 0, y = 25)
        self.entry = ttk.Entry(self.form)
        self.entry2 = ttk.Entry(self.form, show='*')
        self.entry.insert(0,'Luga8')
        self.entry2.insert(0,'jNGRtxr5')
        self.entry.place(x = 50, y = 5)
        self.entry2.place(x = 50, y = 30)
        Btn = ttk.Button(self.form, text = 'login',command=self.login).place(x = 75, y = 65)
        self.form.mainloop()
    def login(self):
        print 'Login ...'
        print('current value is %s' % self.entry.get())
        print('current value is %s' % self.entry2.get())
        self.g.go('http://office.loveme.com/assign_women')
        self.g.set_input('logins_ident', self.entry.get())
        self.g.set_input('logins_password', self.entry2.get())
        self.g.set_input('remember_login', '1')
        self.g.submit()
        cookies = self.cookies_file
        self.g.dump_cookies(cookies)
        self.cookies.set(True)
        self.form.destroy()
    def set_timeout(self):
        print 'Setting timeout to (%s) ...' % self.timeout
        self.lb6["text"] = 'Setting timeout to (%s) ...' % self.timeout
        self.g.setup(connect_timeout=self.timeout)
        self.g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30), (60, 100)))
    def set_log(self):
        if self.log.get() == True:
            print 'Loging enabled ...'
            self.lb6["text"] = 'Loging enabled ...'
            logger = logging.getLogger('grab')
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)
            self.g.setup(log_dir='log')
            self.g.setup(debug_post='True')
            self.log.set(False)
            try:
                os.mkdir('log')
            except Exception:
                shutil.rmtree('log')
                os.mkdir('log')
                print 'Dir "log" already exsit or maby ome error ...'
    def set_mode(self):
        if self.mode.get():
            print 'Testing mode enabled ...'
            self.lb6["text"] = 'Testing mode enabled ...'
    def search_run(self):
        if self._run == False:
            self._run = True
            self.test()
            self.searchBtn["text"] = "Stop"
            if self._run:
				threading.Thread(target=self.search).start()
            else:
				self.searchBtn["text"] = "run search"
        else:
            self._run = False
    def set_age(self):
        if self.from_age.get() <= self.to_age.get():
            print ('Age from search set to %d ...' % self.from_age.get())
            print ('Age to search set to %d ...' % self.to_age.get())
            self.lb6["text"] = 'Age from search set to %d ...' % self.from_age.get()
            self.lb6["text"] = 'Age to search set to %d ...' % self.to_age.get()
        else:
            print 'Specify the correct settings for search !!!'
            self.from_age.set(18)
    def search_restore(self):
        print  'RESTORE SEARCH (page (%s), country (%s), state (%s))' % (self.sawe_search, self.sawe_country, self.sawe_state)
        if self.sawe_search != 1 and self.country_set() == self.sawe_country:
			if self.state_set() == self.sawe_state:
				print 'RESTORE SEARCH OK, page (%s) state_set (%s) sawe_state (%s)' % (self.sawe_search,self.state_set(),self.sawe_state)
			else:
				print 'RESTORE SEARCH (New search begin ...)'
				self.sawe_search = 1
        else:
			print 'RESTORE SEARCH (New search begin ...)'
			self.sawe_search = 1
    def search_backup(self, page):
        if self.sawe_search == page:
            print 'SEARCH BACKUP (Search is done, current page (%s))' % self.sawe_search
            self.sawe_search = 1
            self.sawe_country = ''
            self.sawe_state = ''
        else:
            print 'SEARCH BACKUP (Sawe search result, sawe_search != page (%s))' % self.sawe_search
            self.sawe_country = self.country_set()
            self.sawe_state = self.state_set()
            print 'SEARCH BACKUP (sawe_country (%s), sawe_state (%s))'% (self.sawe_country, self.sawe_state)
        self.session.commit()	
    def search(self):
        print '\n================================ RESTART ================================\n'
        print 'Running search... '
        self.lb6["text"] = "Running search... "
        self.lb["text"] = "Running search... "
        self.set_log()
        self.set_timeout()
        self.load_cookies()
        self.set_age()
        runtime = 0
        _iter = 0
        uri = 'http://office.loveme.com/search_men_results~pg1?q=age_from-'+ str(self.from_age.get())+'--age_to-'+ str(self.to_age.get())+'--country-'+str(self.country_set())+str(self.state_set())+'&women_id='+str(self.ladyId_set())
        try:
            self.g.go(uri)
            print 'Self network test OK'
        except Exception:
            print 'Exept error, host is down, try after timeout 10s ...'
            time.sleep(10)
            self.g.go(uri)
        #
        try:
            q = self.g.doc.select('//div[@class="f_left"]/b')
            found = q[2].text()
            found = int(found)
            page = (found/20)+1
        except Exception:
            print 'Exception in parse page total'
            page=1
        self.search_restore()
        for x in range(self.sawe_search,page+1):
            if self._run:
                xtmp = x
                _tmp = time.clock()
                _iter += 1
                try:
                    self.men_search(x)
                except Exception:
					print 'Search function crashed, try again after 10s ...'
					time.sleep(10)
					self.men_search(x)
                run = time.clock()-_tmp
                runtime += run
                fulltime = (runtime / _iter) * (page-self.sawe_search)
                remaining = (fulltime - runtime)
                self.Bar["maximum"] = fulltime
                self.Bar["value"] = runtime
                self.lb["text"] = 'Parsing page '+str(self.sawe_search+_iter-1)+' from '+str(page)+' ...'
                self.lb8["text"] = self.seconds_to(remaining)
                self.lb1["text"] = 'Need %s / Last %s / Run %s' % (self.seconds_to(fulltime), self.seconds_to(remaining), self.seconds_to(runtime))
                print 'Time need %s, remaining %s, process run %s' % (self.seconds_to(fulltime), self.seconds_to(remaining), self.seconds_to(runtime))
            else:
                print "\nStop searching ..."
                self.sawe_search = x
                break
        self.sawe_search = xtmp
        print ' *** ' * 16
        self.lb6["text"] = 'Search over, found (%d) men ...' % self.total
        self.lb["text"] = 'Search over, found (%d) men ...' % self.total
        self.searchBtn["text"] = "Search"
        self.lb8["text"] = self.seconds_to(0)
        self.lb1["text"] = 'Need %s / Last %s / Run %s' % (self.seconds_to(0), self.seconds_to(0), self.seconds_to(0))
        self._run = False
        self.search_backup(page)
    def men_search(self, x):
        uri = 'http://office.loveme.com/search_men_results~pg'+str(x)+'?q=age_from-'+ str(self.from_age.get())+'--age_to-' + str(self.to_age.get())+'--country-'+str(self.country_set())+str(self.state_set())+'&women_id='+str(self.ladyId_set())
        try:
            self.g.go(uri)
            print 'Self network test OK'
        except Exception:
            print 'Exept error, host is down, try after timeout 10s ...'
            time.sleep(10)
            self.g.go(uri)
        if self.g.search(u'Your search returned no results. Please try again using different criteria'):
            print ('** Search over, found (%d) men **' % self.total)
            self.session.commit()
            self._run = False
            self.searchBtn["text"] = "Search"
        else:
            h = self.g.doc.select('//p[@class="bold"]/a')
            h = filter(lambda x: x != '', h)
            self.total += len(h)-1
            for x in range(1,len(h)):
                ur = h[x].attr('href')
                self.men_id = re.sub('[\D]','',ur)
                self.name = h[x].attr('title').split(' ')[0]
                self.key = False
                self.session.add(User(self.name , self.men_id, self.key ))
                print ('Adding a user %s (%s) to the database ...' % (repr(self.name), self.men_id))
                self.lb6["text"] = 'Adding a user %s (%s) to the database ...' % (repr(self.name), self.men_id)
        self.session.commit() 
    def load_letter(self): 
        fn = tkFileDialog.Open(self.tk, filetypes = [('*.txt files', '.txt')]).show()
        if fn == '':
            return
        self.textbox.delete('1.0', 'end') 
        self.textbox.insert('1.0', open(fn, 'rt').read())
        self.lb6["text"] = "Loading letter complete... "
    def save_letter(self):
        fn = tkFileDialog.SaveAs(self.tk, filetypes = [('*.txt files', '.txt')]).show()
        if fn == '':
            return
        if not fn.endswith(".txt"):
            fn+=".txt"
        open(fn, 'wt').write(self.textbox.get('1.0', 'end'))
        self.lb6["text"] = "Saving letter complete... "  
    def apply_letter(self):
        print "Apply changes ..."
        self.letter = self.textbox.get('1.0', 'end')
        print self.letter
        self.lb6["text"] = "Applying changes complete... "
if __name__ == '__main__':
    gui = SpiderGUI()
    gui.start()
