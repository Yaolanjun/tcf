"user_based collaborative filtering"
import sys, random, math
from operator import itemgetter
from math import sqrt
sys.path.append("/home/chen/yaoayao/tcf/")
import improve_cos



if __name__ == '__main__':

    trainfile = r'/home/chen/yaoayao/tcf/train_1/train1.txt'
    testfile  = r'/home/chen/yaoayao/tcf/train_1/test1.txt'
    icf = improve_cos.ItemBasedCF()
    icf.load_train_data(trainfile)
    icf.calculate_ave()
    icf.load_test_data(testfile)
    icf.get_sim_matrix()
    icf.rmse()


