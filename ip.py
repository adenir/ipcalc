import re


class Ipv4NetworkCalc():
    def __init__(self, ip='', prefixo='', mascara='',
                 rede='', broadcast='', numero_ips=''):
        self.ip = ip
        self.prefixo = prefixo
        self.mascara = mascara
        self.rede = rede
        self.broadcast = broadcast
        self.numero_ips = numero_ips

        if self.ip =='':
            raise ValueError('IP não enviado.')

        self.ip_prefixo()

        if not self.is_ip():
            raise ValueError('IP inválido.')

        if not self.prefixo and not self.mascara:
            raise ValueError("Prefixo ou máscara não enviado.")

        if self.mascara:
            self.mascara_bin  = self.ip_decimal_binario(self.mascara)
            self.prefixo_mascara()
            

        self.set_numero_hosts()
        self.set_rede_broadcast()
        self.mascarado_prefixo()

    def mascarado_prefixo(self):
        mascara_bin = ''
        for i in range(32):
            if i < int(self.prefixo):
                mascara_bin += '1'
            else:
                mascara_bin += '0'
        self.mascara = self.ip_binario_ip_decimal(mascara_bin)


    def set_rede_broadcast( self ):
        ip_bin = self.ip_decimal_binario(self.ip)
        ip_bin = ip_bin.replace('.', '')
        rede = ''
        broadcast = ''
        for conta, bit in enumerate(ip_bin):
            if conta < int(self.prefixo):
                rede += str(bit)
                broadcast += str(bit)
            else:
                rede += '0'
                broadcast += '1'
        self.rede = self.ip_binario_ip_decimal(rede)
        self.broadcast = self.ip_binario_ip_decimal(broadcast)

    def ip_binario_ip_decimal(self, ip=''):
        novo_ip = str(int(ip[0:8], 2))+'.'
        novo_ip += str(int(ip[8:16], 2)) + '.'
        novo_ip += str(int(ip[16:24], 2)) + '.'
        novo_ip += str(int(ip[24:32], 2))
        print(novo_ip)
        return novo_ip


    def set_numero_hosts(self):
        host_bits = 32-int(self.prefixo)
        self.numero_ips = pow(2, host_bits)


    def prefixo_mascara(self):
        mascara_bin = self.mascara_bin.replace('.','')
        conta = 0
        for bit in mascara_bin:
            if bit == '1':
                conta += 1
        self.prefixo = conta


    def ip_decimal_binario(self, ip=''):
        if not ip:
            ip = self.ip

        bloco_ip = ip.split('.')
        ip_bin = []

        for bloco in bloco_ip:
            binario = bin(int(bloco))
            binario = binario[2:].zfill(8)
            ip_bin.append(binario)

        ip_bin = '.'.join(ip_bin)
        return ip_bin


    def ip_prefixo(self):
        ip_prefixo_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}$')
        if not ip_prefixo_regexp.search(self.ip):
            return

        divide_ip = self.ip.split('/')
        self.ip = divide_ip[0]
        self.prefixo = divide_ip[1]

    def is_ip(self):
        ip_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')

        if ip_regexp.search(self.ip):
            return True
        return False
    
    def getIP(self):
        return self.ip
    
    def getPrefixo(self):
        return self.prefixo
    
    def getMascara(self):
        return self.mascara
    
    def getRede(self):
        return self.rede
    
    def getBroadcast(self):
        return self.broacast
    
    def getHosts(self):
        return self.numero_ips
    

    def fetAll(self):
        return {
            'ip': self.ip,
            'prefixo': self.prefixo,
            'mascara': self.mascara,
            'rede': self.rede,
            'broadcast': self.broadcast,
            'numero_ips': self.numero_ips
        }
"""
if __name__ == '__main__':
    ipv4 = Ipv4NetworkCalc(ip='10.0.125.180', prefixo='25')
    print(ipv4.fetAll())
"""
