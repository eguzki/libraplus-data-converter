"""
CUOTA Object
"""
class Cuota(object):
    """docstring for Cuota"""
    def __init__(self):
        self.numcomu = None
        self.numprop = None
        self.numcuota = 0
        self.titcuota = 0
        self.impresu = 0
        self.ptsrec = 0

    def write(self, file_out):
        reg = []

#1   NUMCOMU     Numerico    3               No
        reg.append("%3d" % self.numcomu)
#2   NUMPROP     Numerico    4               No
        reg.append("%4d" % self.numprop)
#3   NUMCUOTA    Numerico    2               No
        reg.append("%2d" % self.numcuota)
#4   TITCUOTA    Numerico    4               No
        reg.append("%4d" % self.titcuota)
#5   IMPPRESU    Numerico    13  2           No
        reg.append("%13.2f" % self.impresu)
#6   PTSREC  Numerico    13  2           No
        reg.append("%13.2f" % (self.ptsrec))
#7   AAULTREC    Numerico    4               No
        reg.append(" "*4)
#8   MMULTREC    Numerico    2               No
        reg.append(" "*2)
#9   PERIODO     Numerico    2               No
        reg.append("%2d" % (1))
#10  IVA     Numerico    5   2           No
        reg.append("%5.2f" % (0.00))
#11  TIPOUNIDAD  Numerico    1               No
        reg.append("%1d" % (0))
#12  CONTADOR1   Numerico    7               No
        reg.append("%7d" % (0))
#13  CONTADOR2   Numerico    7               No
        reg.append("%7d" % (0))
#14  CANEXENTO   Numerico    7               No
        reg.append("%7d" % (0))
#15  PRECIOCON   Numerico    13  4           No
        reg.append("%13.4f" % (0.00))
#16  ULTLECTURA  Numerico    7               No
        reg.append("%7d" % (0))
#17  TIENEIVA    Logico  1               No
#        reg.append("%1d" % (0))
        reg.append("FF 0   0   0")

        #import pdb; pdb.set_trace()
        file_out.write("".join(reg))

