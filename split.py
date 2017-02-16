
def split_data(filename="/Users/sussie/Documents/tcf/ub.test"):
    fp = open(filename, 'rb')
    fileout=open("/Users/sussie/Documents/tcf/test1.txt",'w')
    line=fp.readline()
    l=[]
    while line !='':
        s=','.join(line.split('\t'))
        fileout.write(s)
        line=fp.readline()
    fileout.close()
    fp.close()




