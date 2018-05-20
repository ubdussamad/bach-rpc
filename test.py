import os
from hashlib import md5
from decorator import *
from hashlib import md5
class test:
    def __init__(self):
        self.file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))),os.path.join('data','asrar.txt'))

        if not os.path.exists(self.file):
            directory = os.path.dirname(self.file)
            if not os.path.exists(directory):
                os.mkdir(directory)
            with open(self.file,'w') as f_obj:
                    f_obj.write('admin,81dc9bdb52d04dc20036dbd8313ed055,1,101\n')

        with open(self.file,'r') as f_obj:
            data = f_obj.read()
            data = [i for i in data.split('\n') if i]
            keys = [i.split(',')[0] for i in data]
            values = [i.split(',')[1:] for i in data]
            self.credentials = dict(zip(keys, values))

    def append(self,data):
        with open(self.file,'a') as f_obj:
            new_user_id = max([int(self.credentials[usr][2]) for usr in self.credentials])
            f_obj.write(','.join([data[0],md5(data[1].encode('utf-8')).hexdigest(),data[2],str(new_user_id+1)]))
            return(0)

@time_wrapper
def test(x) -> int:
    return (x**24699)/256
