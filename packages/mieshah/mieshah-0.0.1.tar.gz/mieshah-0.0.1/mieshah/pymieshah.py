from sympy import symbols, sympify
import numpy as np
from dimpy import *

class miescatter:
    def __init__(self, **kwargs):
        self.x = symbols('x')
        self.ps = kwargs.get('ps', None)
        self.wl = kwargs.get('wl', None)
        self.m = kwargs.get('m', None)
        self.incr = kwargs.get('incr', None)
        self.I_perp=[]
        self.I_parl=[]
        self.theta=[]
        self.p_theta=[]
        self.Polar=[]        
 

        if self.ps==None or self.wl==None or type(self.m)!=tuple:
            print("Invalid input\nPlease enter a valid ps, wl, and m (e.g. ps=0.1 or ps=[0.01:0.1], wl=0.365, m=(1.403,0.024))")
            print("Exiting...")
            exit()
            

        # Convert f string to a SymPy expression
        f_expr = kwargs.get('f', None)
        if f_expr is not None:
            self.f = sympify(f_expr)
        else:
            self.f = None

        if type(self.ps) == list and self.f is not None:
            if len(self.ps) != 2:
                print("Invalid input\nPlease enter a valid ps (e.g. ps=[0.01:0.1] or ps=[0.1,0.01])")
                print("Exiting...")
                exit()
            self.ps_min = min(self.ps)
            self.ps_max = max(self.ps)
            if self.incr is None:
                self.incr = (self.ps_max - self.ps_min) / 100
                print("'incr' is set to default value:", self.incr)
        elif type(self.ps) ==float and self.f is not None:
            print("ps and f are not compatible\nAs single particle is entered no frequency distribution is allowed.\nExiting...")
            self.f = None
            exit()
        elif type(self.ps) ==int and self.f is not None:
            print("ps and f are not compatible\nAs single particle is entered no frequency distribution is allowed.\nExiting...")
            self.f = None
            exit()
        elif type(self.ps) ==list and self.f is None:
            print("ps and f are not compatible\nAs a range of particle size is entered a frquency distribution function must be given (e.g. f='x**-1.5')\nExiting...")
            self.f = None
            exit()
        if self.f is not None:
            print("Please wait...")
        self.miecalc()

    def miecalc(self):
        P,Q,R,C,S,AR,AI,BR,BI=dim(21001),dim(21001),dim(21001),dim(21001),dim(21001),dim(21001),dim(21001),dim(21001),dim(21001)
        #f1 = open(os.path.join(script_dir, "mie1.out"), "w")
        #f2 = open(os.path.join(script_dir, "mie2.out"), "w")
        f1 = open("mie1.out", "w")
        f2 = open("mie2.csv", "w")

        NMAX=21001
    #    a = self.ps
        AMU1=self.m[0]
        AMU2=self.m[1]
        WL=self.wl
        DK=self.incr

        def mie_theta(ITH,a_range):
            SSS1=0.0
            SSS2=0.0
            tot_freq=0.0
            Phase_func_list=[]
            QBAK_ = []
            QEXT_ = []
            QSCA_ = []
            QABS_ = []
            ALBED_ = []
            ASYM_ = []
            QPR_ = []
            RHO_ = []
            SCA_ = []
            X_=[]
            if type(a_range)==list and self.f is not None:
                a_=np.arange(a_range[0],a_range[1]+DK,DK)
            elif type(a_range)==float or type(a_range)==int:
                a_=[a_range]
            for a in a_:
                if len(a_)!=1:
                    frequency = self.f.subs({self.x:a})
                else:
                    frequency = 1.0
                X=(6.283185307*a)/WL
                Y1=X*AMU1
                Y2=-X*AMU2
                YY=Y1*Y1+Y2*Y2
                NYY=int(1.01*np.sqrt(YY)+50.0)
                if AMU1 - 1.0 < 0:
                    NYY = NYY + int(X * (1.0 - AMU1))
                else:
                    NX = NYY
                if(NYY-NMAX)<=0:
                    if(NYY-0.10E-09)<=0:
                        N=NYY+int(0.75*X+50.0)
                    else:
                        N=NX+int(0.75*X+50.0)
                else:
                    NX=NMAX
                PJN1=0.0
                QJN1=0.0
                RJN1=0.0
                CX=np.cos(X)
                SX=np.sin(X)

                C[0]=(CX/X)+SX
                CQ=CX/C[0]
                JN=N+1
                while True:  # Label 35
                    JN=JN-1
                    XN=2*JN+1
                    PR=(XN*Y1/YY)-PJN1
                    PI=(XN*Y2/YY)+QJN1
                    PP=PR*PR+PI*PI
                    RJN=X/(XN-X*RJN1)
                    PJN=PR/PP
                    QJN=PI/PP
                    #print(PJN,QJN,RJN)
                    if (JN - NMAX) <= 0:
                        P[JN-1] = PJN
                        Q[JN-1] = QJN
                        R[JN-1] = RJN
                        PJN1 = PJN
                        QJN1 = QJN
                        RJN1 = RJN
                    else:
                        PJN1 = PJN
                        QJN1 = QJN
                        RJN1 = RJN
                    if (JN - 1) <= 0:
                        break
                TXE=0.0
                SCA=0.0
                ASQ=0.0
                for NS in range(1, NMAX+1): # do 10 NS=1,NX
                    CN=NS
                    if (NS-1) <= 0:
                        S[0]=(SX/X)-CX
                        DCX=CX-C[1]/X
                    else:
                        S[NS-1]=R[NS-1]*S[NS-2]
                        XN=2*NS-1
                        QC=X/(XN-X*CQ)
                        C[NS-1]=C[NS-2]/QC
                        DCX=C[NS-2]-CN*(C[NS-1]/X)
                        CQ=QC
                    PQ=(P[NS-1]**2)+(Q[NS-1]**2)
                    #print(P[NS-1],Q[NS-1])
                    ZR1=(P[NS-1]/PQ)-CN*(Y1/YY)
                    ZI1=CN*(Y2/YY)-Q[NS-1]/PQ
                    X1=(1.0/R[NS-1])-CN/X
                    ZR2=1.0
                    ZI2=C[NS-1]/S[NS-1]
                    ZR3=X1
                    ZI3=DCX/S[NS-1]
                    ANR=ZR1-X1*AMU1
                    ANI=ZI1+X1*AMU2
                    ADR=ZR1-ZI1*ZI2-AMU1*X1-AMU2*ZI3
                    ADI=ZR1*ZI2+ZI1-AMU1*ZI3+AMU2*X1
                    BNR=AMU1*ZR1+AMU2*ZI1-X1
                    BNI=AMU1*ZI1-AMU2*ZR1
                    XR=ZR1-ZI1*ZI2
                    XI=ZR1*ZI2+ZI1
                    BDR=AMU1*XR+AMU2*XI-ZR3
                    BDI=AMU1*XI-AMU2*XR-ZI3
                    AA=(ADR**2)+(ADI**2)
                    ARNS=(ANR*ADR+ANI*ADI)/AA
                    AINS=(ANI*ADR-ANR*ADI)/AA
                    BB=(BDR**2)+(BDI**2)
                    BRNS=(BNR*BDR+BNI*BDI)/BB
                    BINS=(BNI*BDR-BNR*BDI)/BB
                    AR[NS-1]=ARNS
                    AI[NS-1]=AINS
                    BR[NS-1]=BRNS
                    BI[NS-1]=BINS
                    RN=CN+0.5
                    TXE=TXE+RN*(ARNS+BRNS)
                    SCA=SCA+RN*(ARNS**2+AINS**2+BRNS**2+BINS**2)
                    TEST=RN*(ARNS+BRNS)/TXE
                    TEST=TEST**2
                    if (NS-1)<=0:
                        VAPISR=1.5*(BR[0]-AR[0])
                        VAPISI=1.5*(BI[0]-AI[0])
                    else:
                        FNPV=CN-1.0
                        FNA=FNPV*(CN+1.0)/CN
                        FNB=(FNPV+CN)/(FNPV*CN)
                        ASQ=ASQ+(AR[NS-2]*AR[NS-1]+AI[NS-2]*AI[NS-1])*FNA
                        ASQ=ASQ+(BR[NS-2]*BR[NS-1]+BI[NS-2]*BI[NS-1])*FNA
                        ASQ=ASQ+(AR[NS-2]*BR[NS-2]+AI[NS-2]*BI[NS-2])*FNB
                        RM=RN*((-1.0)**NS)
                        VAPISR= VAPISR+RM*(AR[NS-1]-BR[NS-1])
                        VAPISI= VAPISI+RM*(AI[NS-1]-BI[NS-1])
                        if (TEST-0.1E-21)<=0:
                            break
                XX=4.0/(X*X)
                QEXT=XX*TXE
                QSCA=XX*SCA
                QABS=QEXT-QSCA
                ALBED=QSCA/QEXT
                RHO=2.0*X*(AMU1-1.0)
                ASQ=XX*ASQ
                ASYM=ASQ/QSCA
                QPR=QEXT-ASQ
                QBAK=XX*((VAPISR**2)+(VAPISI**2))
                NN=CN
                TH=ITH-1
                THETA=TH
                TH=TH*0.01745329
                CTH=np.cos(TH)
                PI=0.0
                PI1=1.0
                S1R=1.5*(AR[0]+CTH*BR[0])
                S1I=1.5*(AI[0]+CTH*BI[0])
                S2R=1.5*(AR[0]*CTH+BR[0])
                S2I=1.5*(AI[0]*CTH+BI[0])
                for M in range(2,NN+1):
                    FN=M
                    FNN=(2.0*FN+1.0)/(FN*(FN+1.0))
                    PI2=(CTH*(2.0*FN-1.0)*PI1-FN*PI)/(FN-1.0)
                    TAU2=FN*CTH*PI2-(FN+1.0)*PI1
                    S1R=S1R+FNN*(AR[M-1]*PI2+BR[M-1]*TAU2)
                    S1I=S1I+FNN*(AI[M-1]*PI2+BI[M-1]*TAU2)
                    S2R=S2R+FNN*(AR[M-1]*TAU2+BR[M-1]*PI2)
                    S2I=S2I+FNN*(AI[M-1]*TAU2+BI[M-1]*PI2)
                    PI=PI1
                    PI1=PI2
                SS1=(S1R**2)+(S1I**2)
                SS2=(S2R**2)+(S2I**2) 
                if len(a_)!=1:
                    if self.f is not None:
                        SSS1=SS1*frequency*DK+SSS1
                        SSS2=SS2*frequency*DK+SSS2
                        Phase_func_list.append(2*(SS1+SS2)/(QSCA*(X**2))*frequency*DK)
                        tot_freq=frequency*DK+tot_freq
                        if THETA==0:
                            X_.append(X*frequency*DK)
                            QABS_.append(QABS*frequency*DK)
                            QSCA_.append(QSCA*frequency*DK)
                            QEXT_.append(QEXT*frequency*DK)
                            QBAK_.append(QBAK*frequency*DK)
                            ALBED_.append(ALBED*frequency*DK)
                            #print(ALBED_,ALBED*frequency*DK)
                            ASYM_.append(ASYM*frequency*DK)
                            QPR_.append(QPR*frequency*DK)
                            RHO_.append(RHO*frequency*DK)
                            SCA_.append(SCA*frequency*DK)
                else:
                    SSS1=SS1
                    SSS2=SS2
                    Phase_func_list.append(2*(SS1+SS2)/(QSCA*(X**2)))
                    tot_freq=1
                    if THETA==0:
                        X_.append(X)
                        QABS_.append(QABS)
                        QSCA_.append(QSCA)
                        QEXT_.append(QEXT)
                        QBAK_.append(QBAK)
                        ALBED_.append(ALBED)
                        ASYM_.append(ASYM)
                        QPR_.append(QPR)
                        RHO_.append(RHO)
                        SCA_.append(SCA)
                    
            #print(ALBED_)
            SSS1=SSS1/tot_freq
            SSS2=SSS2/tot_freq
            TSS=SSS1+SSS2
            Phase_func=np.sum(Phase_func_list)/tot_freq
            POLAR=(SSS1-SSS2)/TSS
            if len(a_)!=1 and THETA==0:
                #print(X_,tot_freq)
                X=np.sum(X_)/tot_freq
                QABS=np.sum(QABS_)/tot_freq
                QSCA=np.sum(QSCA_)/tot_freq
                QEXT=np.sum(QEXT_)/tot_freq
                ALBED=np.sum(ALBED_)/tot_freq
                ASYM=np.sum(ASYM_)/tot_freq
                QPR=np.sum(QPR_)/tot_freq
                QBAK=np.sum(QBAK_)/tot_freq
                RHO=np.sum(RHO_)/tot_freq
                SCA=np.sum(SCA_)/tot_freq
        #        return X, QSCA, QEXT, QABS, ALBED, ASYM, QPR, QBAK, NN, THETA, POLAR, SS1, SS2,Pg
                self.X = X
                self.QBAK = QBAK
                self.QEXT = QEXT
                self.QSCA = QSCA
                self.QABS = QABS
                self.ALBED = ALBED
                self.ASYM = ASYM
                self.QPR = QPR
                self.RHO = RHO
                self.SCA = SCA
                self.NN = NN
            else:
                self.X = X
                self.QBAK = QBAK
                self.QEXT = QEXT
                self.QSCA = QSCA
                self.QABS = QABS
                self.ALBED = ALBED
                self.ASYM = ASYM
                self.QPR = QPR
                self.RHO = RHO
                self.SCA = SCA
                self.NN = NN
            self.I_perp.append(SSS1)
            self.I_parl.append(SSS2)
            self.theta.append(THETA)
            self.p_theta.append(Phase_func)
            self.Polar.append(POLAR)
            self.THETA = THETA
            self.POLAR = POLAR
            self.SS1 = SS1
            self.SS2 = SS2
            self.Pg = Phase_func
 
            f2.write(f"{THETA},{SSS1},{SSS2},{POLAR},{Phase_func}\n")  
           
        f2.write(f"theta,I_perp,I_para,Polar,p_theta\n")  
        for ITH in range (1,182,1):
                #self.f = self.f.subs({self.x:self.ps})
                print(f"Calculating for: theta= {ITH-1} deg.", end="\r", flush=True)
                mie_theta(ITH,self.ps)
        print("\nProcess competed.\nPlease see the output files for results")
            #f1.write(f'{self.THETA}\t{self.SS1}\t{self.SS2}\t{self.POLAR}\t{self.Pg}\n')
        f1.write(f"X\tQSCA\tQEXT\tQABS\tALBED\tASYM\tQPR\tQBAK\n")
        f1.write(f"{self.X}\t{self.QSCA}\t{self.QEXT}\t{self.QABS}\t{self.ALBED}\t{self.ASYM}\t{self.QPR}\t{self.QBAK}\n")
        #print('X,QSCA,QEXT,QABS,ALBED,ASYM,QPR,QBAK,NN are')
        #print(X,QSCA,QEXT,QABS,ALBED,ASYM,QPR,QBAK,NN)
        f1.close()
        f2.close()
        


'''# Example usage
from matplotlib import pyplot as plt
mies1 = miescatter(ps=[0.001,0.62], wl=0.365, m=(1.403,0.024), f='x**-2', incr=0.005)
mies2 = miescatter(ps=[0.62,6.2], wl=0.365, m=(1.403,0.024), f='x**-2.75', incr=0.01)
mies3 = miescatter(ps=[6.2,20], wl=0.365, m=(1.403,0.024), f='x**-3.4', incr=0.1)
mies = miescatter(ps=100, wl=6.283185307, m=(1.5,0.0))
#print(mies.ps)               # Output: 7
#print(mies.wl)               # Output: 0.6
#print(mies3.QEXT)           # Output: 0.0
#print(mies.scat_angle)
#print(mies2.scat_angle)           # Output: [0.0, 0.0, 0.0, ...]
pol_av=(np.array(mies1.Polar)+np.array(mies2.Polar)+np.array(mies3.Polar))/3
print(mies3.ALBED)
# Plot at an interval of 2 degrees
#plt.plot(mies3.scat_angle[::2], mies3.p_theta[::2], label='Phase function')
plt.plot(mies3.theta, pol_av, label='Polarization')
#plt.yscale('log')
plt.show()
#print(len(mies.I_para))           # Output: [0.0, 0.0, 0.0, ...]
#print(len(mies2.I_para))  
'''