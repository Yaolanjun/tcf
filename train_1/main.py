"user_based collaborative filtering"
import sys, random, math
from operator import itemgetter
from math import sqrt
sys.path.append("/home/chen/yaoayao/")
import usercf
import improve_cos
import itemcf
import trust_itemcf


if __name__ == '__main__':

    trainfile = r'/home/chen/yaoayao/train_1/train1.txt'
    testfile  = r'/home/chen/yaoayao/train_1/test1.txt'

    ul=[10,20,30,40,50,60,70,80,90,100,200,300]
    il=[20,50,70,100,200,300,400,500,600,700,800,900]
    print "\n\nthe user cf bagin :\n"
    ucf = usercf.UserBasedCF()
    ucf.load_train_data(trainfile)
    ucf.load_test_data(testfile)
    ucf.get_sim_matrix()
    filename=r'/home/chen/yaoayao/train_1/usercf.txt'
    for i1 in ul:ucf.rmse(i1,filename)

    
    print "\n\nthe item cf begin:\n"    
    icf = itemcf.ItemBasedCF()
    icf.load_train_data(trainfile)
    icf.load_test_data(testfile)
    icf.get_sim_matrix()
    filename=r'/home/chen/yaoayao/train_1/itemcf.txt'
    for i2 in il:icf.rmse(i2,filename)


    print "\n\nimprove cos begin:\n"
    picf = improve_cos.ItemBasedCF()
    picf.load_train_data(trainfile)
    picf.calculate_ave()
    picf.load_test_data(testfile)
    picf.get_sim_matrix()
    filename=r'/home/chen/yaoayao/train_1/improve_cos.txt'
    for i3 in il:picf.rmse(i3,filename)

    print "\n\nthe trust begin:\n"
    ticf = trust_itemcf.ItemBasedCF()
    ticf.load_train_data(trainfile)
    ticf.calculate_ave()
    ticf.load_test_data(testfile)
    ticf.get_direct_matrix()
    ticf.get_trust_matrix()
    ticf.get_indirect_matrix()
    ticf.get_sim_matrix()
    filename=r'/home/chen/yaoayao/train_1/trust_itemcf.txt'
    for i4 in il:ticf.rmse(i4,filename)




