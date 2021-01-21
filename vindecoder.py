import requests
from bs4 import BeautifulSoup

##https://en.wikipedia.org/wiki/Vehicle_identification_number#Model_year_encoding
##to define FMS years (=2013+) and tachoyears (assuming oldest truck we plug into is 2000)
borderYear = ['D']
fmsYear=['E','F','G','H','J','K','L','M','N','P','R','S'] #FMS years until 2025 script will work - should confirm each year
tachoYear=['Y','1','2','3','4','5','6','7','8','9','A','B','C'] #Never needs to change

Y0 = "CBL-VG-BJ1939-Y0"
Y3 = "Y3"
Y4 = "Y4"
Y5 = "Y5"
Y6 = "Y6"
BFMS = "BFMS"
TACHO = "BHGV+BTUH+BTDC-Y1"
AEDP = "AEDP"
AEPC = "AEPC" #https://www.kba.de/SharedDocs/Publikationen/EN/SV/sv32_pdf_en.pdf?__blob=publicationFile&v=6 Trailer vin codes
BPC = "ACC-BPC"
askSE = "Contact your SE, unable to automate"
askSESpecial = "Special cable needed, please contact your SE"

##Make an Array which stores the cables
cableNames = [Y0,Y3,Y4,Y5,Y6,BFMS,TACHO,AEDP,AEPC,BPC,askSE,askSESpecial]

def cablecheck(vins):
    results = []
    cables = []
    backupCables = []

    for vin in vins.splitlines(): #split the vin inputs
        vin = vin.strip()  #do some trimming of trailing and mid white spaces in each reg

        ###Re-initialise variables for best practice (incase someone enters short vin or bad data)
        vinStart=None
        vinStart4=None
        vinStart5=None
        vinStart6=None

        ###Now set the variables based on current vin
        vinStart=vin[0:3] #take first 3 chars from VIN
        vinStart4=vin[0:4] #take first 4 chars from VIN for other make models
        vinStart5=vin[0:5] #take first 5 chars from VIN
        vinStart6=vin[0:6] #take first 6 chars from VIN
        modelYear = vin[9] #take 10th character from VIN for the model year to use in MAN


        #Vin Rules
        ###VOLVO
        if vinStart == 'YV2':
            cable = volvoDecoder(vin) #Send to the volvo decoder function web scraper
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == '1C4':
            cable = Y4 #For Jeep vehicles
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == '5YJ3':
            cable = askSESpecial #Tesla Model 3
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == '5YJS':
            cable = "Y4"
            fullCable = vin+" - " + cable  + " - EV data not supported on Tesla Model S" #Tesla Model S
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == '6FP':
            cable = Y4 #For Ford Rangers
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'AHT':
            cable = Y4 #For Toyotas
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JAA':
            cable = TACHO # For Isuzu
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JAL':
            cable = TACHO # For Isuzu also
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JCB':
            cable = Y0 # For JCB
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JMA':
            cable = Y4 # For Mitsubishis
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JMZ':
            cable = Y4 # For Mazdas
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JTD':
            cable = Y4 #For toyotas (prius and aygo etc)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JTE':
            cable = Y4 #For toyota Land Cruiser
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'JTH':
            cable = Y4 #For Lexus
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'KMH':
            cable = Y4 #For Hyundai
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'KNA':
            cable = Y4 #Kia Niro
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'LSH':
            cable = Y4 #For LDV/Maxus edeliver3
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'LSK':
            cable = Y4 #For LDV vans
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'LZY':
            cable = TACHO # For Yutong TC9
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'LZZ':
            cable = TACHO # For Yutong TC9
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'MMC':
            cable = Y4 # For Mitsubishi
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'MPA':
            cable = Y4 # For Isuzu D Max (mostly connected by OBD)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'NLR':
            cable = TACHO #For Tesma turkish buses
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'NLT':
            cable = TACHO #For Tesma turkish buses
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'NMB':
            cable = TACHO #Mercedes turkish buses
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'NMT':
            cable = Y4 #Another Toyota code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'NNA':
            cable = TACHO #Another isuzu truck code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SAB':
            cable = TACHO #Optare bus code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SAD':
            cable = Y4 #Jaguar E pace
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SAJ':
            cable = Y4 #Jaguar code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SAL':
            cable = BPC #Land rover BPC (unfriendly OBD)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SAR':
            cable = BPC #Rover BPC (unfriendly OBD)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SB1':
            cable = Y4 #Toyota code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SCR':
            cable = Y4 #Carbodies/LEVC code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SDP':
            cable = Y4 #MG
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SEG':
            cable = TACHO #Dennis Elite truck
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SFD':
            cable = TACHO #For alexander dennis enviro red bus
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SHH':
            cable = Y4 #Honda Civic
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SHS':
            cable = Y4 #Honda additional code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'SJN':
            cable = Y4 #Nissan code (leaf/quashqai)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'TMA':
            cable = Y4 #Hyundai code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'TMB':
            cable = Y6 #Skoda code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'TMK':
            cable = TACHO #Karosa bus
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'TW1':
            cable = Y4 #Toyota code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'TYA':
            cable = Y4 #Mitsibushi Canter Fuso code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'U5Y':
            cable = Y4 #KIA code (Sportage/Ceed)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'UU1':
            cable = Y5 #Dacia code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VCE':
            cable = BPC # Volvo construction A40 not known if canbus or J1939
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VF1':
            cable = Y5 #Y5 as this is Renault vans
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VF3':
            cable = Y5 #For Peugeot Boxer or Peugeot cars
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF61':
            cable = askSE
            fullCable = vin+" - " +cable + " (Renault)" #Renault Trucks
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF62':
            cable = askSE
            fullCable = vin+" - " +cable + " (Renault)" #Renault Trucks
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF63':
            cable = askSE
            fullCable = vin+" - " +cable + " (Renault)" #Renault Trucks
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF64':
            cable = askSE
            fullCable = vin+" - " +cable + " (Renault)" #Renault Trucks
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF6M':
            cable = Y5 #Renault Master code
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF6S':
            cable = Y5 #Renault Maxity
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'VF6V':
            cable = Y5 #Renault Master code
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VF7':
            cable = Y5 #Y5 for Citroen
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart in ['VF9','VM3']:
            cable = AEPC #For Lamberet trailers (FR)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VFK':
            cable = AEPC #For Fruehauf trailers (FR)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VFN':
            cable = AEPC #For Cherreau trailers (FR) #Chams has run into some issues with AEPC before
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VH1':
            cable = AEPC #For Benalu trailers (FR) #Chams has run into some issues with AEPC before had to
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VLU':
            cable = askSE
            fullCable = vin+" - " + cable + " (Scania)" #Scania bus chassis
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VNE':
            cable = TACHO #For Volvo crossway bus
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VNV':
            cable = Y5 #For Nissan
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VR3':
            cable = Y5 #for Peugeot Partner
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VR7':
            cable = Y5 #Citroen Berlingo 2020
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VS9':
            cable = TACHO #Irizar coach
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VSK':
            cable = Y4 #Nissan EV200
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VSS':
            cable = Y6 #for Seat (VW group)
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VWA':
            cable = Y4 #Nissan NT400 Cabstar
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'VXE':
            cable = Y5 #For Opel Vivaro
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 in ['W0L0','W0LP','W0LG']:
            cable = Y4 #For Opel Astra/Corsa/insignia
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 in ['W0L2','W0L3','W0L4','W0LE','W0LF','W0LJ','W0LM']:
            cable = Y5 #For Opel Vivaros/Movanos different codes
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart6 in ['W0LVSD','W0LVAH']:
            cable = Y4 #Further granular astra/corsa codes (old ones)
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart6 in ['W0LVRE','W0LVSU','W0LVST']:
            cable = Y5 #Further granular Movano codes
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'W0VZ':
            cable = Y4 #Old opel insignia codes
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'W0V':
            cable = Y5 #Catch all other Opels which are Y5
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'W1K':
            cable = Y3 #Mercedes passenger cars AMG
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'W1T':
            cable = askSE
            fullCable = vin+" - " +cable  + " (Mercedes)" #Mercedes Atego Trucks (can have FMS)
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'W1V':
            cable = Y3 #Mercedes Sprinter 2020+ and Vito 2020+
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WAU':
            cable = Y6 #For Audi
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WBA':
            cable = BPC
            fullCable = vin+" - " + cable + " (BMW - Known OBD issues)" #BMWs unfriendly OBD vehicle
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WBS':
            cable = BPC
            fullCable = vin+" - " + cable  + " (BMW - Known OBD issues)" #BMWs unfriendly OBD vehicle
            results.append(fullCable)
            cables.append(cable)
        elif vinStart5 in ['WDB90','WDB91']:
            cable = Y3 #Y3 as this is Sprinter vans
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart5 in ['WDB93','WDB95','WDB96','WDB97']:
            cable = askSE
            fullCable = vin+" - " +cable + " (Mercedes)" # For Merc Trucks
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 in ['WDB6','WDF9']:
            cable = askSE
            fullCable = vin+" - " +cable + " (Mercedes)" #Merc Truck codes
            results.append(fullCable)
            cables.append(cable)
        elif vinStart in ['WDC','WDD']:
            cable = Y3 #Y3 for MB passenger cars
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart5 == 'WDF41':
            cable = Y5 #Y5 for MB Citan
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 in ['WDF4','WDF6','WDB4']:
            cable = Y3 #Y3 for MB Vito/viano non Citan
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WEB':
            cable = TACHO #for MB Evo bus
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart in ['WF0','WFO']: #Catch often typo of 0 and O for Ford Vin
            cable = Y4 #Y4 for ford
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WFB':
            cable = AEPC #For Feldbinder trailers
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WHW':
            cable = Y4 #Hako street cleaners
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WK0':
            cable = AEPC #For Kogel trailers
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WKE':
            cable = AEPC #For Krone trailers
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WKK':
            cable = TACHO #Mercedes/Setra bus
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WJM':
            cable = "BFMS + BHGV+BTUH+BTDC-Y1 (Iveco could be both, FMS is located next to tacho head)" #Iveco trucks 2020+
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(BFMS)
            cables.append(TACHO)
        elif vinStart == 'WMA':
            if modelYear in fmsYear:
                cable = "If UK/IE/FR - " + BFMS + " - If DE/ES customer please send "+ TACHO + " instead"
                cables.append(BFMS)
                backupCables.append(TACHO) ## have to put backup cables count for DE/ES
                #MAN follow 10th digit VIN for year so can accurately set BFMS on 2013+
            elif modelYear in tachoYear:
                cable = TACHO #Anything in tachoYear https://en.wikipedia.org/wiki/Vehicle_identification_number#Model_year_encoding set
                cables.append(TACHO)
            elif modelYear in borderYear:
                cable = "Could be BFMS or BHGV+BTUH+BTDC-Y1 as 2013 year"
                cables.append(TACHO)
                backupCables.append(BFMS)
            else:
                cable = "Unsure on year, if 2013+ BFMS otherwise BHGV+BTUH+BTDC-Y1" #Fallback/catch all incase doesn't follow standard (or for new years).
                cables.append(TACHO) #Main assumption is tacho
                backupCables.append(BFMS) #Backup add a BFMS count
            fullCable = vin+" - " + cable
            results.append(fullCable)
        elif vinStart == 'WME':
            cable = Y5 #Smart brand
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WMW':
            cable = Y4 #Mini brand
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart in ['WP0','WP1']:
            cable = Y6 #For Porsche
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WSK':
            cable = AEPC #For Schmitz Cargobull trailers (DE)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'WSM':
            cable = AEPC #For Schmitz Cargobull trailers (DE)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart in ['WV1','WV2','WV3','WVG','WVW']:
            cable = Y6 #Y6 for VW Caddy/Transporter/Crafter
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'XLE':
            cable = askSE
            fullCable = vin+" - " + cable + " (Scania)" #Scania
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'XLR':
            ####vinStart6 codes ending in M all seem to be newest 2020.
            ####As new DAFs are found check the new first 6 digits (expect XLRASN for example) to keep up to date
            if vinStart6 in ['XLRAD8','XLRAE4','XLRAE5','XLRAE6','XLRAS7','XLRAT7','XLRTE7','XLRTG4','XLRTG8']:
                cable = TACHO #These models I've analysed are <2013 codes always and default to tacho because data on the 2013s is very good with tacho, little benefit to sending BFMS
            elif vinStart6 in ['XLRATM','XLRACM','XLRADM','XLRAE7','XLRAE8','XLRAEH','XLRAEL','XLRAEM','XLRAKM','XLRASH','XLRASM','XLRASM','XLRTE4','XLRADM']:
                cable = BFMS #These models I've analysed are always >2013
            elif vinStart4 == 'XLR0':
                cable = TACHO #These models I've analysed are <2013 codes always
            elif vinStart4 == 'XLRT':
                cable = BFMS #These models I've analysed are always >2013
            else:
                cable = "Unsure on year, if 2013+ BFMS otherwise BHGV+BTUH+BTDC-Y1" #DAF Truck code fallback
            fullCable = vin+" - " + cable
            results.append(fullCable)
            if cable in [BFMS,TACHO]:
                cables.append(cable)
            else:
                cables.append(TACHO) ##main cable assume TACHO
                backupCables.append(BFMS) ####backup cable add BFMS incase it is FMS but we cant decode it right
        elif vinStart == 'XNL':
            cable = TACHO #For Go-Ahead buses DAF body/volvo VDL
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart5 == 'YARVF':
            cable = Y5 #Toyota proace which is a Berlingo rebadge
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'YE2':
            cable = TACHO #Van hool
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'YS2':
            cable = askSE
            fullCable = vin+" - " +cable + " (Scania)" # For Scania trucks
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'YV1':
            cable = Y4 #Y4 for Volvo Passenger vehicles (S60)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'YV3':
            cable = TACHO #Volvo buses (dont work on volvo portal)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'ZAH':
            cable = AEDP #Rolfo trailers (UK - confirmed with Rolfo all come with Rubolite junction box)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'ZAM':
            cable = Y4 #Maserati code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'ZAR':
            cable = Y4 #Alfa Romeo code
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'ZCEC':
            cable = Y5 #Iveco daily 2020+
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 == 'ZCFA':
            cable = "BFMS + BHGV+BTUH+BTDC-Y1 (Iveco could be both, FMS is located next to tacho head)" #Tacho cables for Iveco Eurocargo trucks (no portal so no FMS)
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(BFMS)
            cables.append(TACHO)
        elif vinStart4 == 'ZCFB':
            cable = TACHO #Tacho for Eurocargo (<2013)
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart4 in ['ZCFC','ZCFK','ZCF0']:
            cable = Y5
            fullCable = vin+" - " + cable + " (if tacho downloads is key swap to BHGV+BTUH+BTDC-Y1)" #Y5 for Iveco Daily
            results.append(fullCable)
            cables.append(cable)
            backupCables.append(TACHO) #to count incase tacho downloads is key
        elif vinStart == 'ZFA':
            cable = Y5 #For Fiat passenger vehicles
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable)
        elif vinStart == 'ZFC':
            cable = Y5 #Fiat code
            fullCable = vin+" - " +cable
            results.append(fullCable)
            cables.append(cable) #Append the cable choice for counting
        else:
            cable = askSE #Catch any unknown
            fullCable = vin+" - " + cable
            results.append(fullCable)
            cables.append(cable)

        print ("VIN: " + vin + " - cable - " + cable)

    return results, cables, backupCables

#Volvo Bodybuilder portal web scraper
def volvoDecoder(vin):
  baseURL='https://vbi2.truck.volvo.com/cgi-bin/vbi_vehspec3.cgi?set_spec_from_db=1&from=OM%2CCOS&drawing_type=UCD&block_pc=63%2CB3%2CD3%2CD4&frame_holes=-&remove_blind_holes=on&func=0&scale=1.0&lang=engvt&spec_id='
  ##&change_variants=&build_week=&varfam=0&messageMode=SHORT'
  #VIN='YV2RT40C8LB306801'
  URL=baseURL+vin+'&change_variants=&build_week=&varfam=0&messageMode=SHORT'

  #headers with Authorization
  headers={'Authorization': 'Basic dWs3OTg6cTE2'}

  try:
    html_text = requests.get(URL, headers=headers).text
  except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
  except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
  except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
  except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)

  soup = BeautifulSoup(html_text, 'html.parser')
  for link in soup.find_all('tr'):
    #print (link.text)
    if 'without fleet management system gateway' in link.text.lower():
      return 'BHGV+BTUH+BTDC-Y1'
    elif 'fleet management system gateway' in link.text.lower():
      return 'BFMS'
