import math
import copy

###############################
#Define a tree node
class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
    def addBranch(self, branchName, entropy, dataset, target):
        group = [dataset[0]] + list(dataset[i] for i in range(len(dataset)) if dataset[i][0] == branchName)
        if entropy == 0:
            childNode = ""
            for i in range(len(group[0])):
                if group[0][i] == target:
                    childNode = group[1][i]
            self.children.append({"branch": branchName, "entropy":entropy, "child": childNode})
        elif entropy != 0 and len(group[0]) > 3:
            group = map(lambda x: x[1:], group)
            childNode = buildTree(group, target)
            self.children.append({"branch": branchName, "entropy":entropy, "child": childNode})
        else:
            group = map(lambda x: x[1:], group)
            targetValues = list(set(targetColWithoutHeader(target, group)))
            count1 = len(filter(lambda x: x == targetValues[0], targetColWithoutHeader(target, group)))
            count2 = len(group) - 1 - count1
            if count1 >= count2:
                self.children.append({"branch": branchName, "entropy":entropy, "child": targetValues[0]})
            else:
                self.children.append({"branch": branchName, "entropy":entropy, "child": targetValues[1]})

    def __str__(self):
        res = "Node Name: %s\n" % self.name
        for item in self.children:
            res += "Branch: %s %s\n" % (str(item["branch"]),  str(item["entropy"]))
        return res

########### Helper functions
def changeColToBeginning(originalDataset, colIndex):
    dataset = copy.deepcopy(originalDataset)
    tmp = []
    for i in range(len(dataset)):
        tmp.append(dataset[i][0])
    for i in range(len(dataset)):
        dataset[i][0] = dataset[i][colIndex]
    for i in range(len(dataset)):
        dataset[i][colIndex] = tmp[i]
    return dataset

def targetColWithoutHeader(target, lines):
    return list(lines[i][j] for i in range(len(lines)) for j in range(len(lines[i])) if lines[0][j] == target and i != 0)

##########
#Read data from file
def readData():
    while True:
        try:
            filename = raw_input('What is the name of the file containing your data? (data1, data2, data3, adult1, adult2)')
            file = open(filename, 'rU')
            data = [line.split() for line in file.readlines() if line.strip()]
            return data
            break
        except IOError:
            print "No such file, please select again (data1, data2, data3, adult1, adult2)."

#find the possible binary target attributes
def getPossibleTargets(lines):
    possibleTargets = []
    attributes = lines[0]
    for i in range(len(attributes)):
        col = list(line[i] for line in lines)[1:]
        if len(set(col)) == 2:
            possibleTargets.append(attributes[i])
    return possibleTargets

#get target attribute from user input
def setTarget(possibleTarget):
    print "Please select the target attribute: ", possibleTarget, "by input the full target attribute name"
    target = raw_input()
    return target

#calculate target attribute entropy
def entropy(dataset, target):
    targetValues = list(set(targetColWithoutHeader(target, dataset)))
    count1 = len(filter(lambda x: x == targetValues[0], targetColWithoutHeader(target, dataset)))
    count2 = len(dataset) - 1 - count1
    length = count2 + count1
    coe1 = float(count1)/length
    coe2 = float(count2)/length
    if coe1 == 0:
        return - round(coe2 * math.log(coe2,2), 3)
    elif coe2 == 0:
        return round(-coe1 * math.log(coe1,2))
    else:
        return round(-coe1 * math.log(coe1,2) - coe2 * math.log(coe2,2), 3)

#calculate the entropy of attributes base on the target
def subEntropiesForAttr(dataset, colIndex, target):
    dataset = changeColToBeginning(dataset, colIndex)
    totalRecords = float(len(dataset) - 1)
    targetValues = list(set(targetColWithoutHeader(target, dataset)))
    entropies = []
    attrValueSet = set(dataset[i][0] for i in range(len(dataset)) if i != 0)

    for value in attrValueSet:
        group = [dataset[0]] + list(dataset[i] for i in range(len(dataset)) if dataset[i][0] == value)
        entropies.append([value, ((len(group) - 1)/totalRecords)*entropy(group, target)])
    # print "sub entropies", entropies
    return entropies

#build the decision tree base on the splitting criterion
def buildTree(dataset, target):
    datasetEntropy = entropy(dataset, target)
    attrs = dataset[0]
    gains = []
    rootName = ""
    maxInfoGain = 0
    children = []
    keyCol = 0
    for i in range(len(attrs)):
        if attrs[i] != target:
            subEn = subEntropiesForAttr(dataset, i, target)
            gain = datasetEntropy - reduce(lambda x, y: x + y, [subEn[j][1] for j in range(len(subEn))], 0)
            gains.append([attrs[i], gain])
            if gain >= maxInfoGain:
                rootName = attrs[i]
                maxInfoGain = gain
                children = subEn
                keyCol = i
    rootNode = Node(rootName)
    children = sorted(children, key=(lambda x: x[1]), reverse=True)
    for item in children:
        rootNode.addBranch(item[0], item[1], changeColToBeginning(dataset, keyCol), target)
    # print rootNode
    return rootNode

#print the decision tree
def printTree(rootNode, target, init):
    res = ""
    for child in rootNode.children:
        res += init + "if %s is %s, then " % (rootNode.name, child["branch"])
        if isinstance(child["child"], Node):
            res += "\n" + printTree(child["child"], target, init + "\t")
        else:
            res += target + " is " + child["child"] + "\n"
    return res

def main():
    dataset = readData()
    possibleTargets = getPossibleTargets(dataset)
    target = setTarget(possibleTargets)
    tree = buildTree(dataset, target)
    file = open("Rules","w+")
    file.write("Target attribute is " + target + "\n\n\n")
    rules = printTree(tree, target, "")
    file.write(rules)
    print "The results are saved in the file Rules."
    print "********  Algorithm Finished ********"

if __name__ == '__main__':
    main()
