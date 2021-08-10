
##### - This program is an implementation of association rule mining algorithm Apriori in Python.

##### - Overview the program code:

    There is one python file, containing 9 functions including main():
    
    load_database()                 -load data from file
    build_first_itemset()           -generate distinct items
    apply_min_support()             -delete items which do not meet min_support_requirements
    generate_candidate_itemset()    -generate candidate itemsets by joining two sets
    candidate_subsets()             -generate all subsets
    generate_frequent_itemset()     -generate frequent itemsets by applying the min_support
    create_and_write_rules()        -create rules meeting min_confidence requirements
    run_apriori()                   -run the apriori algorithm
            


##### - The following is the code structure:
    
    run_apriori()(main())---->load_database
                                ---->process the header
                         ---->get measures(min_support, min_confidence)
                         ---->generate rules
                                ---->build first itemset
                                ---->generate frequent itemsets
                                    ---->generate candidate itemset
                                    ---->apply min_support measure
                                ---->create rules which meets min_confidence measure
                                    ---->generate all subsets of frequent itemsets
                                    ---->apply min_confidence measure
                         ---->write rules to file


##### - Run the program
    bluenose: python apriori.py
    python version: python 2.7
    
    The results are saved to file Rules, to view the results
    bluenose: more Rules
    
[Reference](https://github.com/abarmat/python-apriori/blob/master/apriori.py)
