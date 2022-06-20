import json
import csv

f = open("unifi_trafficrules.json","r")
f2 = open("unifi_networkconf.json","r")
f3 = open("unifi_cat_app.json","r")
csv_file = open('internetRules.csv','w')

rules = json.load(f)
networks = json.load(f2)
apps = json.load(f3)

netDic = {}
for n in networks["data"]:
    netDic[n["_id"]]=json.dumps([n])

parsedRulesArray = []

for r in rules:
    pRuleDic = {}
    print()
    print("Action: " + r["action"].capitalize())
    pRuleDic["Action"] = r["action"].capitalize()

    appIds = (r["matching_target"] + "_ids").lower()

    if appIds in r:
        appNames = []
        for appId in r[appIds]:
            name = ""
            if(r["matching_target"] == "APP_CATEGORY"):
                name = apps["categories"][str(appId)]["name"]
            if(r["matching_target"] == "APP"):
                name = apps["applications"][str(appId)]["name"]
            appNames.append(name)
        appString = ', '.join(map(str, appNames))
        #print(r["matching_target"].capitalize() + ": " + appString)
        print("Target: " + appString)
        pRuleDic["Target"] = appString
    else:
        print("Target: " + r["matching_target"].capitalize())
        pRuleDic["Target"] = r["matching_target"].capitalize()

    netNameList = []
    for td in r["target_devices"]:
        if td["type"] == "NETWORK":
            nid = td["network_id"]
            netJ = json.loads(netDic[nid])[0]
            netName = (netJ["name"].partition('_')[0]).capitalize()
            netNameList.append(netName)

    if(netNameList != []):
        netNameString = ', '.join(map(str, netNameList ))
        print("Devices: " + netNameString)
        pRuleDic["Devices"] = netNameString
    else:
        print("Devices: All")
        pRuleDic["Devices"] = "All"

    if 'schedule' in r:
        if (r["schedule"]["mode"] != "ALWAYS"):
            #print("Timeframe: " + r["schedule"]["time_range_start"] + " - " + r["schedule"]["time_range_end"])
            pRuleDic["StartTime"] = r["schedule"]["time_range_start"]
            pRuleDic["EndTime"] = r["schedule"]["time_range_end"]
            print("StartTime: " + r["schedule"]["time_range_start"])
            print("EndTime: " + r["schedule"]["time_range_end"])
        else:
            print("StartTime: 00:00")
            print("EndTime: 24:00")
            pRuleDic["StartTime"] = "00:00"
            pRuleDic["EndTime"] = "24:00"

        if (r["schedule"]["repeat_on_days"] != []):
            daysList = [d.capitalize() for d in r["schedule"]["repeat_on_days"]]
            dayString = ', '.join(map(str, daysList ))
            print("Days: " + dayString)
            pRuleDic["Days"] = dayString
        else:
            print("Days: Everyday")
            pRuleDic["Days"] = "Everyday"

    print("Description: " + r["description"])
    pRuleDic["Description"] = r["description"]
    print(pRuleDic)
    parsedRulesArray.append(pRuleDic)

print(parsedRulesArray)

# create the csv writer object
csv_writer = csv.writer(csv_file)
 
# Counter variable used for writing
# headers to the CSV file
count = 0
for rule in parsedRulesArray:
    if count == 0:
        # Writing headers of CSV file
        header = rule.keys()
        csv_writer.writerow(header)
        count += 1
    # Writing data of CSV file
    csv_writer.writerow(rule.values())
 
csv_file.close()