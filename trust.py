"user_based collaborative filtering"
import sys, random, math
from operator import itemgetter
from math import sqrt
sys.path.append("/Users/sussie/Documents/tcf/")
import trust_itemcf



if __name__ == '__main__':

    trainfile = r'/Users/sussie/Documents/tcf/train_1/train1.txt'
    testfile  = r'/Users/sussie/Documents/tcf/train_1/test1.txt'
    ticf = trust_itemcf.ItemBasedCF()
    ticf.load_train_data(trainfile)
    ticf.calculate_ave()
    ticf.load_test_data(testfile)
    ticf.get_direct_matrix()

    ticf.get_trust_matrix()

    semester=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,200]
    for i in range(len(semester)):
        ticf.get_indirect_matrix(semester[i])
        ticf.get_sim_matrix()
        ticf.rmse()


    '''
    ticf.get_trust_matrix()
    ticf.get_indirect_matrix()
    ticf.get_sim_matrix()
    ticf.rmse()
    '''