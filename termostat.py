import serial.tools.list_ports
import serial
import PySimpleGUI as sg
ser = None  #Global tanımlanmalı
seri_baglandi = False
isitma_durum = False 
sogutma_durum = False  
min_sicaklik = 0
max_sicaklik = 0  
ara_bolge = 0  
set_flag = False
#! Port Listeleme
def serial_ports():
    ports = serial.tools.list_ports.comports()
    print(ports)
    seri_port = []
    for p in ports:
        print(p.device)
        seri_port.append(p.device)
    print(seri_port)
    return seri_port
########################
def serial_baglan():
    com_deger = value[0]
    baud_deger = value[1]
    print("Baud Deger", value[1])
    global ser
    ser = serial.Serial(com_deger, baud_deger, timeout=0, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE , bytesize = serial.EIGHTBITS, rtscts=0)
    window["-BAGLANDI_TEXT-"].update('Bağlandı...')


def isitma():
    global isitma_durum

    if (isitma_durum == True):
        ser.write('ISK'.encode('Ascii'))
        window["ISITMA"].update("ISITMA AÇ", button_color="GREEN")
        isitma_durum = False 
    elif (isitma_durum == False):
        ser.write('ISA'.encode('Ascii')) 
        window["ISITMA"].update("ISITMA KAPA", button_color="RED")
        isitma_durum = True 

def sogutma():
    global sogutma_durum

    if (sogutma_durum == True):
        ser.write('STK'.encode('Ascii'))
        window["SOGUTMA"].update("SOĞUTMA AÇ", button_color="GREEN")
        sogutma_durum = False 
    elif (sogutma_durum == False):
        ser.write('STA'.encode('Ascii')) 
        window["SOGUTMA"].update("SOĞUTMA KAPA", button_color="RED")
        sogutma_durum = True 
def sicaklik_ayar(sensor_data1):
    aralik = 1
    try:
        sensor_data1 = float(sensor_data1)
    except ValueError:
        print("Çeviri Hatasi")
        return
    if (sensor_data1 < min_sicaklik and isitma_durum == False):
        isitma()
    elif (sensor_data1 > (min_sicaklik + aralik) and isitma_durum == True):
        isitma() 
    elif (sensor_data1 > max_sicaklik and sogutma_durum == False):
        sogutma()
    elif (sensor_data1 < (max_sicaklik - aralik) and sogutma_durum == True):
        sogutma()
    else:
        pass 

   
    if (sensor_data1 < min_sicaklik):
        ser.write('L1A'.encode('Ascii'))
        ser.write('L2K'.encode('Ascii'))
    elif (sensor_data1 > max_sicaklik):
        ser.write('L1K'.encode('Ascii'))
        ser.write('L2A'.encode('Ascii'))
    else:
        ser.write('L1A'.encode('Ascii'))
        ser.write('L2A'.encode('Ascii'))
        


def ayarla():

    global min_sicaklik
    global max_sicaklik
    global set_flag
    en_yuksek = window["enyuksek"].get()
    if ("." in en_yuksek):
        en_yuksek = float(en_yuksek)
    else:
        en_yuksek = int(en_yuksek)
    en_dusuk = window["endusuk"].get()
    if ("." in en_dusuk):
        en_dusuk = float(en_dusuk)
    else:
        en_dusuk = int(en_dusuk)

    print("En Yüksek", en_yuksek)
    print("En Düşük ", en_dusuk)
    min_sicaklik = en_dusuk
    max_sicaklik = en_yuksek
    set_flag = True 
sg.theme("Reddit")

sensor_layout = [[sg.Text(text="Sensör 1:"), sg.Input(default_text="0", font=("Arial Black", 13), key="sensor1", size=(5,1)),
                sg.Text(text="Sensör 2:"), sg.Input(default_text="0", font=("Arial Black", 13), key="sensor2", size=(5,1)),
                sg.Text(text="Sensör 3:"), sg.Input(default_text="0", font=("Arial Black", 13), key="sensor3", size=(5,1)),
                sg.Text(text="Sensör 4:"), sg.Input(default_text="0", font=("Arial Black", 13),  key="sensor4", size=(5,1))
                ] 
                ]

manual_layout = [[sg.Button(button_text="ISITMA AÇ", button_color="GREEN", size=(32,1), key="ISITMA"), sg.Button(button_text="SOĞUTMA AÇ", button_color="GREEN", size=(33,1), key="SOGUTMA")]]

ayar_layout = [[sg.Text("En Yüksek Sıcaklık:"), sg.Input("", size=(6,1), font=("Arial Black", 13), key="enyuksek"), sg.Text("En Düşük Sıcaklık:"), sg.Input("", size=(6,1), font=("Arial Black", 13), key="endusuk"), sg.Button(button_text="AYARLA", key="AYARLA")]]

layout =[ [sg.Text("Port Seçiniz:"), sg.Combo(serial_ports(), size=(10,1)),
            sg.Text("Baud Seçiniz:"), sg.Combo(["110","300","600","1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"], default_value=9600), 
            sg.Button(button_text="Bağlan", key="-BAGLAN-", size=(10,1)) ],
            [sg.Text("", size=(10,1), key="-BAGLANDI_TEXT-")],
            [sg.Frame("Sensör", sensor_layout)],
            [sg.Frame("Manuel Kontrol", manual_layout)],
            [sg.Frame("Ayarlama", ayar_layout)]
        ]
window = sg.Window("Python Termostat", layout)

while True:
    event, value = window.read(timeout=1000) 
    if event == sg.WIN_CLOSED or event == 'Exit':
        break    
    if event == "-BAGLAN-":
        if (value[0] == ""):
            sg.popup("Bir Port Seçiniz!", title="Hata", custom_text="Tamam") 
        elif (value[1] == ""):
            sg.popup("Baud Oranını Seçiniz!", title="Hata", custom_text="Tamam")
        else:
            serial_baglan()
            seri_baglandi = True 
    if(seri_baglandi == True):
        data = ser.readline().decode('Ascii')
        if (data != ""):
            sensor_data1 = data[0:4]
            sensor_data2 = data[4:8]
            sensor_data3 = data[8:12]
            sensor_data4 = data[12:16]
            print(data)
            window["sensor1"].update(sensor_data1)
            window["sensor2"].update(sensor_data2)
            window["sensor3"].update(sensor_data3)
            window["sensor4"].update(sensor_data4)
    if event == "SOGUTMA":
        sogutma()        
    if event == "ISITMA":
        isitma()
    if event == "AYARLA":
        ayarla()
    if set_flag == True:
        sicaklik_ayar(sensor_data1)
   
window.close()