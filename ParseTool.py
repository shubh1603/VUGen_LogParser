import re
import os
import json
import datetime

def metricsExtractor(tfile):
    with open(tfile) as f:
        lines = f.readlines()
    sum = 0
    itr = 0
    sb = 0
    for line in lines:
        if line.__contains__("Notify") and line.__contains__('ended'):
            matchObj = re.match(
                r'Notify: Transaction "(.*)" ended with a "(.*)" status \(Duration: (.*) Wasted Time: (.*)\)', line)
            if matchObj.group(3).__contains__('Think Time'):
                mobj = re.match(r'(.*) Think Time: (.*)', matchObj.group(3))
                duration = mobj.group(1)
            else:
                duration = matchObj.group(3)
            sum += (float(duration) - float(matchObj.group(4)))
            itr += 1
        if line.__contains__("Request body"):
            mhObj = re.match(r't=.*ms: Request body for .* \((.*) byte', line)
            sb += float(mhObj.group(1))
    f.close()
    return {'TxnName':matchObj.group(1),'Metrics':{'Avg RT': round(float(sum/itr),4),'PostBytes':round(float(sb/itr),2)}}

def checkPOST():
    print("Checking for POST only transactions")
    txnfiles = os.listdir('temp')
    for file in txnfiles:
        with open('temp//' + file) as f:
            lst = f.readlines()
            post = 0
            get = 0
            check = True
            for line in lst:
                post += line.count('POST')
                get += line.count('GET')
            if get > 0:
                check = True
            elif post > 0:
                check = False
            f.close()
            #removing files with GET txns
            if check:
                if f.closed:
                    os.remove('temp//' + file)
                else:
                    print('Please close',file)

def txnParser(inp):
    #split the output file based on txnfiles
    print("Parsing Transactions")
    with open(inp) as infile:
        fname = 'temp1'
        for line in infile:
            if line.__contains__("Notify") and line.__contains__('start'):
                matchObj = re.match(r'Notify: Transaction "(.*)" started', line)
                fname = str(matchObj.group(1))
                with open('temp//'+fname + '.txt', 'a') as f:
                    f.writelines(line)
                    f.close()
            elif line.__contains__("Notify") and line.__contains__('end'):
                matchObj = re.match(
                    r'Notify: Transaction "(.*)" ended with a ".*" status \(Duration: .* Wasted Time: .*\)',
                    line)
                fname = str(matchObj.group(1))
                with open('temp//'+fname + '.txt', 'a') as f:
                    f.writelines(line)
                f.close()
            else:
                with open('temp//'+fname + '.txt', 'a') as f:
                    f.writelines(line)
                    f.close()



if __name__ == "__main__":

    # create temp working directory
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    # remove old temp log files
    txnfiles = os.listdir('temp')
    for file in txnfiles:
        os.remove('temp//' + file)

    # Split the input files, based on transactions
    inpfile = input("Enter log file \n:")
    txnParser(inpfile)

    # Look for txns with only POST requests
    checkPOST()

    txnfiles = os.listdir('temp')
    lst = []
    # Get the metrics
    print("Getting the Metrics")
    for f in txnfiles:
        print(f)
        lst.append(metricsExtractor('temp//' + f))

    # Generate the json file
    x = str(datetime.datetime.now().strftime("%d%m_%H%M%S"))
    with open('Metrics_'+x+'.json', 'w') as f:
        json.dump(lst, f)
    f.close()

