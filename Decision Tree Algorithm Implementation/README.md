
##### - This program is an implementation of decision tree algorithm ID3 in Python.

##### - Overview the program code:
    
    There is 1 python file, containing 1 class, and 10 functions including main():
    
    class Node                  - store node information
    readData()                  - read data from file
    getPossibleTargets()        - find the possible binary target attributes
    setTarget()                 - get target attribute from user input
    entropy()                   - calculate target attribute entropy
    subEntropiesForAttr()       - calculate the entropy of attributes base on the target
    buildTree()                 - build the decision tree base on the splitting criterion
    printTree()                 - print the rules
    
    
    
##### - The following is the code structure:

    main()  -----> readData
            -----> getPossibleTargets
            -----> setTarget
            -----> buildTree
                    -----> calculate target entropy
                    -----> find max infoGain attribute
                    -----> create node for this attribute
                    -----> recursively add child node for this node
            -----> printTree
            -----> writeRulesToFile
 
 

##### - Run the program
    bluenose: python id3.py
    python version: python 2.7
    
    The results are saved to file Rules, to view the results
    bluenose: more Rules
    
##### - Note
    When execute the algorithm, please make sure input as the hints.