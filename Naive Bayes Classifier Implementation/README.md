##### - This program is an implementation of Naive Bayes Classifier in Python.

##### - Run the program
    bluenose: python naivebayes.py
    python version: python 2.7
   
    The results are saved to file 'Result.txt', to view the results
    bluenose: cat Result.txt
    
##### - Overview the program code:

    There is 1 python file, containing 6 functions including main():
    
    loadTrainFile()                 - read the training data from file
    loadTestFile()                  - read the testing data from file
    getTargetAttribute()            - get the attribute to predict from user
    training()                      - use training the data to build the classification knowledge
    predict()                       - predict testing data
    
    
##### - The following is the code structure:

    main()  -----> loadTrainFile
            -----> loadTestFile
            -----> getTargetAttribute
                    -----> getPossibleTargets
                    -----> getUserInput
            -----> training
                    -----> build a dictionary to store the target attribute values and occurrences
                    -----> build a dictionary to store the occurrences of each attribute pair
                    -----> get the classifier
            -----> predict
                    -----> get the prediction result
                    -----> save the result to file
           

##### - Bonus
    
    The dataset is student academic performance dataset. I split the dataset into 70% training, and 30% testing.
    Afterwards, I perform Naive Bayes and C4.5 classifier, the result is analyzed in the following table.
    
    |           | Naïve Bayes          | C4.5                       |
    |-----------|----------------------|----------------------------|
    | Algorithm | Priori probabilities | Entropy & Information gain |
    | Accuracy  | 71/107               | 85/107                     |
    | Speed     | Relatively slower    | Relatively quicker         |
    
 