"""
User Object
"""

import sys

class User(object):
    """docstring for User"""
    def __init__(self):
        self.numcomu = None
        self.numprop = None
        self.nombre = None
        self.via = None
        self.calle = None
        self.numcalle = None
        self.pobla = None
        self.provincia = "NAVARRA"
        self.piso = None
        self.cpostal = None
        self.banco = None
        self.sucursal = None
        self.dccuenta = None
        self.numcta= None

    def write(self, file_out):
        # Line's width
        reg = [' ']*612
#1   NUMCOMU     Numerico    3               No
        reg[0:3] = "%3d" % self.numcomu
#2   NUMPROP     Numerico    4               No
        reg[3:7] = "%4d" % self.numprop
#3   DESGLOSE    Numerico    1               No
#4   IDIOMA  Numerico    1               No
#5   LNIF    Caracter    1               No
        reg[9:10] = "0"
#6   NNIF    Caracter    8               No
        reg[10:11] = "0"
#7   CNIF    Caracter    1               No
#8   RAZON   Caracter    45              No
        data = self.nombre.encode("latin1")
#        for char in data:
#            sys.stdout.write("\\u%0.4x" % ord(char))
#        sys.stdout.write("\n")
        reg[21:66] = data + " "*(45 - len(data))
#9   NOMBRE  Caracter    30              No
        # just in case, give 45 spaces, the same for 'razon' field
        data = self.nombre.encode("latin1")
        reg[66:111] = data + " "*(45 - len(data))
#10  VIA     Caracter    2               No
        data = self.via.encode("latin1")
        reg[116:118] = data + " "*(2 - len(data))
#11  CALLE   Caracter    40              No
        data = self.calle.encode("latin1")
        reg[118:158] = data + " "*(40 - len(data))
#12  NUMCALLE    Numerico    5               No
        data = str(self.numcalle)
        reg[158:163] = " "*(5 - len(data)) + data
#13  PISO    Caracter    7               No
        data = self.piso.encode("latin1")
        reg[163:170] = data + " "*(7 - len(data))
#14  RESTODOMI   Caracter    40              No
#15  CPOSTAL     Numerico    5               No
        reg[210:215] = "%5d" % self.cpostal
#16  POBLA   Caracter    35              No
        data = self.pobla.encode("latin1")
        reg[220:255] = data + " "*(35 - len(data))
#17  PROV    Caracter    20              No
        data = self.provincia.encode("latin1")
        reg[255:275] = data + " "*(20 - len(data))
#18  TFNO    Caracter    10              No
#19  TFNO2   Caracter    10              No
#20  TFNO3   Caracter    10              No
#21  FAX     Caracter    10              No
#22  BANCO   Numerico    4               No
        reg[355:359] = "%4d" % self.banco
#23  SUCURSAL    Numerico    4               No
        reg[359:363] = "%4d" % self.sucursal
#24  DCCUENTA    Caracter    2               No
        reg[363:365] = "%2d" % self.dccuenta
#25  NUMCTA  Numerico    10              No
        reg[365:375] = "%10d" % self.numcta
#26  CORREO  Caracter    50              No
#27  MODOPAGO    Caracter    1               No
#28  TIPOPER     Caracter    1               No
#29  LUGAREXP    Caracter    40              No
#30  FECHAEXP    Fecha   8               No
#31  ESTADO  Caracter    1               No
#32  PROFESION   Caracter    40              No

        #import pdb; pdb.set_trace()
        file_out.write("".join(reg))
