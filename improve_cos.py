"item_based collaborative filtering"
import sys, random, math
from operator import itemgetter
from math import sqrt


class ItemBasedCF():
    '''  recommendation - ItemBasedCF '''
    def __init__(self):
        self.trainset = {}
        self.testset = {}
        self.trans_prefs={}
        self.user_ave={}

        self.n_sim_movie = 800

        self.sim_mat = {}
        #self.movie_count = 0

        print >> sys.stderr, 'Similar movie number = %d' % self.n_sim_movie


    '''load the trainset'''
    def load_train_data(self,filename):
        fp=open(filename,'rb')
        line=fp.readline()
        #line=fp.readline()
        trainset_len = 0
        while line != '':
            line.strip('\r\n')
            user,item,rating,time=line.split(',')
            self.trainset.setdefault(user, {})
            self.trainset[user][item] = float(rating)
            trainset_len += 1
            line=fp.readline()

        fp.close()
        print >> sys.stderr, 'train set = %s' % trainset_len

    '''calculate the average rating of user'''
    def calculate_ave(self):
        for user in self.trainset:
            sum=0.0
            n=0
            for item in self.trainset[user]:
                sum=sum+self.trainset[user][item]
                n=n+1

            self.user_ave[user]=sum/n

    '''load the testset'''
    def load_test_data(self,filename):
        fp = open(filename, 'rb')
        #line = fp.readline()
        line = fp.readline()
        testset_len = 0
        while line != '':
            line.strip('\r\n')
            user,item,rating,time=line.split(',')
            self.testset.setdefault(user, {})
            self.testset[user][item] = float(rating)
            testset_len += 1
            line=fp.readline()

        fp.close()
        print >> sys.stderr, 'test set = %s' % testset_len

    '''transform the prefs'''

    def transform(self):
        for user in self.trainset:
            for item in self.trainset[user]:
                self.trans_prefs.setdefault(item, {})
                self.trans_prefs[item][user] = self.trainset[user][item]

        print "finish transform the prefs"



    '''calculate the similarity of the two item'''
    def cos_sim(self,item1,item2):
        si={}
        for user in self.trans_prefs[item1]:
            if user in self.trans_prefs[item2]:si[user]=1

        if len(si)==0:return 0.0

        sum1sq=sum([pow(self.trans_prefs[item1][user]-self.user_ave[user],2) for user in si])
        sum2sq=sum([pow(self.trans_prefs[item2][user]-self.user_ave[user],2) for user in si])
        sum1=sqrt(sum1sq)
        sum2=sqrt(sum2sq)

        sum_of_item=sum([(self.trans_prefs[item1][user]-self.user_ave[user])\
                         *(self.trans_prefs[item2][user]-self.user_ave[user])\
                         for user in si])
        if sum1*sum2==0.0:return 1.0
        return sum_of_item/float(sum1*sum2)



    '''get the simlarity matrix of item'''
    def get_sim_matrix(self):
        sim_matrix={}
        self.transform()

        for item in self.trans_prefs:
            sim_matrix.setdefault(item, {})
            for other in self.trans_prefs:
                if other==item:continue
                sim_matrix[item][other]=self.cos_sim(item,other)

            #sort the similarity
            self.sim_mat[item]=sorted(sim_matrix[item].iteritems(),\
                                      key=lambda b:b[1],reverse=True)

        print "have finished calculate the similarity matrix"



    '''predict the ratings'''
    def predict_rating(self,user,item,nn):
        r=0.0
        totalsim=0.0

        self.n_sim_movie=nn

        for i in range(nn):

            if i>=len(self.sim_mat[item]):break

            other=self.sim_mat[item][i][0]
            if other in self.trainset[user].keys():
                r=r+self.trainset[user][other]*self.sim_mat[item][i][1]

                totalsim=totalsim+self.sim_mat[item][i][1]

        '''cannot predict the rating if totalsim equals 0.0, return 0.0 '''
        if totalsim==0.0: return 0.0

        return r/totalsim



    '''evaluate the performance with the RMSE'''
    def rmse(self,nn,filename):
        n=0.0
        sum_r=0.0
        total=0.0

        for user in self.testset.keys():
            if user not in self.trainset: continue
            for item in self.testset[user].keys():
                total=total+1

                if item not in self.sim_mat.keys():
                    continue
                rating=self.predict_rating(user,item,nn)

                if rating!=0.0:
                    n=n+1
                    #sum_r = sum_r + abs(self.testset[user][item] - rating)
                    sum_r = sum_r+pow(self.testset[user][item]-rating,2)
        

        out=open(filename,'a')
        out.write("the number of neighbour is: "+str(self.n_sim_movie))        
        out.write("the coverage is :"+str(n/total))
        out.write("\nthe rmse is: "+str(sqrt(sum_r/float(n))))
        out.write("\n\n\n\n")
        out.close()
        
        print "the coverage is ",n/total
        print "the rmse is %f"% sqrt(sum_r/float(n))
        #print "the mse is %f" % (sum_r / n)



if __name__ == '__main__':
    trainfile = r'test1/train_rating.txt'
    testfile  = r'test1/train_rating.txt'
    itemcf = ItemBasedCF()
    itemcf.load_train_data(trainfile)
    itemcf.calculate_ave()
    itemcf.load_test_data(testfile)
    itemcf.get_sim_matrix()
    itemcf.rmse()
