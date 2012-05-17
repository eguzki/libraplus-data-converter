"""
PISO Object
"""
class Piso(object):
    """docstring for Piso"""
    def __init__(self):
        self.numcomu = None
        # Portal
        self.nfinca = None
        self.numprop = None
        self.numasocia = None
        self.piso = None
#        self.coef_1 = None

    def write(self, file_out):
        reg = []

#1   NUMCOMU     Numerico    3               No
        reg.append("%3d" % self.numcomu)
#2   NFINCA  Numerico    4               No
        reg.append("%4d" % self.nfinca)
#3   NUMPROP     Numerico    4               No
        reg.append("%4d" % self.numprop)
#4   NUMASOCIA   Numerico    4               No
        reg.append("%4d" % self.numasocia)
#5   PISO    Caracter    14              No
        data = self.piso.encode("latin1")
        reg.append(data[:14])
        reg.append(" "*(14 - len(data[:14])))
#6   SINOETI     Caracter    1               No
        reg.append(" ")
#7   MARCARECI   Logico  1               No
        reg.append("F")
#8   SALDO_01    Numerico    13  2           No
        reg.append("%13.2f" % (0.00))
#9   SALDO_02    Numerico    13  2           No
        reg.append("%13.2f" % (0.00))
#10  SALDO_03    Numerico    13  2           No
        reg.append("%13.2f" % (0.00))
#11  SALDO_04    Numerico    13  2           No
        reg.append("%13.2f" % (0.00))
#12  SALDO_05    Numerico    13  2           No
        reg.append("%13.2f" % (0.00))
#13  SALDO_06    Numerico    13  2           No
        reg.append("%13.2f" % (0.00))
#14  OCUPANTE    Numerico    6               No
        reg.append(" "*6)
#15  CONCEPAG21  Numerico    2               No
        reg.append(" "*2)
#16  CONCEPAG22  Numerico    2               No
        reg.append(" "*2)
#17  CONCEPAG23  Numerico    2               No
        reg.append(" "*2)
#18  CONCEPAG31  Numerico    2               No
        reg.append(" "*2)
#19  CONCEPAG32  Numerico    2               No
        reg.append(" "*2)
#20  CONCEPAG33  Numerico    2               No
        reg.append(" "*2)
#21  INDLIBRE    Caracter    1               No
        reg.append(" "*1)
#22  DIAFACTURA  Numerico    2               No
        reg.append(" "*2)
#23  INDCERTI    Caracter    1               No
        reg.append(" "*1)
#24  INDACUSE    Caracter    1               No
        reg.append(" "*1)
#25  IVASINO     Caracter    1               No
        reg.append(" "*1)
#26  TANTOIVA    Numerico    5   2           No
        reg.append("%5.2f" % (0.00))
#27  OBSERVAC1   Caracter    70              No
        reg.append(" "*70)
#28  OBSERVAC2   Caracter    70              No
        reg.append(" "*70)
#29  COEFI_1     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#30  COEFI_2     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#31  COEFI_3     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#32  COEFI_4     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#33  COEFI_5     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#34  COEFI_6     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#35  COEFI_7     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#36  COEFI_8     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#37  COEFI_9     Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#38  COEFI_10    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#39  COEFI_11    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#40  COEFI_12    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#41  COEFI_13    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#42  COEFI_14    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#43  COEFI_15    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#44  COEFI_16    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#45  COEFI_17    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#46  COEFI_18    Numerico    13  5           No
        reg.append("%13.5f" % (0.00))
#47  TANTOIRPF   Numerico    5   2           No
        reg.append("%5.2f" % (0.00))
#48  TIPOBLOQUE  Caracter    2               No
        reg.append(" "*2)
#49  BAJA    Logico  1               No
        reg.append(" "*1)
#50  SITEXTOCSB1     Logico  1               No
        reg.append(" "*1)
#51  SITEXTOCSB2     Logico  1               No
        reg.append(" "*1)
#52  PTSACUENTA  Numerico    14  2           No
        reg.append("%14.2f" % (0.00))
#53  PRIMEPAG    Logico  1               No
        reg.append(" "*1)
#54  SEGUNPAG    Logico  1               No
        reg.append(" "*1)
#55  TERCEPAG    Logico  1               No
        reg.append(" "*1)
#56  MOTMARCARE  Numerico    1               No
        reg.append(" "*1)

        #import pdb; pdb.set_trace()
        file_out.write("".join(reg))

