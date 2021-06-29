import PyQt5.uic
import PyQt5.QtWidgets
from ip import Ipv4NetworkCalc
import re

def ipChanged():
    ip  = window.text_ip.text()
    arr_text = ip.split('/')
    window.btn_calcIP.setEnabled(False)
    
    if is_ip(arr_text[0]):
        window.btn_calcIP.setEnabled(True)
        window.label_ip.setText(arr_text[0])
        if len(arr_text)>1:
            if is_cidr(window.edit_cidr.text()) and is_ip(arr_text[0]):
                window.btn_calcIP.setEnabled(True)
            window.edit_cidr.setText(arr_text[1])
    else:
        window.btn_calcIP.setEnabled(False)

def cidrChanged():
    if is_cidr(window.edit_cidr.text()):
        window.btn_calcIP.setEnabled(True)
        window.edit_Mask.setText(mascarado_prefixo(window.edit_cidr.text()))
        print(mascarado_prefixo(window.edit_cidr.text()))
    else:
        window.btn_calcIP.setEnabled(False)
        

def maskChanged():
    m = window.edit_Mask.text()
    mas = m.split('.')
    if len(mas)==4 and mas[3]!='':
        cidr = prefixo_mascara(ip_decimal_binario(m))
        window.edit_cidr.setText(str(cidr))
        
    
def calcula():
    ip  = window.text_ip.text()
    arr_text = ip.split('/')
    maskChanged()
    window.text_ip.setText(arr_text[0]+"/"+window.edit_cidr.text())
    objIp = Ipv4NetworkCalc(ip=arr_text[0], mascara = window.edit_Mask.text())
    setValores(objIp.fetAll())

def setValores(obj):
    print(obj)
    window.label_ip.setText(obj.get('ip'))
    window.label_cidr.setText(str(obj.get('prefixo')))
    window.label_rede.setText(obj.get('rede'))
    window.label_mascara.setText(obj.get('mascara'))
    window.label_broadcast.setText(obj.get('broadcast'))
    window.label_hosts.setText(str(obj.get('numero_ips')))

def ip_prefixo(socket):
        ip_prefixo_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}$')
        if not ip_prefixo_regexp.search(socket):
            return
        divide_ip = socket.split('/')
        return ({"ip":divide_ip[0],"cidr":divide_ip[1]})
        

def is_ip(ip):
    ip_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')
    if ip_regexp.search(ip):
        return True
    return False
    
def is_cidr(cidr):
        cidr_regexp = re.compile('^[0-9]{1,2}$')
        if cidr_regexp.search(cidr) and int(cidr)<=32 and int(cidr)>1:
            return True
        return False
    
def prefixo_mascara(mask):
        mascara_bin = mask.replace('.','')
        conta = 0
        for bit in mascara_bin:
            if bit == '1':
                conta += 1

        return conta 

def mascarado_prefixo(cidr):
        mascara_bin = ''
        for i in range(32):
            if i < int(cidr):
                mascara_bin += '1'
            else:
                mascara_bin += '0'
        return ip_binario_ip_decimal(mascara_bin)   
    
def ip_binario_ip_decimal(ip=''):
    novo_ip = str(int(ip[0:8], 2))+'.'
    novo_ip += str(int(ip[8:16], 2)) + '.'
    novo_ip += str(int(ip[16:24], 2)) + '.'
    novo_ip += str(int(ip[24:32], 2))
    return novo_ip

def ip_decimal_binario(ip):
        bloco_ip = ip.split('.')
        ip_bin = []

        for bloco in bloco_ip:
            binario = bin(int(bloco))
            binario = binario[2:].zfill(8)
            ip_bin.append(binario)

        ip_bin = '.'.join(ip_bin)
        return ip_bin

app= PyQt5.QtWidgets.QApplication([])
window=PyQt5.uic.loadUi('telaip.ui')
window.text_ip.setText('192.168.0.1/24')
window.edit_cidr.setText('24')
window.edit_Mask.setText('255.255.255.0')
window.text_ip.textChanged.connect(ipChanged)
window.edit_cidr.textChanged.connect(cidrChanged)
window.btn_calcIP.clicked.connect(calcula)

window.show()
app.exec()