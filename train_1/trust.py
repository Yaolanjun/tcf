"user_based collaborative filtering"
import sys, random, math
from operator import itemgetter
from math import sqrt
sys.path.append("/home/chen/yaoayao/")

import trust_itemcf




if __name__ == '__main__':

    trainfile = r'/home/chen/yaoayao/train_1/train1.txt'
    testfile  = r'/home/chen/yaoayao/train_1/test1.txt'
    filename = r'/home/chen/yaoayao/train_1/trust_cf.txt'
    ticf = trust_itemcf.ItemBasedCF()
    ticf.load_train_data(trainfile)
    ticf.calculate_ave()
    ticf.load_test_data(testfile)
    ticf.get_direct_matrix()

    l=[0.4,0.5,0.6,0.7,0.8,0.9,1]
    semester=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,200]
    for i in range(len(l)):
        alpha=l[i]
        print "\n\n\nthe alpha is :"+str(alpha)+"\n"
        ticf.get_trust_matrix(alpha)
        out=open(filename,'a')
        out.write("\n\n\n\n"+str(alpha))
        out.close()
        for j in range(len(semester)):
            print "the neighbour is :"+str(semester[j])+"\n"
            ticf.get_indirect_matrix(semester[j])
            ticf.get_sim_matrix()
            ticf.rmse(filename)
