
import random
def split_data(filename="/Users/sussie/Documents/tcf/ratings.csv"):
    fp = open(filename, 'rb')
    train_out=open("/Users/sussie/Documents/tcf/train.txt",'w')
    test_out=open("/Users/sussie/Documents/tcf/test.txt", 'w')
    line=fp.readline()
    line = fp.readline()
    #l=[]
    while line !='':
        #s=','.join(line.split('::'))

        #l.append(line)
        n=random.randint(1,10)
        if n<=8:
            train_out.write(line)
        else:
            test_out.write(line)
        line=fp.readline()
    fp.close()
    train_out.close()
    test_out.close()

if __name__ == '__main__':
    split_data()




