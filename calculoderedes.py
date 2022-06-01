from re import *

class Calcipv4:
    def __init__(self, ip, mascara=None, prefixo=None):
        self.ip = ip
        self.mascara = mascara
        self.prefixo = prefixo

    @property
    def ip(self):
        return self._ip

    @property
    def mascara(self):
        return self._mascara

    @property
    def prefixo(self):
        return self._prefixo

    @ip.setter
    def ip(self, valor):
        self._ip = valor
        print('IP ->',valor)
        self._ip_binario = self.ip_para_bin(valor)

    @mascara.setter
    def mascara(self, valor):
        if not valor:
            return

        if not self._valida_ip(valor):
            raise ValueError('Máscara inválida')
        self._mascara = valor


    @prefixo.setter
    def prefixo(self, valor):
        if not valor:
            return

        if valor >= 32:
            raise ValueError('Prefixo máximo - 32bits')
        self._prefixo = int(valor)

    def mascara_octeto(self):
        mascara_octeto = [] #lista com mascara dos octetos do ip
        nun_1 = ('1'*self.prefixo).ljust(32, '0')
        n = 8
        self.lista_mascara_octal = [nun_1[i:i+n] for i in range(0, 32, 8)]
        hosts = (2**(self.lista_mascara_octal[3].count('0')))-2
        for c in range(4):
            s = 0
            for i, x in enumerate(self.lista_mascara_octal[c]):
                if i == 0:
                    if x == '1':
                        s += 128
                elif i == 1:
                    if x == '1':
                        s += 64
                elif i == 2:
                    if x == '1':
                        s += 32
                elif i == 3:
                    if x == '1':
                        s += 16
                elif i == 4:
                    if x == '1':
                        s += 8
                elif i == 5:
                    if x == '1':
                        s += 4
                elif i == 6:
                    if x == '1':
                        s += 2
                elif i == 7:
                    if x == '1':
                        s += 1
            mascara_octeto.append(s)
        print('Mascara -> ',end='')
        for i, c in enumerate(mascara_octeto):
            if i < 3:
                print(f'{c}.', end='')
            else:
                print(c)
        print(f'Hosts -> {hosts}')

    def ips(self):
        blocos = self._ip_binario
        bloco_rede = int(self._ip_broadcast_trans(blocos[3]), 2)
        bloco_broadcast_ip = int((self.inversor(('1'*self.prefixo).ljust(32, '0')))[24:], 2)
        bloco_ultimo_ip = int((self.inversor(('1'*self.prefixo).ljust(32, '0')))[24:], 2)-1
        self.ultimo_ip = f'{self.bin_para_ip(blocos[:3])}.{bloco_ultimo_ip}'
        self.broadcast_ip = f'{self.bin_para_ip(blocos[:3])}.{bloco_broadcast_ip}'
        self.rede = f'{self.bin_para_ip(blocos[:3])}.{bloco_rede}'
        print('IP broadcast ->',self.broadcast_ip)
        print('Ultimo IP ->',self.ultimo_ip)
        print('Rede ->',self.rede)

    @staticmethod
    def ip_para_bin(ip):
        blocos = ip.split('.')
        blocos_bin = [str(bin(int(x)))[2:].zfill(8) for x in blocos]
        return blocos_bin

    @staticmethod
    def bin_para_ip(bin):
        blocos = bin #transformar o ip binário pra ip inteiro
        blocos_int = [str(int(x, 2)) for x in blocos]
        return '.'.join(blocos_int)


    @staticmethod
    def inversor(lista):
        invertido = []
        for i, c in enumerate(lista):
            if c == '1':
                invertido.insert(i, '0') #criei essa função pra inverter os bits de rede pra calcular o ultimo ip
            else:
                invertido.insert(i, '1')
        return ''.join(invertido)

    @staticmethod
    def _valida_ip(ip):
        regexp = compile(r'^([0-9].{1,3}.[0-9].{1,3}.[0-9].{1,3}.[0-9].{1,3}$)')
        if regexp.search(ip):
            return True

    @staticmethod
    def _ip_broadcast_trans(ip):
        ip_broadcast = []
        for i, c in enumerate(ip):
            if i >= 2:
                ip_broadcast.append('0')
            else:
                ip_broadcast.append(c)
        return ''.join(ip_broadcast)
