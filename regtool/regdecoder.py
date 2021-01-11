import requests
import json
from bs4 import BeautifulSoup

Y3 = "Y3"
Y4 = "Y4"
Y5 = "Y5"
Y6 = "Y6"
BPC = "ACC-BPC"
BFMS = "BFMS"
TACHO = "BHGV+BTUH+BTDC-Y1"
obtainVIN = "Please obtain a VIN and check with SE"
useVinDecoder = "Please obtain a VIN and use vindecoder.munaaf.com"

def ruleEngine(make,model,year):
    cable = []
    make = make.upper() #uppercase for consistent checking
    model = model.upper() #uppercase for consistent checking
    #print (make)
    #print (model)
    #print (year)

    #Rule Engine to go through all the permutations of make model year unique cables
    if make == 'FIAT':
        cable = Y5
    elif make == 'AUDI':
        cable = Y6
    elif make == 'BMW':
        cable = BPC #Hardwire cable recommendation as BMW dont play nice
    elif make == 'CITROEN':
        cable = Y5
    elif make in ['DAF TRUCKS','LEYLAND DAF']:
        if year >= '2013':
            cable = BFMS
        else:
            cable = TACHO
    elif make == 'DENNIS':
        cable = TACHO #DENNIS EAGLE TRUCK Tacho
    elif make == 'FORD':
        cable = Y4
    elif make == 'HYUNDAI':
        cable = Y4 # Hyundai
    elif make == 'ISUZU' and 'D-MAX' in model:
        cable = Y4 #donedeal.ie says ISUZU
    elif make == 'ISUZU TRUCKS': #Isuzu trucks tacho cables
        cable = TACHO
    elif make == 'IVECO' and 'DAILY' in model: #Iveco
        cable = Y5
    elif make in ['IVECO','IVECO FORD'] and year >= '2012':
        cable = "BFMS + BHGV+BTUH+BTDC-Y1 (Iveco could be both, FMS is located next to tacho head)"
    elif make in ['IVECO','IVECO FORD']: #Assume Iveco truck IVECO FORD is used by donedeal.ie occasionally for trucks
        cable = TACHO # Iveco Tacho default
    elif make == 'KIA':
        cable = Y4
    elif make in ['LAND ROVER','LAND-ROVER']:
        cable = BPC #Hardwire cable recommendation as Rover dont play nice
    elif make == 'LDV':
        cable = Y4 #LDV Vans
    elif make in ['MAN','FITZGERALD']:
        if year >= '2013':
            cable = BFMS
        else:
            cable = TACHO
    elif make in ['MERCEDES-BENZ','MERCEDES BENZ']:
        if 'Not Available' in model:
            cable = obtainVIN
        elif 'ATEGO' in model:
            cable = obtainVIN
        elif 'AROCS' in model:
            cable = obtainVIN
        elif 'ACTROS' in model:
            cable = obtainVIN
        elif 'ANTOS' in model:
            cable = obtainVIN
        elif 'AXOR' in model:
            cable = obtainVIN
        elif 'TOURISMO' in model:
            cable = TACHO
        elif 'CITAN' in model:
            cable = Y5
        elif 'SPRINTER' in model:
            cable = Y3
        elif 'VITO' in model:
            cable = Y3
        else:
            cable = Y3  ##should I fail safe against other merc codes?
    elif make in ['MITSUBISHI FUSO','MITSUBISHI']:
        if 'CANTER' in model: #Mitsubishi canter truck
            cable = TACHO
        else:
            cable = Y4
    elif make == 'NISSAN':
        if 'NV400' in model:
            cable = Y5
        elif 'NV300' in model:
            cable = Y5
        elif 'NV250' in model:
            cable = Y5
        else:
            cable = Y4
    elif make == 'PEUGEOT':
        cable = Y5
    elif make == 'RENAULT': #donedeal doesn't differentiate renault truck by make
        if 'MIDLUM' in model: #so need to check these 3 codes we've seen so far
            cable = obtainVIN
        elif '8' in model:
            cable = obtainVIN
        elif '14' in model:
            cable = obtainVIN
        elif 'MASTER' in model:
            cable = Y5
        elif 'KANGOO' in model:
            cable = Y5
        elif 'TRAFIC' in model:
            cable = Y5
        elif 'TRAFFIC' in model:
            cable = Y5
        else:
            cable = obtainVIN #to failsafe catch any truck codes and not send Y5 for trucks accidentally.
    elif make == 'RENAULT TRUCKS':
        if 'MASTER' in model:
            cable = Y5
        else:
            cable = obtainVIN
    elif make == 'TOYOTA':
        cable = Y4
    elif make in 'SCANIA':
        cable = obtainVIN
    elif make == 'SEAT':
        cable = Y6
    elif make == 'SKODA':
        cable = Y6
    elif make in 'SMART':
        cable = Y5
    elif make == 'VAUXHALL':
        if 'VIVARO' in model:
            cable = Y5
        elif 'MOVANO' in model:
            cable = Y5
        elif 'COMBO' in model:
            cable = Y5
        else:
            cable = Y4
    elif make == 'VOLVO':
        if 'FE' in model:
            cable = useVinDecoder
        elif 'FH' in model:
            cable = useVinDecoder
        elif 'FM' in model:
            cable = useVinDecoder
        elif 'FL' in model:
            cable = useVinDecoder
        elif model in ['FH','FM','FE','FL']:
            cable = useVinDecoder
        else:
            cable = Y4
    ###check cases for passenger volvos?
    elif make == 'VOLKSWAGEN':
        cable = Y6
    else:
        return "Not Sure - please obtain a VIN and ask your SE"

    ###Think about implementing some sort of counter that will track globally number of each cable
    ## so it can be retrieved and presented in the final result at the end of HTML?
    return cable

#Convert Irish number plate first 2 chars into model year
def convertYear(reg):
    year = None

    trimReg = reg[0:2] #Grab first two chars (nums) from
    #Assume regs start from 2000 (00) so just append 20 in front
    year = "20"+trimReg

    return year

def cablecheck(regs, browser):
    results = []
    baseURL = 'https://www.mycarcheck.com/vrm/'
    #baseURLIE = 'https://www.cartell.ie/ssl/servlet/step1?whitelabel=aaireland&registration='
    baseURLIE = 'https://www.donedeal.ie/cadview/api/v3/reg/'

    #print ("Regs sent to cablecheck: " + regs)

    for reg in regs.splitlines(): #split the reg inputs
        #print (reg)
        #######do some trimming of trailing and mid white spaces in each reg
        reg = reg.replace(" ", "").strip()
        #Re-initialize all variables
        cableRes = ""
        vehicleMake = None
        vehicleModel = None
        vehicleYear = None
        print (reg)
        #print (URL)
        if len(reg) <= 7:
            print ("UK Reg Found of length <=7")
            URL=baseURL+reg # Generate the full URL to be sent into selenium browser
            print (URL)
            try:
                #html_text = requests.get(URL).text
                browser.get(URL)
                #print ("Built browser")
                soup = BeautifulSoup(browser.page_source, features='html.parser')
                #print ("Built Soup")

                #Try to fetch make model year from mycarcheck, if fail graceful error
                try:
                    vehicleMake = soup.find('div', {'class':'make'}).text
                    vehicleModel = soup.find('div', {'class':'model'}).text
                    vehicleYear = soup.find('div', {'class':'registered'}).text
                    print (vehicleMake)
                    print (vehicleModel)
                    print (vehicleYear)
                except:
                    #print ("no Make found - invalid reg")
                    ###Try to see if this is an Irish registration
                    #cableRes = cablecheckIE(reg,browser)
                    cableRes = "Invalid registration - no results - please check with your SE"
                    #results.append(reg+" - " + cableRes)
                finally:
                    #Finally check if valid make is found to send to rule engine, if not the cableRes string is generated already so can pass
                    if vehicleMake:
                        #print ("make found")
                        cableRes = ruleEngine(vehicleMake,vehicleModel,vehicleYear)
            #Try to catch some general HTTP errors
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
            except:
                print ("I errored here")
            finally:
                #Append the cable check results into the results list to be returned
                results.append(reg+" - " + cableRes)
        elif len(reg) in (8,9):
            print ("IE Reg Found of length 8 or 9")
            URL=baseURLIE+reg+'/vehicle-reports' #Generate the Ireland URL
            print (URL)
            respSession = requests.Session()

            try:
                #browser.get(URL)
                respSession.headers.update({
                    'Accept':'*/*',
                    'Accept-Encoding':'gzip, deflate, br',
                    'Connection':'keep-alive',
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
                    })
                #print ("Set headers")
                resp = respSession.get(URL)
                print (resp)

                soup = BeautifulSoup(resp.content,'html.parser')
                json_soup = json.loads(soup.text)

                try:
                    vehicleMake = json_soup['vehicleDetails']['Make'].upper()
                    vehicleModel = json_soup['vehicleDetails']['Model'].upper()
                    vehicleYear = convertYear(reg)
                    print (vehicleMake)
                    print (vehicleModel)
                    print (vehicleYear)
                except:
                    #asd
                    cableRes = "Invalid registration or unable to automate - no results - please check with your SE"
                finally:
                    if vehicleMake:
                        cableRes = ruleEngine(vehicleMake,vehicleModel,vehicleYear)

            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
            except:
                print ("I errored here")
            finally:
                #browser.close() #close browser process
                #Append the cable check results into the results list to be returned
                results.append(reg+" - " + cableRes)

    return results

