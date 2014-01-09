"""
COMUNIDAD Object
"""
class Comunidad(object):
    """docstring for Comunidad"""
    def __init__(self):
        self.numcomu = None
        self.nombre = None
        self.nif = None
        self.direc = None
        self.codpostal = 31003
        self.banco = None
        self.sucursal = None
        self.dc = None
        self.ccuenta = None

    def parse(self, line):
        """
        Parse line
        """
        self.direc = line[28:68].strip()
        self.nombre = self.direc
        self.nif = line[4:13].strip()
        self.banco = int(line[68:72].strip())
        self.sucursal = int( line[72:76].strip() )
        try:
            self.dc = int( line[76:78].strip() )
        except ValueError:
            # could not parse dc, leave it as **
            self.dc = "**"
        self.ccuenta = int( line[78:88].strip() )

    def write(self, file_out):
        reg = []
# 1   NUMCOMU     Numerico    3               No
        reg.append("%3d" % self.numcomu)
# 2   NOMBRE  Caracter    40              No
        data = self.nombre.encode("latin1")
        reg.append(data + " "*(40 - len(data)))
# 3   NIF     Caracter    9               No
        data = self.nif.encode("latin1")
        reg.append(data + " "*(9 - len(data)))
# 4   DNIF    Caracter    1               No
        reg.append(" "*1)
# 5   SUFIJO  Numerico    3               No
        reg.append(" "*3)
# 6   DIREC   Caracter    40              No
        data = self.direc.encode("latin1")
        reg.append(data + " "*(40 - len(data)))
# 7   CODPOSTAL   Numerico    5               No
        reg.append(" "*5)
# 8   POBLACION   Caracter    30              No
        reg.append(" "*30)
# 9   PROVINCIA   Caracter    30              No
        reg.append(" "*30)
# 10  UNICONT     Numerico    3               No
        reg.append(" "*3)
# 11  PAGAADMIN   Caracter    1               No
        reg.append(" "*1)
# 12  CTAADMIN    Caracter    12              No 177
        reg.append(" "*12)
# 13  GESTOR  Numerico    1               No
        reg.append(" "*1)
# 14  FORMATOREP  Numerico    2               No
        reg.append(" "*2)
# 15  NUMPAGOSRE  Numerico    2               No
        reg.append(" "*2)
# 16  FORMATOLIQ  Numerico    2               No
        reg.append(" "*2)
# 17  TEXTOCSB    Caracter    70              No
        reg.append(" "*70)
# 18  FECHACADUC  Numerico    6               No
        reg.append(" "*6)
# 19  SEGUNDOMI   Caracter    1               No
        reg.append(" "*1)
# 20  ULTREC  Numerico    6               No
        reg.append(" "*6)
# 21  ULTFACT     Fecha   8               No
        reg.append(" "*8)
# 22  ULTREPITE   Numerico    3       Desc    SPANISH     No 
        reg.append(" "*3)
# 23  ULTPROP     Numerico    4               No 282
        reg.append(" "*4)
# 24  FECHAINIEJ  Fecha   8               No
        reg.append(" "*8)
# 25  FECHAFINEJ  Fecha   8               No
        reg.append(" "*8)
# 26  NIVELPISO   Numerico    1               No
        reg.append(" "*1)
# 27  BLOQUEO999  Logico  1               No
        reg.append(" "*1)
# 28  TANTOPENA   Numerico    4   2           No
        reg.append("%4.2f" % (0.00))
# 29  DIASPENA    Numerico    3               No
        reg.append(" "*3)
# 30  CONCEPPENA  Numerico    2               No
        reg.append(" "*2)
# 31  FORMULAPEN  Caracter    1               No
        reg.append(" "*1)
# 32  INCLUPENA   Caracter    1               No
        reg.append(" "*1)
# 33  FECHAULTMO  Fecha   8               No
        reg.append(" "*8)
# 34  EMISORA     Caracter    1               No
        reg.append(" "*1)
# 35  BBBACTIVO   Numerico    1               No
        reg.append(" "*1)
# 36  BBBCOMU     Numerico    4               No 327
        reg.append(" "*4)
# 37  OOOCOMU     Numerico    4               No
        reg.append(" "*4)
# 38  DCCCOMU     Caracter    2               No
        reg.append(" "*2)
# 39  CCCCOMU     Numerico    10              No
        # The following bank account must start one char before stated in specs!
        # removed one char from this field
        reg.append(" "*9)
# 40  BBBCOMU2    Numerico    4               No
        reg.append("%04d" % self.banco)
# 41  OOOCOMU2    Numerico    4               No
        reg.append("%04d" % self.sucursal)
# 42  DCCCOMU2    Caracter    2               No
        dc_ = ""
        if isinstance(self.dc, int):
            dc_ = "%02d" % self.dc
        else:
            dc_ = self.dc + " "*(2-len(self.dc))
        reg.append(dc_)
# 43  CCCCOMU2    Numerico    10              No
        reg.append("%010d" % self.ccuenta)
# 44  BBBCOMU3    Numerico    4               No
        reg.append(" "*4)
# 45  OOOCOMU3    Numerico    4               No
        reg.append(" "*4)
# 46  DCCCOMU3    Caracter    2               No
        reg.append(" "*2)
# 47  CCCCOMU3    Numerico    10              No
        reg.append(" "*10)
# 48  MAYORPROP   Caracter    3               No
        reg.append(" "*3)
# 49  MAYORACTA   Caracter    3               No
        reg.append(" "*3)
# 50  MAYORING    Caracter    3               No
        reg.append(" "*3)
# 51  GCOBROOF    Caracter    12              No
        reg.append(" "*12)
# 52  GCOBROAD    Caracter    12              No
        reg.append(" "*12)
# 53  GCOBROBA    Caracter    12              No
        reg.append(" "*12)
# 54  COBROOF     Caracter    12              No
        reg.append(" "*12)
# 55  COBROAD     Caracter    12              No
        reg.append(" "*12)
# 56  COBROBA     Caracter    12              No
        reg.append(" "*12)
# 57  GCOBROOFAC  Logico  1               No
        reg.append(" "*1)
# 58  GCOBROADAC  Logico  1               No
        reg.append(" "*1)
# 59  GCOBROBAAC  Logico  1               No
        reg.append(" "*1)
# 60  COBROOFAC   Logico  1               No
        reg.append(" "*1)
# 61  COBROADAC   Logico  1               No
        reg.append(" "*1)
# 62  COBROBAAC   Logico  1               No
        reg.append(" "*1)
# 63  PAGOHONO    Caracter    12              No
        reg.append(" "*12)
# 64  GASTOSHONO  Caracter    3               No
        reg.append(" "*3)
# 65  RETENCI     Caracter    12              No
        reg.append(" "*12)
# 66  IVAREPNOR   Caracter    12              No
        reg.append(" "*12)
# 67  IVAREPNORTAN    Numerico    5   2           No
        reg.append("%5.2f" % (0.00))
# 68  IVAREPRED   Caracter    12              No
        reg.append(" "*12)
# 69  IVAREPREDTAN    Numerico    5   2           No
        reg.append("%5.2f" % (0.00))
# 70  IVAREPEXE   Caracter    12              No
        reg.append(" "*12)
# 71  IVAREPEXETAN    Numerico    5   2           No
        reg.append("%5.2f" % (0.00))
# 72  IVASOP  Caracter    12              No
        reg.append(" "*12)
# 73  ADMIPROV    Caracter    12              No
        reg.append(" "*12)
# 74  CODTIT_1    Numerico    4               No
        reg.append(" "*4)
# 75  CODTIT_2    Numerico    4               No
        reg.append(" "*4)
# 76  CODTIT_3    Numerico    4               No
        reg.append(" "*4)
# 77  CODTIT_4    Numerico    4               No
        reg.append(" "*4)
# 78  CODTIT_5    Numerico    4               No
        reg.append(" "*4)
# 79  CODTIT_6    Numerico    4               No
        reg.append(" "*4)
# 80  CODTIT_7    Numerico    4               No
        reg.append(" "*4)
# 81  CODTIT_8    Numerico    4               No
        reg.append(" "*4)
# 82  CODTIT_9    Numerico    4               No
        reg.append(" "*4)
# 83  CODTIT_10   Numerico    4               No
        reg.append(" "*4)
# 84  CODTIT_11   Numerico    4               No
        reg.append(" "*4)
# 85  CODTIT_12   Numerico    4               No
        reg.append(" "*4)
# 86  CADUMM_1    Numerico    2               No
        reg.append(" "*2)
# 87  CADUAA_1    Numerico    4               No
        reg.append(" "*4)
# 88  CADUMM_2    Numerico    2               No
        reg.append(" "*2)
# 89  CADUAA_2    Numerico    4               No
        reg.append(" "*4)
# 90  CADUMM_3    Numerico    2               No
        reg.append(" "*2)
# 91  CADUAA_3    Numerico    4               No
        reg.append(" "*4)
# 92  CADUMM_4    Numerico    2               No
        reg.append(" "*2)
# 93  CADUAA_4    Numerico    4               No
        reg.append(" "*4)
# 94  CADUMM_5    Numerico    2               No
        reg.append(" "*2)
# 95  CADUAA_5    Numerico    4               No
        reg.append(" "*4)
# 96  CADUMM_6    Numerico    2               No
        reg.append(" "*2)
# 97  CADUAA_6    Numerico    4               No
        reg.append(" "*4)
# 98  CADUMM_7    Numerico    2               No
        reg.append(" "*2)
# 99  CADUAA_7    Numerico    4               No
        reg.append(" "*4)
# 100     CADUMM_8    Numerico    2               No
        reg.append(" "*2)
# 101     CADUAA_8    Numerico    4               No
        reg.append(" "*4)
# 102     CADUMM_9    Numerico    2               No
        reg.append(" "*2)
# 103     CADUAA_9    Numerico    4               No
        reg.append(" "*4)
# 104     CADUMM_10   Numerico    2               No
        reg.append(" "*2)
# 105     CADUAA_10   Numerico    4               No
        reg.append(" "*4)
# 106     CADUMM_11   Numerico    2               No
        reg.append(" "*2)
# 107     CADUAA_11   Numerico    4               No
        reg.append(" "*4)
# 108     CADUMM_12   Numerico    2               No
        reg.append(" "*2)
# 109     CADUAA_12   Numerico    4               No
        reg.append(" "*4)
# 110     EXTRA_1     Logico  1               No
        reg.append(" "*1)
# 111     EXTRA_2     Logico  1               No
        reg.append(" "*1)
# 112     EXTRA_3     Logico  1               No
        reg.append(" "*1)
# 113     EXTRA_4     Logico  1               No
        reg.append(" "*1)
# 114     EXTRA_5     Logico  1               No
        reg.append(" "*1)
# 115     EXTRA_6     Logico  1               No
        reg.append(" "*1)
# 116     EXTRA_7     Logico  1               No
        reg.append(" "*1)
# 117     EXTRA_8     Logico  1               No
        reg.append(" "*1)
# 118     EXTRA_9     Logico  1               No
        reg.append(" "*1)
# 119     EXTRA_10    Logico  1               No
        reg.append(" "*1)
# 120     EXTRA_11    Logico  1               No
        reg.append(" "*1)
# 121     EXTRA_12    Logico  1               No
        reg.append(" "*1)
# 122     APUNTEUNI   Logico  1               No
        reg.append(" "*1)
# 123     NUMPISOS    Numerico    4               No
        reg.append(" "*4)
# 124     BAJA    Logico  1               No
        reg.append(" "*1)
# 125     BLOCKNOTAS  Memo    4               No
        reg.append(" "*4)
        #import pdb; pdb.set_trace()
        file_out.write("".join(reg))
