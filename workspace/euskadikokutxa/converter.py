# -*- coding: utf-8 -*-
import logging
import optparse
import sys
import os
import re
from datetime import datetime
import codecs
from entity import comunidad, cuota, piso, user, cuotaCollection

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}

RESULT = {
    "comunidad": None,
    "pisos": [],
    "cuotas": [],
    "personas": []
}

CUOTAS = [(1,1), (2,11), (3,2), (4,8), (5, 5),
          (6,9), (7,7), (8,8), (9,9), (10,10),
          (11,11), (12,12)]

LOGGER = None
PISO_PORTAL_PATTERN_1 = re.compile("(\d+)\s*-\s*(\d+.*)")
PISO_PORTAL_PATTERN_2 = re.compile("N*\s+(\d+)\s+(\d+.*)")
PISO_PORTAL_PATTERN_3 = re.compile("N*\s+(\d+)\s+(ATICO|BAJO)\s*")
PISO_PORTAL_PATTERN_4 = re.compile("(\d+\s+BIS)\s+(-)\s*")
PISO_PORTAL_PATTERN_5 = re.compile("(\d+\s+BIS)\s+(\d+.*)\s*")
PISO_PORTAL_PATTERN_6 = re.compile("(\d+)\s*-(.*)\s*$")
LOCAL_PATTERN = re.compile("LOCAL")
GARAJE_PATTERN  = re.compile("GARAJE")
GENERIC_CUOTA_ANUAL_PATTERN = re.compile("CUOTA ANUAL\s+[a-zA-Z0-9\(\)]*\s+\d+[.\d,]*\s*$")
COMUNIDAD_CUOTA_PATTERN = re.compile("CUOTA COMUNIDAD\s+\d+[.\d,]*\s*$")
CUOTA_EXTRA_PATTERN = re.compile("CUOTA EXTRA")
CUOTA_PATTERN = re.compile("\s\d+[.\d,]*\s*$")

def userData_handler5380(line):
    """docstring for comunidad"""
    LOGGER.debug("%s", line)
    comu = comunidad.Comunidad()
    comu.parse(line)
    RESULT["comunidad"] = comu
    LOGGER.info("New comunidad!: %s\n", comu.nombre)

def userData_handler5680(line):
    """
    New user register
    5680H31927627001000000004903BIURRUN ETXERA, IÑAKITX                 2054000042000062905100000090000005990000000004 SEPTIEMBRE-11
    5680H31886872000000000009704ASURMENDI FERNANDEZ, JESUS MARIA        3008007310151731601200000062090006540000000086 CUOTA MENSUAL 62,09
    """
    LOGGER.debug("%s", line)
    persona = user.User()
    comu = RESULT["comunidad"]

    # Calculate numcomu and numprop format
    if int(line[19:23]) != 0:
        persona.numprop = len(RESULT["personas"]) + 1
        comu.numcomu = int(line[19:23])
    elif divmod(int(line[22:25]), 100)[0] == 0:
        # numprop contains numcomu
        persona.numprop = int(line[24:28])
        comu.numcomu = None
    else:
        # numcomu has 3 digits and numprop does not contain
        persona.numprop = len(RESULT["personas"]) + 1
        comu.numcomu = int(line[22:25])

    #
    persona.nombre = line[28:68].strip()
    persona.banco = line[68:72]
    persona.sucursal = line[72:76]
    persona.dccuenta = line[76:78]
    persona.numcta = line[78:88]

    RESULT["personas"].append(persona)
    cuotas = cuotaCollection.CuotaCollection()
    RESULT["cuotas"].append(cuotas)

    cuotas.numprop = persona.numprop

    data = line[28:].strip()
    m = CUOTA_PATTERN.search(data)
    if m:
        #cuo.numcuota = 1
        #cuo.titcuota = 1
        cuotas.cuotas[1] = {
                "titcuota": 1,
                "ptsrec": float(str(m.group(0).strip()).translate(None, ".").replace(",", "."))
                }

    LOGGER.info("New propietario!: %2d: %s\n", persona.numprop,
                persona.nombre.encode("latin1"))

def userData_handler5681(line):
    """
    docstring for userDataHandler5681
    CUOTA ANUAL LOCAL
    CUOTA ANUAL GARAJE
    CUOTA ANUAL 
    """
    LOGGER.debug("%s", line)
    persona = RESULT["personas"][-1]
    cuotas = RESULT["cuotas"][-1]
    #cuotas.numprop = int(line[24:28])
    cuoObject = {
            "titcuota": 0,
            "ptsrec": 0.0
            }

    if LOCAL_PATTERN.search(line[28:]):
        # 5681 associated to numcuota = 3, titcuota = 2
        cuoObject["titcuota"] = 2
        cuotas.cuotas[3] = cuoObject
    elif (GARAJE_PATTERN.search(line[28:]) or 
          GENERIC_CUOTA_ANUAL_PATTERN.search(line[28:])):
        # 5681 associated to numcuota = 2, titcuota = 11
        cuoObject["titcuota"] = 11
        cuotas.cuotas[2] = cuoObject
    elif COMUNIDAD_CUOTA_PATTERN.search(line[28:]):
        # 5681 associated to numcuota = 1, titcuota = 1
        cuoObject["titcuota"] = 1
        cuotas.cuotas[1] = cuoObject
    else:
        assert False, ("register 5681 is neither a LOCAL nor GARAJE "
        "nor CUOTA ANUAL not CUOTA COMUNIDAD")

    data = line[28:].strip()
    m = CUOTA_PATTERN.search(data)
    if not m:
        assert False, "Unknow cuota number on register 5681"

    cuoObject["ptsrec"] = float(str(m.group(0).strip()).translate(None, ".").replace(",", "."))

def userData_handler5682(line):
    """docstring for userDataHandler5682"""
    LOGGER.debug("%s", line)
    cuotas = RESULT["cuotas"][-1]

    #import pdb
    #pdb.set_trace()
    #cuotas.numprop = int(line[24:28])

    cuoObject = {
            "titcuota": 0,
            "ptsrec": 0.0
            }

    # Check there is extra,
    # in this case, we are adding one cuota register to RESULT["cuotas"]
    # otherwise, associate to numcuota=1 unless it was already assigned
    if CUOTA_EXTRA_PATTERN.search(line[28:]):
        # 5682 associated to numcuota = 4, titcuota = 8
        cuoObject["titcuota"] = 8
        cuotas.cuotas[4] = cuoObject
    elif GENERIC_CUOTA_ANUAL_PATTERN.search(line[28:]):
        # 5682 associated to numcuota = 2, titcuota = 11
        cuoObject["titcuota"] = 11
        cuotas.cuotas[2] = cuoObject
    elif len(cuotas.cuotas) != 0:
        # There is a previous 5681 register, forget this one
        return
    else:
        # 5682 associated to numcuota = 1, titcuota = 1
        cuoObject["titcuota"] = 1
        cuotas.cuotas[1] = cuoObject

    data = line[28:].strip()
    m = CUOTA_PATTERN.search(data)
    if not m:
        assert False, "Unknow cuota number on register 5682"

    cuoObject["ptsrec"] = float(str(m.group(0).strip()).translate(None, ".").replace(",", "."))

def userData_handler5683(line):
    """
    New user register
    5683H31346026001000000002265 CUOTA ANUAL TRASTERO(13)         60,10
    """
    LOGGER.debug("%s", line)
    cuotas = RESULT["cuotas"][-1]

    # 5683 associated to numcuota = ?
    if 4 in cuotas.cuotas:
        # There is a previous cuota like this, forget
        LOGGER.debug("forgetting cuota: %s", line)
        return

    #cuotas.numprop = int(line[24:28])
    # 5683 associated to numcuota = 4, titcuota = 8
    cuoObject = {
            "titcuota": 8,
            "ptsrec": 0.0
            }
    cuotas.cuotas[4] = cuoObject
    data = line[28:].strip()
    m = CUOTA_PATTERN.search(data)
    if not m:
        assert False, "Unknow cuota number on register 5683"

    cuoObject["ptsrec"] = float(str(m.group(0).strip()).translate(None, ".").replace(",", "."))

def userData_handler5684(line):
    """docstring for userDataHandler5684"""
    LOGGER.debug("%s", line)

def userData_handler5685(line):
    """docstring for userDataHandler5685"""
    LOGGER.debug("%s", line)

def userData_handler5686(line):
    """
    docstring for userDataHandler5686
    It is known cuota type (garaje, local, vecino)
    """
    LOGGER.debug("%s", line)
    cuotas = RESULT["cuotas"][-1]

    persona = RESULT["personas"][-1]
    persona.via = line[68:71].strip()
    persona.pobla = line[108:116].strip()
    persona.cpostal = int(line[143:148])
    persona.calle = line[71:108].strip()

    pis_obj = piso.Piso()
    pis_obj.numprop = persona.numprop
    pis_obj.numasocia = persona.numprop

    # Pattern matching depending on cuota type
    m = None
    
    # VECINO
    m_1 = PISO_PORTAL_PATTERN_1.search(persona.calle)
    m_2 = PISO_PORTAL_PATTERN_2.search(persona.calle)
    m_3 = PISO_PORTAL_PATTERN_3.search(persona.calle)
    m_4 = PISO_PORTAL_PATTERN_4.search(persona.calle)
    m_5 = PISO_PORTAL_PATTERN_5.search(persona.calle)
    m_6 = PISO_PORTAL_PATTERN_6.search(persona.calle)
    if m_1:
        m = m_1
    elif m_2:
        m = m_2
    elif m_3:
        m = m_3
    elif m_4:
        m = m_4
    elif m_5:
        m = m_5
    elif m_6:
        m = m_6

    if m:
        persona.piso = m.group(2).strip()
        persona.numcalle = m.group(1)
        persona.calle = persona.calle[:m.start()].strip().strip(".").strip()
        pis_obj.piso = persona.piso
    elif 1 not in cuotas.cuotas:
        # EXCEPTION
        # TRASTERO, LOCAL or GARAJE
        persona.piso = persona.calle
        persona.numcalle = "0"
        pis_obj.piso = persona.piso
    else:
        LOGGER.warning("Cannot parse VECINO at register 5686: %s",
                       persona.calle)
        persona.piso = persona.calle
        persona.numcalle = "0"
        pis_obj.piso = persona.piso

    # append piso
    RESULT["pisos"].append(pis_obj)

def end_of_file(line):
    """docstring for end_of_file"""
    LOGGER.debug("%s", line)
    numcomu = RESULT["comunidad"].numcomu
    if not numcomu:
        # numcomu was not set
        # Compute numComu
        numcomu = min ( [ divmod(persona.numprop, 100)[0] for persona in RESULT["personas"] ] )
        RESULT["comunidad"].numcomu = numcomu

    for persona in RESULT["personas"]:
        persona.numcomu = numcomu
    for pisos in RESULT["pisos"]:
        pisos.numcomu = numcomu
        pisos.nfinca = numcomu
    for cuotas in RESULT["cuotas"]:
        cuotas.numcomu = numcomu

def nop(line):
    """docstring for nop"""
    pass

CODES = {
    '5180': nop,
    '5380': userData_handler5380,
    '5680': userData_handler5680,
    '5681': userData_handler5681,
    '5682': userData_handler5682,
    '5683': userData_handler5683,
    '5684': userData_handler5684,
    '5685': userData_handler5685,
    '5686': userData_handler5686,
    '5880': end_of_file,
}

def convert(filename, file_dir, encoding="latin1"):
    """docstring for splitter"""
    file_object = codecs.open(filename, mode = 'r', encoding = encoding)
    for line in file_object.readlines():
        code = line[0:4]
        if code not in CODES:
            logging.warning("code %s not known: %s" % (code, line))
        else:
            CODES[code](line)

    # Write files
    # Comunidad
    out_file = open(os.path.join(file_dir, "WCOMUNI.TXT"), 'w')
    RESULT["comunidad"].write(out_file)
    out_file.close()
    LOGGER.info("WCOMUNI.TXT created!")

    # Pisos
    out_file = open(os.path.join(file_dir, "WPISOS.TXT"), 'w')
    for entity in sorted ( RESULT["pisos"], key=lambda x: x.numprop ):
        entity.write(out_file)
        out_file.write("\n")
    out_file.close()
    LOGGER.info("WPISOS.TXT created!")

    # Cuotas
    # Now, a register 5680 may have more than one type of cuotas
    # Cuota.py object should remain simple
    # Generate WCUOTAS filling more than one CUOTA (numcuota, titcuota)
    out_file = open(os.path.join(file_dir, "WCUOTAS.TXT"), 'w')
    for cuotas in sorted ( RESULT["cuotas"], key=lambda x: x.numprop ):
        cuotasArray = []
        for c_index_numcuota, c_index_titcuota in CUOTAS:
            cuo = cuota.Cuota()
            cuo.numcomu = cuotas.numcomu
            cuo.numprop = cuotas.numprop
            cuo.impresu = cuotas.impresu

            # if there is in cuotas dict, then create cuota object with that info
            if c_index_numcuota in cuotas.cuotas:
                cuo.numcuota = c_index_numcuota
                assert c_index_titcuota == cuotas.cuotas[c_index_numcuota]["titcuota"], "titcuota do not match: [%d, %d]" % (c_index_titcuota, cuotas.cuotas[c_index_numcuota]["titcuota"])
                cuo.titcuota = c_index_titcuota
                cuo.ptsrec = cuotas.cuotas[c_index_numcuota]["ptsrec"]
                cuotasArray.append(cuo)
            else:
                cuo.numcuota = c_index_numcuota
                cuo.titcuota = c_index_titcuota
                cuo.ptsrec = 0
                cuotasArray.append(cuo)

        for cuo in cuotasArray:
            cuo.write(out_file)
            out_file.write("\n")

    out_file.close()
    LOGGER.info("WCUOTAS.TXT created!")

    # Personas
    out_file = open(os.path.join(file_dir, "WPERSONA.TXT"), 'w')
    for entity in sorted ( RESULT["personas"], key=lambda x: x.numprop ):
        entity.write(out_file)
        out_file.write("\n")
    out_file.close()
    LOGGER.info("WPERSONA.TXT created!")
    LOGGER.info("OUTPUT_DIR: %s" % (file_dir))
    LOGGER.info("Finished OK. YUHUUU!")

def main():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--logging-level', help='Logging level')
    parser.add_option('-f', '--logging-file', help='Logging file name')
    parser.add_option('-e', '--encoding', help='file encoding', default="latin1")
    parser.add_option('-o', '--output', help='output dir')
    (options, args) = parser.parse_args()
    logging_level = LOGGING_LEVELS.get(options.logging_level, logging.NOTSET)
    logging.basicConfig(level=logging_level,
                        filename=options.logging_file,
                        format='%(asctime)-15s %(levelname)s: %(message)s')
    global LOGGER
    LOGGER = logging.getLogger()
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)-15s %(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(console_handler)

    output_dir = os.path.abspath(options.output)
    if not os.path.exists( output_dir ):
        os.makedirs( output_dir )

    filename = sys.argv[-1]
    #Input parameter parsing logic
    LOGGER.info(("Starting job pid: %s "
                 "filename: %s logfile: %s\n"),
                str(os.getpid()),
                filename,
                options.logging_file)
    try:
        convert(filename, output_dir, options.encoding)
    except:
        from sys import exc_info
        from traceback import format_tb
        e_type, e_value, tb = exc_info()
        traceback = ['Unexpected fatal error: Traceback (most recent call last):']
        traceback += format_tb(tb)
        traceback.append('%s: %s' % (e_type.__name__, e_value))
        LOGGER.error("Unexpected error:  %s" % (traceback))
        LOGGER.info("Finished with errors. ARGHHHH!")

if __name__ == "__main__":
    main()
