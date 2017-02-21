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
        self.item_rating_count={}

        self.direct_matrix={}
        self.indirect_matrix={}
        self.trust_matrix={}
        self.item_ave=0.0

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
        total=0.0
        while line != '':
            total+=1
            line.strip('\r\n')
            user,item,rating,time=line.split(',')
            self.item_rating_count.setdefault(item,0)
            self.item_rating_count[item]=self.item_rating_count[item]+1
            self.trainset.setdefault(user, {})
            self.trainset[user][item] = float(rating)
            trainset_len += 1
            line=fp.readline()

        fp.close()
        self.item_ave=total/len(self.item_rating_count)
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
        if sum1 * sum2 == 0.0: return 1.0
        return sum_of_item/float(sum1*sum2)


    '''get the trust of the two item'''
    def trust(self,item,other,lambd=0.5):
        count=0.0
        total=0.0
        for user in self.trans_prefs[item]:
            if user in self.trans_prefs[other]:
                total=total+1

                a=abs(self.trans_prefs[item][user]-self.trans_prefs[other][user])
                if a<=lambd:
                    count=count+1-a/lambd

        if total==0.0:
            return 0.0
        if(self.item_rating_count[other]>=0.5*self.item_ave):
            return count*total/self.item_rating_count[item]

        return count*total*self.item_rating_count[other]\
               /(self.item_rating_count[item]*0.5*self.item_ave)


    def get_trust_matrix(self):
        result={}

        for item in self.trans_prefs:
            result.setdefault(item,{})
            for other in self.trans_prefs:
                if item==other:continue

                result[item][other]=self.trust(item,other)

            self.trust_matrix[item]=sorted(result[item].iteritems(),\
                                           key=lambda b:b[1],reverse=True)
        print "finish get the matrix of trust"


    '''get the simlarity matrix of item'''
    def get_direct_matrix(self):
        self.transform()

        for item in self.trans_prefs:
            self.direct_matrix.setdefault(item, {})
            for other in self.trans_prefs:
                if other==item:continue
                self.direct_matrix[item][other]=self.cos_sim(item,other)

            #sort the similarity

        print "have finished calculate the similarity matrix"


    def get_indirect_sim(self,item,other,count=300):
        total_sim = 0.0
        total_trust = 0.0
        for i in range(count):
            it = self.trust_matrix[item][i][0]
            if other not in self.direct_matrix[it]:continue
            total_sim+=self.direct_matrix[it][other]*self.trust_matrix[item][i][1]
            total_trust+=self.trust_matrix[item][i][1]

        if total_trust == 0.0: return 0.0
        return total_sim/total_trust



    def get_indirect_matrix(self):

        for item in self.trans_prefs:
            if self.item_rating_count[item] >= 0.5*self.item_ave: continue
            self.indirect_matrix.setdefault(item,{})
            for other in self.trans_prefs:
                if other == item:continue
                sim = self.get_indirect_sim(item,other)
                if sim != 0.0: self.indirect_matrix[item][other] = sim


    def get_sim_matrix(self,alpha = 0.5):
        result={}
        for item in self.trans_prefs:
            result.setdefault(item, {})
            if self.item_rating_count[item]>0.5*self.item_ave:
                result[item] = self.direct_matrix[item]
            else:
                for other in self.trans_prefs:
                    if other == item:continue
                    if other in self.direct_matrix[item]:
                        direct_sim = self.direct_matrix[item][other]
                    else:
                        direct_sim = 0.0

                    if other in self.indirect_matrix[item]:
                        indirect_sim = self.indirect_matrix[item][other]
                    else:
                        indirect_sim = 0.0

                    sim = alpha*direct_sim+(1-alpha)*indirect_sim
                    if sim != 0:
                        result[item][other] = sim

            self.sim_mat[item]=sorted(result[item].iteritems(),\
                                      key=lambda b:b[1],reverse=True)
        print "get the sim matrix"



    '''predict the ratings'''
    def predict_rating(self,user,item):
        r=0.0
        totalsim=0.0

        for i in range(self.n_sim_movie):
            other=self.sim_mat[item][i][0]
            if other in self.trainset[user].keys():
                r=r+self.trainset[user][other]*self.sim_mat[item][i][1]

                totalsim=totalsim+self.sim_mat[item][i][1]

        '''cannot predict the rating if totalsim equals 0.0, return 0.0 '''
        if totalsim==0.0: return 0.0

        return r/totalsim



    '''evaluate the performance with the RMSE'''
    def rmse(self):
        n=0.0
        sum_r=0.0
        total=0.0

        for user in self.testset.keys():
            if user not in self.trainset: continue
            for item in self.testset[user].keys():
                total=total+1

                if item not in self.sim_mat.keys():
                    continue
                rating=self.predict_rating(user,item)

                if rating!=0.0:
                    n=n+1
                    #sum_r=sum_r+abs(self.testset[user][item]-rating)
                    sum_r=sum_r+pow(self.testset[user][item]-rating,2)
        print "the coverage is ",n/total
        #print "the mse is %f"%(sum_r/n)
        print "the rmse is %f"% sqrt(sum_r/float(n))



if __name__ == '__main__':
    trainfile = r'test1/train_rating.txt'
    testfile  = r'test1/train_rating.txt'
    itemcf = ItemBasedCF()
    itemcf.load_train_data(trainfile)
    itemcf.calculate_ave()
    itemcf.load_test_data(testfile)
    itemcf.get_sim_matrix()
    itemcf.rmse()