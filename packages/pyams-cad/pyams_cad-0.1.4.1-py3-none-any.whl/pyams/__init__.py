
import sys,os
from PyQt5.QtWidgets import QApplication

dire =os.path.dirname(__file__)
sys.path+=[dire]

from .PyAMS import  *

def win():
        app=QApplication(sys.argv);
        w=PyAMS();
        dire =os.path.dirname(__file__)
        r=dire
        print(dire)
        w.ppDir=r;
        w.path=r;
        w.pathLib=r+'//demo';
        w.show();
        sys.exit(app.exec_());
