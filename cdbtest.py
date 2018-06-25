
"""

execfile('/home/oxygen31/TMADDEN/RF/swWork/cdb/cdbtest.py')


"""

 
from cdb.cdb_web_service.api.itemRestApi import ItemRestApi

execfile('speadsheet.py')


 
def cdblogon():
    
    usrn=raw_input("Username: ")
    passwd=raw_input("Password: ")

    itemRestApi_ = ItemRestApi(
        host='ctlappsdev', 
        port=10233, 
        protocol='https', 
        username=usrn, 
        password=passwd)
        
    return(itemRestApi_)



def printItem(item):
    print "-----------------"
    print_dict(item)
   
    print "  "
    print "=================="
    print "  "
    
def print_dict(item, level=0):
    item = list_to_dict(item)
    for k in item.keys():
        if type(item[k])!=unicode and type(item[k])!=int and type(item[k])!=str and type(item[k])!=float:
            print "%s%s :--->"%("    "*level,k)
            print_dict(item[k], level+1)
        else:
            print "%s%s : %s"%("    "*level,k, item[k])
            print " "
  

def list_to_dict(item):
    if type(item)==list:
        itemd = {}
        count =0
        for k in item:   
            itemd[str(count)]=k
            count= count+1
        return(itemd)
    else:
        return(item)



def printLocations(itemid=None,level=0,maxlevel=100):
    if level>=maxlevel: return

    if level==0:
        loclist = itemRestApi.getLocationTopLevelItems()
    else:
        loclist = itemRestApi.getItemElementsForItem(itemid)

    for i in loclist:
        if u'name' in i.keys():
            if level==0:
                print '%sid: %d, name: %s'%('    '*level,i['id'],str(i['name']))
                printLocations(i['id'],level+1,maxlevel)
            else:
                print '%sid: %d, name: %s'%('    '*level,i['containedItem']['id'],str(i['containedItem']['name']))
                printLocations(i['containedItem']['id'],level+1,maxlevel)

   
dbLocations= [
{'id':'56','name':'RF_Teststand', 'terms':['Test Stand']},
{'id':'50','name':'High_Bay_Area#1', 'terms':['RF1','36',]},
{'id':'51','name':'High_Bay_Area#2', 'terms':['RF2','37']},
{'id':'52','name':'High_Bay_Area#3', 'terms':['RF3','38']},
{'id':'53','name':'High_Bay_Area#4', 'terms':['RF4','40']},
{'id':'54','name':'High_Bay_Area#5', 'terms':['RF5','Booster','Extraction','420 Spares']},
{'id':'48','name':'A014', 'terms':['Source','A014','AO14']}


]

def ssLocToDbLoc(ssloc):
    for dbloc in dbLocations:
        for term in dbloc['terms']:
            if term in ssloc or ssloc in term:
                return( {'id':dbloc['id'], 'ssloc':ssloc} )
    return({'id':None, 'ssloc':ssloc} )


def findCatelogItem(name, model_number):
    item = itemRestApi.getItemByUniqueAttributes( 
        "Catalog", 
        name,
        itemIdentifier1=model_number)
    return(item['id'])

def checkInventory(itemid,callback = None):
    num_inventory = 0
    num_spares = 0
    unknown_location = 0
    print "____________________________________________________________________"
    print "Catelog Item"
    print ""
    item = itemRestApi.getItemById(itemid)
    print "id: %s, name: %s, Model #: %s"%(item['id'],item['name'],item['item_identifier1'])
    print ""
    print "Inventory Items--------------------------------------------------"

    invt=itemRestApi.getItemsDerivedFromItem(itemid)
    num_inventory = len(invt)
    for ii in invt:
        print "    id: %s, name: %s, Model #: %s"%(ii['id'],ii['name'],ii['item_identifier1'])

        dblocs = itemRestApi.getFirstItemRelationshipList(ii['id'],'Location')
        if len(dblocs)>0:
            dbloc = dblocs[0]
            print "        Location: %s LocID: %s"%(
                dbloc['relationship_details'],dbloc['second_item_element_id'])


            try:
                status =  itemRestApi.getInventoryItemStatus(ii['id'])
                print '        Status: %s'%(status['value'])
                if status['value']=='Spare':
                    num_spares = num_spares +1
            except:
                pass 

            if callback != None:
                callback(item['id'],ii['id'],dbloc['second_item_element_id'])
        else:
            unknown_location = unknown_location +1

        print ""
    
    print ""
    print "Number Inventory Items: %d"%num_inventory
    print "Number Spares: %d"%num_spares
    print "Unknown Locations: %d"%unknown_location

    print "End Report____________________________________________________"

def addEdmInventory(edmid):
    columns = ss.getCols([0,1,2,3])
    for col in columns:
      try:
        edmitem= itemRestApi.addItem(
            name=col[0],
            domainName="Inventory",
            derivedFromItemId=edmid, 
            itemIdentifier1=col[1],
            itemProjectName='APS-OPS')
        print "Added %s"%col[0]

        itemid= edmitem['id']
        ssloc =col[2] 
        dbloc = ssLocToDbLoc(ssloc)
        ssslot =col[3] 
        dbloc['ssloc'] = ssloc + ", slot " + ssslot
        print "item id = %s, Location to be %s"%(itemid,dbloc)
        if dbloc['id'] !=None:
            itemRestApi.addItemRelationship(
                itemid, 
                dbloc['id'], 
                'Location', 
                relationshipDetails=dbloc['ssloc'])

            print "Set Location %s"%col[2]

      except:
        print "Problem with %s"%col[0]
        return




#checkInventory(2449,updateStatusByLocation)
def updateStatusByLocation(cat_id, inv_id, loc_id):
    #Installed
#    print '%s %s %s'%(cat_id, inv_id, loc_id)
    stat_val = "Installed" 
    if type(loc_id)==str: loc_id = int(loc_id)
    if loc_id == 56: #test stand
        stat_val ="Spare"
    itemRestApi.updateInventoryItemStatus(inv_id,stat_val)
    print "Updated status %s"%stat_val




 
"""

itemRestApi = cdblogon()


itemRestApi = ItemRestApi(
    host='ctlappsdev', 
    port=10233, 
    protocol='https', 
    username='cdb', 
    password='cdb')

    
itemRestApi.getItemById(50)

itemRestApi.addItem(domainName='Catalog', name='api-test')

item = itemRestApi.addItem(domainName='Catalog', name='api-test2')

id = item['id']



envdet = itemRestApi.getItemByUniqueAttributes( 
    "Catalog", 
    "Envelop Detector",
    "EDM100")

envdet = itemRestApi.getItemById(2358)


envprops = itemRestApi.getPropertiesForItemByItemId( envdet['id'])

printItem(envdet)

printItem(envprops)


env_inventory=itemRestApi.getItemsDerivedFromItem(envdet['id'])

printItem(env_inventory)


printItem(
    itemRestApi.getItemsDerivedFromItem(envdet['id']))


itemRestApi.getCatalogItems()

printItem(
itemRestApi.getItemElementsForItem(envdet['id']))


itemRestApi.addItem(
    name='inveTest2',
    domainName="Inventory",
    derivedFromItemId=500, 
    itemProjectName='APS-U')

prop = itemRestApi.addPropertyValueToItemWithId(
    envdet['id'], 
    'Model Number', 
    tag=None, 
    value='EDM100', 
    units=None, 
    description=None,
    isUserWriteable=None,
    isDynamic=None)




printItem( itemRestApi.getItemById(2359))


printItem(itemRestApi.getPropertiesForItemByItemId( 2359))


printItem(
itemRestApi.getItemElementsForItem(2359))

printItem(itemRestApi.getLocationItems())


itemRestApi.getContextRoot()


itemRestApi.

itemRestApi.

itemRestApi.

itemRestApi.

itemRestApi.


printLocations(maxlevel=3)
printLocations(maxlevel=2)
printLocations()
printLocations(maxlevel=1)
printLocations(itemid = 9,level=1,maxlevel=2)
printLocations(maxlevel=1)
printLocations(itemid = 1, level = 1,maxlevel=2)
printLocations(itemid = 8, level = 1,maxlevel=2)
printLocations(itemid = 9, level = 1,maxlevel=2)
printLocations(itemid = 3, level = 1,maxlevel=2)
printLocations(itemid = 3, level = 1,maxlevel=3)


ss=spreadsheet()
ss.readTabText('EDM_Inventory.csv')

ss.getCols([0])

available fields
ss.headings
ss.rows
ss.verdata
ss.verheadings

for ssloc in ss.getCols([2]):
    print ssLocToDbLoc(ssloc[0])

printItem(itemRestApi.getFirstItemRelationshipList(ser714id,'Location'))




printItem(itemRestApi.getPropertiesForItemByItemId( edmid))

ser714 = itemRestApi.addItem(
    name='Ser.714',
    domainName="Inventory",
    derivedFromItemId=edmid, 
    itemIdentifier1='SN# 25',
    itemProjectName='APS-OPS')

ser714id = ser714['id']




ser714 = itemRestApi.getItemById(ser714id)

printItem(ser714)

ssloc = 'RF2 Rack #1'
dbloc = ssLocToDbLoc(ssloc)
ssslot = '3'
dbloc['ssloc'] = ssloc + ", slot " + ssslot


itemRestApi.addItemRelationship(
    ser714id, 
    dbloc['id'], 
    'Location', 
    relationshipDetails=dbloc['ssloc'])





############################################################
#add to catalog
edm = itemRestApi.addItem(
    domainName='Catalog', 
    name='Envelop Detector Module',
    itemProjectName="APS-OPS",
    itemIdentifier1='EDM100')

printItem(edm)

edmid = edm['id']

edm = itemRestApi.getItemById(edmid)

itemid = findCatelogItem("Envelop Detector Module","EDM100")


ss=spreadsheet()
ss.readTabText('EDM_Inventory.csv')

edmInventory(itemid)

checkInventory(itemid)
checkInventory(2449,updateStatusByLocation)


"""





