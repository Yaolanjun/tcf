"user_based collaborative filtering"
import sys, random, math
from operator import itemgetter
from math import sqrt
sys.path.append("/Users/sussie/Documents/tcf/")
import usercf



if __name__ == '__main__':

    trainfile = r'/Users/sussie/Documents/tcf/train_3/train_1.txt'
    testfile  = r'/Users/sussie/Documents/tcf/train_3/test_1.txt'
    ucf = usercf.UserBasedCF()
    ucf.load_train_data(trainfile)
    ucf.load_test_data(testfile)
    ucf.get_sim_matrix()
    ucf.rmse()


