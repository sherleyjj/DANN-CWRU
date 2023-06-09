from torch.utils.data import Dataset,DataLoader
from scipy.signal import stft
import numpy as np
import scipy.io as sio
import torch
import pywt
class CWRUDataset(Dataset):
    def __init__(self,pathlist) -> None:
        super().__init__()
        self.pathdict = pathlist
        self.label = ['B007','B014','B021','IR007','IR014','IR021','OR007','OR014','OR021']
        self.datalist = [self.loadFile(i) for i in self.label]
        self.startrange = np.linspace(0,100000,600,dtype=np.int32) 
        self.len = 256
    def __len__(self):
        return 1000 #调整样本数
    def __getitem__(self, index) :
        i = index % len(self.label)
        slice = index // len(self.label)
        start = self.startrange[slice]
        data = self.datalist[i][start:start+self.len]
        # stftdata = np.abs(stft(data,12000)[2])
        stftdata =  pywt.cwt(data , np.arange(1,257) , 'gaus1')[0]
        stftdata = np.array(stftdata)
        return torch.tensor(stftdata[:self.len,:self.len]) ,torch.tensor(i)
    def loadFile(self,label):
        file = self.pathdict[label]
        key ='X'+ file.split("_")[-1].split(".")[0] +'_DE_time'
        data = sio.loadmat(file)[key].squeeze()
        return np.array(data,dtype=np.float32)