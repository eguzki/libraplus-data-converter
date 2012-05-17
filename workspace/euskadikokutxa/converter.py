import logging
import optparse
import sys
import os
import re
from datetime import datetime
import codecs
from entity import comunidad, cuota, piso, user

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

LOGGER = None
PISO_PORTAL_PATTERN  = re.compile("(\d+)-(\d+.*)")
LOCAL_PATTERN  = re.compile("LOCAL")

def comunidad_handler(line):
    """docstring for comunidad"""
    LOGGER.debug("%s", line)
    comu = comunidad.Comunidad()
    comu.parse(line)
    RESULT["comunidad"] = comu
    LOGGER.info("New comunidad!: %s\n", comu.nombre)

def new_user_handler(line):
    """
    New user register
    5680H31927627001000000004903BIURRUN BABACE, IGNACIO                 2054000042000062905100000090000005990000000004 SEPTIEMBRE-11
    """
    LOGGER.debug("%s", line)
    persona = user.User()
    comu = RESULT["comunidad"]
    persona.numprop = int(line[24:28])
    persona.nombre = line[28:68].strip()
    try:
        try:
            persona.banco = int(line[68:72])
        except:
            LOGGER.warning("usuario: %d, codigo banco no reconocido: %s",
                       persona.numprop, line[68:72])
            raise Exception()
        try:
            persona.sucursal = int(line[72:76])
        except:
            LOGGER.warning("usuario: %d, codigo sucursal no reconocido: %s",
                       persona.numprop, line[72:76])
            raise Exception()
        try:
            persona.dccuenta = int(line[76:78])
        except:
            LOGGER.warning("usuario: %d, codigo cuenta no reconocido: %s",
                       persona.numprop, line[76:78])
            raise Exception()
        try:
            persona.numcta = int(line[78:88])
        except:
            LOGGER.warning("usuario: %d, numero de cuenta no reconocido: %s",
                       persona.numprop, line[78:88])
            raise Exception()
    except:
        persona.banco = 0
        persona.sucursal = 0
        persona.dccuenta = 0
        persona.numcta = 0

    RESULT["personas"].append(persona)
    LOGGER.info("New propietario!: %2d: %s\n", persona.numprop,
                persona.nombre.encode("latin1"))

def userData_handler5681(line):
    """docstring for userDataHandler5681"""
    LOGGER.debug("%s", line)
    cuo = cuota.Cuota()
    cuo.numprop = int(line[24:28])
    # 5681 associated to numcuota = 3
    cuo.numcuota = 3
    cuo.titcuota = 2
    data = line[28:].strip()
    cuo.ptsrec= float(data[-7:].strip().replace(",", "."))
    RESULT["cuotas"].append(cuo)

def userData_handler5682(line):
    """docstring for userDataHandler5682"""
    LOGGER.debug("%s", line)
    cuo = cuota.Cuota()
    cuo.numprop = int(line[24:28])
    # 5682 associated to numcuota = 1
    cuo.numcuota = 1
    cuo.titcuota = 1
    data = line[28:].strip()
    cuo.ptsrec= float(data[-7:].strip().replace(",", "."))
    RESULT["cuotas"].append(cuo)

def userData_handler5684(line):
    """docstring for userDataHandler5684"""
    LOGGER.debug("%s", line)

def userData_handler5685(line):
    """docstring for userDataHandler5685"""
    LOGGER.debug("%s", line)

def userData_handler5686(line):
    """docstring for userDataHandler5686"""
    LOGGER.debug("%s", line)
    persona = RESULT["personas"][-1]
    persona.via = line[68:71].strip()
    persona.pobla = line[108:116].strip()
    persona.cpostal = int(line[143:148])
    persona.calle = line[71:108].strip()

    pis_obj = piso.Piso()
    pis_obj.numprop = persona.numprop
    pis_obj.numasocia = persona.numprop

    m = PISO_PORTAL_PATTERN.search(persona.calle)
    if m:
        persona.piso = m.group(2)
        persona.numcalle = int(m.group(1))
        persona.calle = persona.calle[:m.start()]
        pis_obj.piso = m.group(2)
    elif LOCAL_PATTERN.search(persona.calle):
        persona.piso = "LOCAL"
        persona.numcalle = 0
        pis_obj.piso = "LOCAL"
    else:
        persona.piso = ""
        persona.numcalle = 0
        pis_obj.piso = ""

    RESULT["pisos"].append(pis_obj)

def end_of_file(line):
    """docstring for end_of_file"""
    LOGGER.debug("%s", line)
    # Compute numComu
    numcomu = min ( [ divmod(persona.numprop, 100)[0] for persona in RESULT["personas"] ] )
    # Override numcomu for testing
    #numcomu = 10
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
    '5380': comunidad_handler,
    '5680': new_user_handler,
    '5681': userData_handler5681,
    '5682': userData_handler5682,
    '5683': nop,
    '5684': userData_handler5684,
    '5685': userData_handler5685,
    '5686': userData_handler5686,
    '5880': end_of_file,
}

def convert(filename, file_dir, encoding="utf8"):
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
    out_file = open(os.path.join(file_dir, "WCUOTAS.TXT"), 'w')
    for entity in sorted ( RESULT["cuotas"], key=lambda x: x.numprop ):
        cuotas = []
        if (entity.numcuota == 1):
            # Regular case
            cuotas.append(entity)
            for numcuota, titcuota in [(2,11), (3,2), (4,8), (5, 5),
                                       (6,9), (7,7), (8,8), (9,9), (10,10),
                                       (11,11), (12,12)]:
                cuo = cuota.Cuota(entity)
                cuo.numcuota = numcuota
                cuo.titcuota = titcuota
                cuo.ptsrec = 0
                cuotas.append(cuo)
        else:
            # Irregular case
            cuo = cuota.Cuota(entity)
            cuo.numcuota = 1
            cuo.titcuota = 1
            cuo.ptsrec = 0
            cuotas.append(cuo)
            cuo = cuota.Cuota(entity)
            cuo.numcuota = 2
            cuo.titcuota = 11
            cuo.ptsrec = 0
            cuotas.append(cuo)
            # Append parsed data
            cuotas.append(entity)
            # Append the rest
            for numcuota, titcuota in [(4,8), (5, 5),
                                       (6,9), (7,7), (8,8), (9,9), (10,10),
                                       (11,11), (12,12)]:
                cuo = cuota.Cuota(entity)
                cuo.numcuota = numcuota
                cuo.titcuota = titcuota
                cuo.ptsrec = 0
                cuotas.append(cuo)

        for cuo in cuotas:
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
    parser.add_option('-e', '--encoding', help='file encoding')
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
