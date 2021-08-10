import copy

#load the training file
def loadTrainFile():
    while True:
        try:
            filename = raw_input('Please enter a training file: ')
            file = open(filename, 'rU')
            data = [line.split() for line in file.readlines() if line.strip()]
            return data
            break
        except IOError:
            print "No such file, please select again."

#load the testing file
def loadTestFile():
    while True:
        try:
            filename = raw_input('Please enter a testing file: ')
            file = open(filename, 'rU')
            data = [line.split() for line in file.readlines() if line.strip()]
            return data
            break
        except IOError:
            print "No such file, please select again."

#get the attribute to predict
def getTargetAttribute(data):
    print "Please choose an attribute (by number) "
    for item in data[0]:
        print data[0].index(item) + 1,item
    while True:
        try:
            choice = input()
            return data[0][int(choice) - 1]
            break
        except IndexError:
            print "Selection out of bound, please select again."

#training the file, calculate the classifier
def training(dataset, targetAttr):
    index = dataset[0].index(targetAttr)
    priorPair = dict()
    targetValues = dict()
    for line in dataset[1:]:
        if line[index] in targetValues.keys():
            targetValues[line[index]] += 1
        else:
            targetValues[line[index]] = 1
        for i in range(len(line)):
            if i != index:
                item = ((dataset[0][i], line[i]), line[index])
                if item in priorPair.keys():
                    priorPair[item] += 1
                else:
                    priorPair[item] = 1
    classifier = [priorPair,targetValues]
    return classifier

#predict the testing file, output the results
def predict(classifier,testData,targetAttr):
    OriAttributes = testData[0]
    index = OriAttributes.index(targetAttr)
    attributes = copy.deepcopy(OriAttributes)
    del attributes[index]
    attrDict = classifier[0]
    tarDict = classifier[1]
    targetValueSet = tarDict.keys()
    for line in testData[1:]:
        tmp = copy.deepcopy(line)
        del tmp[index]
        lineRes = dict()
        for value in targetValueSet:
            for i in range(len(tmp)):
                pair = (attributes[i], tmp[i])
                vo = [key[0][1] for key in attrDict.keys() if key[0][0] == pair[0]]
                k = len(set(vo))
                m = k
                p = 1.0/k
                # print attributes[i], "P:", p
                if (pair, value) in attrDict.keys():
                    #pos = float(attrDict[(pair, value)] + m * p) / (tarDict[value] + m)
                    pos = attrDict[(pair, value)] / float(tarDict[value])
                else:
                    pos = float(0 + m * p) / (tarDict[value] + m)
                if value in lineRes.keys():
                    lineRes[value] *= pos
                else:
                    lineRes[value] = pos
            lineRes[value] *= tarDict[value] / float(len(testData) - 1)

        maximum = max([lineRes[key] for key in lineRes.keys()])
        line.append([key for key in lineRes.keys() if lineRes[key] == maximum][0])
    file = open("Result.txt", "w+")
    testData[0].append("Classfication")
    for item in testData:
        file.write("%s\n" % item)
    count = 0
    for line in testData:
        if line[-1] == line[index]:
            count+=1
    file.write("Accuracy:"+str(count)+"/"+str((len(testData)-1)))



def main():
    trainingData = loadTrainFile()
    testingData = loadTestFile()
    targetAttr = getTargetAttribute(trainingData)
    print "select attribute =",targetAttr
    classfier = training(trainingData, targetAttr)
    predict(classfier,testingData,targetAttr)
    print "The result is in the file 'Result.txt'. "




if __name__ == '__main__':
    main()
