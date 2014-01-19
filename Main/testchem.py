import pyparsing as pyp
import numpy as np

numList = ['1','2','3','4','5','6','7','8','9']
atomicFamilies = {1:"Alkali Metals",
                  2:"Alkaline Earth Metals",
                  3:"Transition Metals",
                  4:"Transition Metals",
                  5:"Transition Metals",
                  6:"Transition Metals",
                  7:"Transition Metals",
                  8:"Transition Metals",
                  9:"Transition Metals",
                  10:"Transition Metals",
                  11:"Transition Metals",
                  12:"Transition Metals",
                  13:"13",
                  14:"14",
                  15:"15",
                  16:"16",
                  17:"Halogens",
                  18:"Noble Gases",
                  19:"Lanthanoids",
                  20:"Actinoids"}

class Chemistry: pass

class Reactions(Chemistry): pass

class Element(Chemistry):
        
    def __init__(self,
                 mass,
                 number,
                 symbol,
                 name,
                 electronegativity,
                 family):
        """Creates an element object using the atomic mass, number, symbol, name, electronegativity and atomic family"""
        #!!Needs octet rule support!!
        
        self.atomicMass = mass
        self.atomicNumber = number
        self.atomicSymbol = symbol
        self.elementName = name
        self.electroneg = electronegativity
        self.atomicFamily = family
        self.bondList = []  
        
    def __str__(self):
        """The string version of an element object -- its name"""
        return self.elementName
            
    def getmass(self):
        """returns the atomic mass as a float"""
        return self.atomicMass
        
    def getnumber(self):
        """returns the atomic number as an integer"""
        return self.atomicNumber
        
    def getname(self):
        """returns the element's name as a string"""
        return self.elementName
        
    def getsymbol(self):
        """returns the atomic symbol as a string"""
        return self.atomicSymbol
        
    def getneg(self):
        """"returns the electronegativity as a float"""
        return self.electroneg
                
    def addBond(self,end,order=1):
        """adds a Bond object to the element's list of Bonds.
        !!Needs more support for if number of bonds exceeds octet!!"""
        self.bondList.append(Bond(self,end,order))
        
    def getBonds(self):
        """returns the list of bonds the element is a part of"""
        return self.bondList
        
    def getfam(self):
        """returns the atomic family as a string"""
        return atomicFamilies[int(self.atomicFamily)]
        
def bothBonds(first,second,order=1):
    """adds the bond to both elements"""
    first.addBond(second,order)
    second.addBond(first,order)
                
class Mendeleev(Chemistry):  
          
    def __init__(self,
                 loc1,
                 loc2):
        """Creates a periodic table of the elements. Only call this once"""
        
        #generates an array of 1s and 0s to create the shape of the periodic table     
        ptable = np.genfromtxt(loc1,dtype='S', unpack=True)
        tempTable = ptable.reshape((7,32))
        theTable = []
        
        #Takes the data for each element and puts it into the appropriate list
        n, symbol, name, family, mass, eneg = np.genfromtxt(loc2, dtype='S', unpack=True)
        nList = n.astype(int)
        nameList = name.astype(str)
        symList = symbol.astype(str)
        famList = family.astype(int)
        massList = mass.astype(float)
        negList = eneg.astype(float)
        
        #Populates the periodic table with element objects
        inc=0
        for i in range(7):
            for j in range(32):
                if tempTable[i][j] == '0':
                    theTable.append(None)
                else:
                    anElement=Element(massList[inc],
                                      nList[inc],
                                      symList[inc],
                                      nameList[inc],
                                      negList[inc],
                                      famList[inc])
                    theTable.append(anElement)
                    inc+=1  
        
        #shapes the periodic table        
        self.finalTable = np.array(theTable).reshape((7,32))
    
    def getTable(self):
        """returns the numpy array that serves as the periodic table"""            
        return self.finalTable
        
    def printableTable(self):
        """returns the periodic table in a string format"""
        stringVal = ''
        for rows in self.finalTable:
            for columns in rows:
                if columns != None:
                    stringVal += str(columns)+'\n'
        return stringVal

    def getElement(self,
                   symbol):
        """Returns the appropriate element object given the element's symbol"""
        for rows in self.finalTable:
            for columns in self.finalTable:
                for atom in columns:
                    if atom != None:
                        if symbol == atom.getsymbol():
                            return atom
    
    def __str__(self):
        """String representation of the periodic table"""
        return "The Periodic Table of the Elements"
        
class Bond(Chemistry):
    
    def __init__(self,
                 start,
                 end,
                 order=1):
        """Creates a Bond object - input the two elements, and the order (default 1) of the bond"""
               
        #Declares the level of the bond and the elements bonded by it
        self.startElement = start
        self.endElement = end
        self.order = order
        if self.order == 1:            
            self.descriptor = 'single'
        elif self.order == 2:
            self.descriptor = 'double'
        elif self.order == 3:
            self.descriptor = 'triple'
        else:
            self.descriptor = None    
            
    def getStart(self):
        """returns the element object at the 'front' of the bond"""
        return self.startElement
        
    def getEnd(self):
        """returns the element object at the 'back' of the bond"""
        return self.endElement
        
    def getOrder(self):
        """returns the order of the bond as an integer"""
        return self.order
        
    def getDescrip(self):
        """returns a string version of the bond's order"""
        return self.descriptor   

    def __str__(self):
        """returns a string depiction of a bond"""
        if self.order == 1:
            return 'sb'
        elif self.order == 2:
            return 'db'
        elif self.order == 3:
            return 'tb'
        else:
            return 'None'

def branching(anObject,structure,location):
    """recursive function that takes an array of element objects, a structure to place them in
    and the starting location and uses it to make a compound"""
    #Creates the components
    primary = anObject[0]
    substituents = anObject[1:][0]
    locDict = {}
    
    for i in range(len(substituents)):
        try:locDict[i] = int(substituents[i])
        except (ValueError,TypeError,AttributeError): pass
            
    locKeys = locDict.keys();locKeys.sort();locKeys.reverse()
    for item in locKeys:
        theElement = substituents[item-1]
        aNum = int(substituents.pop(item))
        if aNum > 1:
            for i in range(aNum-1):
                substituents.insert(i+item,theElement)

    locX = location[0]
    locY = location[1]
    structure[locY][locX] = primary
    
    #Checks if the 4 cardinal points are occupied
    if (locY - 2) < 0: a1 = 1
    else:
        try:a1 = structure[locY-2][locX]
        except:a1 = 1
    if (locX - 2) < 0: a2 = 1
    else:
        try:a2 = structure[locY][locX-2]
        except: a2 = 1
    
    try: a3 = structure[locY+2][locX]
    except: a3 = 1
    try: a4 = structure[locY][locX+2]
    except: a4 = 1
    
    cardinals = [a1,a2,a3,a4]

    status = [] #reports on the four cardinal positions (True if empty, False if not)

    for direction in cardinals:
        if direction == None: status.append(True)
        else: status.append(False)
                        
    i=1
    j=0

    for point in status:
        if j <= len(substituents)-1:
            if point:
                theElement = substituents[j]
                print stringify(theElement)
                aBool = False
                bBool = False
                cBool = False
                if type(theElement) == type([]) or type(theElement) == type(np.zeros(1)):
                    for part in theElement:
                        if type(part) == type([]) or type(part) == type(np.zeros(1)):
                            aBool = True
                if aBool:
                    if type(theElement[0]) == type(''):
                        if theElement[0][0] == '+':
                            theElement[0] = theTable.getElement(theElement[0][1:])
                            bBool = True
                        elif theElement[0][0] == '*':
                            theElement[0] = theTable.getElement(theElement[0][1:])
                            cBool = True
                    if i == 1:
                        subStruct = np.empty((3,5),dtype = object)
                        tempstructure = branching(theElement,subStruct,[2,2])
                        structure[locY-2][locX] = tempstructure
                        if bBool:
                            structure[locY-1][locX] = Bond(primary,tempstructure[2][2],2)
                            bothBonds(primary,tempstructure[2][2],2)
                        elif cBool:
                            structure[locY-1][locX] = Bond(primary,tempstructure[2][2],3)
                            bothBonds(primary,tempstructure[2][2],3)
                        else:                            
                            structure[locY-1][locX] = Bond(primary,tempstructure[2][2])
                            bothBonds(primary,tempstructure[2][2],1)

                    if i == 2:
                        subStruct = np.empty((5,3),dtype = object)
                        tempstructure = branching(theElement,subStruct,[2,2])
                        structure[locY][locX-2] = tempstructure
                        if bBool:
                            structure[locY][locX-1] = Bond(primary,tempstructure[2][2],2)
                            bothBonds(primary,tempstructure[2][2],2)
                        elif cBool:
                            structure[locY][locX-1] = Bond(primary,tempstructure[2][2],3)
                            bothBonds(primary,tempstructure[2][2],3)
                        else:                            
                            structure[locY][locX-1] = Bond(primary,tempstructure[2][2])
                            bothBonds(primary,tempstructure[2][2],1)
                    if i == 3:
                        subStruct = np.empty((3,5),dtype = object)
                        tempstructure = branching(theElement,subStruct,[2,0])
                        structure[locY+2][locX] = tempstructure
                        if bBool:
                            structure[locY+1][locX] = Bond(primary,tempstructure[0][2],2)
                            bothBonds(primary,tempstructure[0][2],2)
                        elif cBool:
                            structure[locY+1][locX] = Bond(primary,tempstructure[0][2],3)
                            bothBonds(primary,tempstructure[0][2],3)
                        else:                            
                            structure[locY+1][locX] = Bond(primary,tempstructure[0][2])
                            bothBonds(primary,tempstructure[0][2],1)
                    if i == 4:
                        subStruct = np.empty((5,3),dtype = object)
                        tempstructure = branching(theElement,subStruct,[0,2])
                        structure[locY][locX+2] = tempstructure
                        if bBool:
                            structure[locY][locX+1] = Bond(primary,tempstructure[2][0],2)
                            bothBonds(primary,tempstructure[2][0],2)
                        elif cBool:
                            structure[locY][locX+1] = Bond(primary,tempstructure[2][0],3)
                            bothBonds(primary,tempstructure[2][0],3)
                        else:                            
                            structure[locY][locX+1] = Bond(primary,tempstructure[2][0])
                            bothBonds(primary,tempstructure[2][0],1)
                    j+=1
                else:
                    try:
                        theElement = theElement[0]
                        if type(theElement) == type(''):
                            if theElement[0] == '+':
                                tempElement = theElement[1:]
                                theElement = theTable.getElement(tempElement)
                                bBool = True
                            elif theElement[0] == '*':
                                tempElement = theElement[1:]
                                theElement = theTable.getElement(tempElement)
                                cBool = True
                        if i == 1:
                            #Put something north
                            structure[locY-2][locX] = theElement
                            if bBool:
                                structure[locY-1][locX] = Bond(primary,theElement,2)
                                bothBonds(primary,theElement,2)
                            elif cBool:
                                structure[locY-1][locX] = Bond(primary,theElement,3)
                                bothBonds(primary,theElement,3)
                            else:                            
                                structure[locY-1][locX] = Bond(primary,theElement)
                                bothBonds(primary,theElement,1)
                        if i == 2:
                            #Put something west
                            structure[locY][locX-2] = theElement
                            if bBool:
                                structure[locY][locX-1] = Bond(primary,theElement,2)
                                bothBonds(primary,theElement,2)
                            elif cBool:
                                structure[locY][locX-1] = Bond(primary,theElement,3)
                                bothBonds(primary,theElement,3)
                            else:                            
                                structure[locY][locX-1] = Bond(primary,theElement)
                                bothBonds(primary,theElement,1)
                        if i == 3:
                            #Put something south
                            structure[locY+2][locX] = theElement
                            if bBool:
                                structure[locY+1][locX] = Bond(primary,theElement,2)
                                bothBonds(primary,theElement,2)
                            elif cBool:
                                structure[locY+1][locX] = Bond(primary,theElement,3)
                                bothBonds(primary,theElement,3)
                            else:                            
                                structure[locY+1][locX] = Bond(primary,theElement)
                                bothBonds(primary,theElement,1)
                        if i == 4:
                            #Put something east
                            structure[locY][locX+2] = theElement                        
                            if bBool:
                                structure[locY][locX+1] = Bond(primary,theElement,2)
                                bothBonds(primary,theElement,2)
                            elif cBool:
                                structure[locY][locX+1] = Bond(primary,theElement,3)
                                bothBonds(primary,theElement,3)
                            else:                            
                                structure[locY][locX+1] = Bond(primary,theElement)
                                bothBonds(primary,theElement,1)
                        j += 1
                    except:
                        #Do something here that locates the proper place on the ring to bond
                        
                        j += 1
                i+=1

    return structure

###Defines the locations of the tables
ptableLoc = 'C:\Users\Dan\Documents\GitHub\Chemistry\Main\ptable.txt'
elementsLoc = 'C:\Users\Dan\Documents\GitHub\Chemistry\Main\elements.txt'        
theTable = Mendeleev(ptableLoc,elementsLoc)          

def stringify(anObject):
    """takes an array and converts every object within to a string"""
    if type(anObject) == type([]) or type(anObject) == type(np.zeros(1)):
        newList = range(len(anObject))
        for i in range(len(anObject)):
            newList[i] = stringify(anObject[i])
        return newList
    if type(anObject) == type(''):return anObject
    if anObject == None:return anObject
    else:return str(anObject)
    
    """height = len(anArray)
    width = len(anArray[0])
    newArray = np.empty((height,width),dtype=object)
    for i in range(height):
        for j in range(width):
            if type(anArray[i][j]) == type([]) or type(anArray[i][j]) == type(np.zeros(1)): newArray[i][j] = stringify(anArray[i][j])
            elif anArray[i][j] == None: newArray[i][j] = anArray[i][j]
            else: newArray[i][j] = str(anArray[i][j])
                                    
    return newArray"""

def stoElement(anObject):
    """recursive function that turns atomic symbols into string representations of their element"""
    if type(anObject) == type([]) or type(anObject) == type(np.zeros(1)):
        newList = range(len(anObject))
        for i in range(len(anObject)):
            if anObject[i][0] == '@':
                print newList[i]
                newList[i] = Ring(toElement(anObject[i][1:]))
                print newList[i]
            else:
                newList[i] = toElement(anObject[i])
        return newList
    
    if type(anObject) == type(''):
        if anObject[0] in ['+','*','@','!']:
            return str(anObject)
        if anObject[0] not in numList: anObject = str(theTable.getElement(anObject))
        return anObject          
        
def toElement(anObject):  
    """Recursive function that turns atomic symbols into their element"""
    if type(anObject) == type([]) or type(anObject) == type(np.zeros(1)):
        newList = range(len(anObject))
        for i in range(len(anObject)):
            if '@' in anObject[i]:
                aNum = anObject[i].find('@')
                newList[i] = [anObject[i][:aNum],Ring(toElement(anObject[i+1:]))]
            else:
                newList[i] = toElement(anObject[i])
        return newList
    
    if type(anObject) == type(''):
        if anObject[0] in ['+','*','@','!']:
            return anObject
        if anObject[0] not in numList: anObject = theTable.getElement(anObject)
        return anObject              
                                                                              
class Compound(Chemistry):
    
    def __init__(self,formula):   
        """Input a formula for a chemical compound.  (currently) requires special
        syntax in order to be properly parsed."""

        #Initializes variables
        self.formula = formula
        self.centers = formula.split()
        size = (6*len(self.centers)+1)**2
        sidelen = int(np.sqrt(size))
        self.structure = np.empty((sidelen,sidelen), dtype = object)
        self.strstructure = np.empty((sidelen,sidelen), dtype = object)
        
        #Separates the compound
        for i in range(len(self.centers)):
            self.centers[i] = [self.centers[i][:self.centers[i].find('(')],
                               pyp.nestedExpr().parseString(self.centers[i][1:]).asList()[0]]
        
        #Associates symbols with their element objects
        #self.stringCenters = stoElement(self.centers)
        self.centers = toElement(self.centers)
        
        #Associates the compound with self.structure and creates bonds
        middle = int(len(self.structure)/2)
        i=middle
        j=2
        k=0
        
        while k < len(self.centers):
            self.structure = branching(self.centers[k],self.structure,[j,i])
            k+=1
            j+=2            
       
        j=3
        for i in range(len(self.centers)-1):
           self.structure[middle][j] = Bond(self.structure[middle][j-1],self.structure[middle][j+1],1)
           bothBonds(self.structure[middle][j-1],self.structure[middle][j+1],1)
           j+=2
        
        self.strstructure = stringify(self.structure)
        print self.strstructure
        
    def __str__(self):
        """the string representation of a compound object"""
        return str(self.formula)  
        
def populate(anObject):
    """"""
    if type(anObject) == type([]) or type(anObject) == type(np.zeros(1)):
        try:
            locDict = {}
            for i in range(len(anObject)):
                try:locDict[i] = int(anObject[i])
                except (ValueError,TypeError,AttributeError): pass
            
            locKeys = locDict.keys();locKeys.sort();locKeys.reverse()
            if len(locKeys) == 0:raise Exception
                
            for item in locKeys:
                anObject[item-1] = populate(anObject[item-1])
                insertObject = anObject[item-1]
                aNum = int(anObject.pop(item))
                if aNum > 1:
                    for i in range(aNum-1):anObject.insert(i+item,insertObject)
            return anObject
        except:
            for i in range(len(anObject)):anObject[i] = populate(anObject[i])
            return anObject
            
        for i in range(len(anObject)):anObject[i] = populate(anObject[i])
        return anObject
        
    if type(anObject) == type(''):return anObject 
    
    else:return anObject

def circulate(aRing,aStruc):
    #aRing = stringify(aRing[0])
    """"""
    k = 0
    primarys = [part[0] for part in aRing]
    substituents = [part[1] for part in aRing]
    if len(aStruc[0])%2 == 0:
        for i in range(2,len(aStruc[0])-3,2):
            aStruc[2][i] = primarys[k]
            if i == 2:
                aStruc[0][i] = substituents[k][0][0]
                aStruc[1][i] = Bond(aStruc[2][i],substituents[k][0][0])
                bothBonds(aStruc[2][i],substituents[k][0][0])
                aStruc[2][i-2] = substituents[k][1][0]
                aStruc[1][i-2] = Bond(aStruc[2][i-2],substituents[k][1][0])
                bothBonds(aStruc[2][i],substituents[k][1][0])
            else:
                aStruc[0][i-1] = substituents[k][0][0]
                aStruc[1][i-1] = Bond(aStruc[2][i],substituents[k][0][0])
                bothBonds(aStruc[2][i],substituents[k][0][0])
                aStruc[0][i] = substituents[k][1][0]
                aStruc[1][i] = Bond(aStruc[2][i],substituents[k][1][0])
                bothBonds(aStruc[2][i],substituents[k][1][0])
            k += 1            
        aStruc[3][-3] = primarys[k]
        aStruc[2][-1] = substituents[k][0][0]
        aStruc[2][-2] = Bond(aStruc[3][-3],substituents[k][0][0])
        bothBonds(aStruc[3][-3],substituents[k][0][0])
        aStruc[3][-1] = substituents[k][1][0]
        aStruc[3][-2] = Bond(aStruc[3][-3],substituents[k][1][0])
        bothBonds(aStruc[3][-3],substituents[k][1][0])
        k += 1
        for i in range(len(aStruc[2])-4,2,-2):
            aStruc[4][i] = primarys[k]
            aStruc[6][i+1] = substituents[k][0][0]
            aStruc[5][i+1] = Bond(aStruc[4][i],substituents[k][0][0])
            bothBonds(aStruc[4][i],substituents[k][0][0])
            aStruc[6][i] = substituents[k][1][0]
            aStruc[5][i] = Bond(aStruc[4][i],substituents[k][1][0])
            bothBonds(aStruc[4][i],substituents[k][1][0])
            k += 1
        aStruc[4][2] = primarys[k]
        aStruc[4][0] = substituents[k][0][0]
        aStruc[4][1] = Bond(aStruc[4][2],substituents[k][0][0])
        bothBonds(aStruc[4][2],substituents[k][0][0])
        aStruc[6][2] = substituents[k][1][0]
        aStruc[5][2] = Bond(aStruc[4][2],substituents[k][1][0])
        bothBonds(aStruc[4][2],substituents[k][1][0])
        for i in range(3,len(aStruc[0])-2,2):
            aStruc[2][i] = Bond(aStruc[2][i-1],aStruc[2][i+1])
            bothBonds(aStruc[2][i-1],aStruc[2][i+1])
        for i in range(len(aStruc[2])-3,2,-2):
            aStruc[4][i] = Bond(aStruc[4][i-1],aStruc[4][i+1])
            bothBonds(aStruc[4][i-1],aStruc[4][i+1])
        aStruc[3][2] = Bond(aStruc[2][2],aStruc[4][2])
        #bothBonds(aStruc[2][2],aStruc[4][2])
    else:
        for i in range(2,len(aStruc[0])-2,2):
            aStruc[2][i] = primarys[k]
            if i == 2:
                aStruc[0][i] = substituents[k][0][0]
                aStruc[1][i] = Bond(aStruc[2][i],aStruc[0][i])
                bothBonds(aStruc[2][i],aStruc[0][i])
                aStruc[2][0] = substituents[k][1][0]
                aStruc[1][0] = Bond(aStruc[2][i],aStruc[2][0])
                bothBonds(aStruc[2][i],aStruc[2][0])
            elif i == len(aStruc[0])-3:
                aStruc[0][i] = substituents[k][0][0]
                aStruc[1][i] = Bond(aStruc[2][i],aStruc[0][i])
                bothBonds(aStruc[2][i],aStruc[0][i])
                aStruc[2][-1] = substituents[k][1][0]
                aStruc[2][-2] = Bond(aStruc[2][i],aStruc[2][-1])
                bothBonds(aStruc[2][i],aStruc[2][-1])
            else:
                aStruc[0][i-1] = substituents[k][0][0]
                aStruc[1][i-1] = Bond(aStruc[2][i],aStruc[0][i-1])
                bothBonds(aStruc[2][i],aStruc[0][i-1])
                aStruc[0][i] = substituents[k][1][0]
                aStruc[1][i] = Bond(aStruc[2][i],aStruc[0][i])
                bothBonds(aStruc[2][i],aStruc[0][i])
            k += 1
        for i in range(len(aStruc[2])-3,0,-2):
            aStruc[4][i] = primarys[k]
            if i == 2:
                aStruc[-1][i] = substituents[k][0][0]
                aStruc[-2][i] = Bond(aStruc[4][i],aStruc[-1][i])
                bothBonds(aStruc[4][i],aStruc[-1][i])
                aStruc[4][0] = substituents[k][1][0]
                aStruc[4][1] = Bond(aStruc[4][i],aStruc[4][0])
                bothBonds(aStruc[4][i],aStruc[4][0])
            elif i == len(aStruc[2]) - 3:
                aStruc[4][-1] = substituents[k][0][0]
                aStruc[4][-2] = Bond(aStruc[4][i],aStruc[4][-1])
                bothBonds(aStruc[4][i],aStruc[4][-1])
                aStruc[-1][i] = substituents[k][1][0]
                aStruc[-2][i] = Bond(aStruc[4][i],aStruc[-1][i])
                bothBonds(aStruc[4][i],aStruc[-1][i])
            else:
                aStruc[-1][i+1] = substituents[k][0][0]
                aStruc[-2][i+1] = Bond(aStruc[4][i],aStruc[-1][i+1])
                bothBonds(aStruc[4][i],aStruc[-1][i+1])
                aStruc[-1][i] = substituents[k][1][0]
                aStruc[-2][i] = Bond(aStruc[4][i],aStruc[-1][i])
                bothBonds(aStruc[4][i],aStruc[-1][i])
            k+= 1
        for i in range(3,len(aStruc[0])-2,2):
            aStruc[2][i] = Bond(aStruc[2][i-1],aStruc[2][i+1])
            bothBonds(aStruc[2][i-1],aStruc[2][i+1])
        aStruc[3][-3] = Bond(aStruc[2][-3],aStruc[4][-3])
        bothBonds(aStruc[2][-3],aStruc[4][-3])
        for i in range(len(aStruc[2])-4,2,-2):
            aStruc[4][i] = Bond(aStruc[4][i+1],aStruc[4][i-1])
            bothBonds(aStruc[4][i+1],aStruc[4][i-1])
        aStruc[3][2] = Bond(aStruc[2][2],aStruc[4][2])
        bothBonds(aStruc[2][2],aStruc[4][2])
        
    return aStruc   
        
class Ring(Compound):
    def __init__(self,ringList):
        """"""
        self.ringList = populate(ringList)[0]
        self.aLen = len(self.ringList)*2
        self.structure = np.empty((7,4+(self.aLen-2)/2),dtype=object)
        print self.structure
        self.structure = circulate(self.ringList,self.structure)
        print stringify(self.structure)
        
    def __str__(self):
        return 'aRing'  

class BridgedStructure(Ring):
    
    def __init__(self,aRing):pass

def BeginProgram():
    """Function that initializes the program""" 
   
    ###Creates a (numpy) array version of the table then a visual (string) version of the table
    #periodicTable = theTable.getTable()
    #printTable = theTable.printableTable()
    
    ###sample compound    
    #testCompound = Compound("C((C((C((H)3))3))3) C((H)2(Cl)1)") #Compound C(C(CH3)3)3)C(H2Cl1)
    #print testCompound #Testing
    #testCompound = Compound("C((+O)2)")
    #print testCompound #Testing
    #testCompound = Compound("N((*N)1)")
    #print testCompound #Testing
    #testCompound = Compound('C((+O((C((H)3))1))1(H)2))')
    #print testCompound #Testing
    testCompound = Compound('C((!@((C((H)2))5(C((H)1(!)1))1))1(H)3)')
    print testCompound
    
BeginProgram()