import math
from scipy.special import erfinv

MC = 0 
DT = 1
Data = 1 
Extra = 2


class CrystallBall:

    def __init__(self):
        self.pi = 3.14159
        self.sqrtPiOver2 = math.sqrt(self.pi/2.0)
        self.sqrt2 = math.sqrt(2.0)
        self.m = 0
        self.s = 1
        self.a = 10
        self.n = 10
        self.fa = math.fabs(self.a)
        self.ex = math.exp(-self.fa * self.fa/2)
        self.A  = pow(self.n/self.fa, self.n) * self.ex
        self.C1 = self.n/self.fa/(self.n-1) * self.ex
        self.D1 = 2 * self.sqrtPiOver2 * math.erf(self.fa/self.sqrt2)
        
        self.B = self.n/self.fa - self.fa
        self.C = (self.D1 + 2 * self.C1)/self.C1
        self.D = (self.D1 + 2 * self.C1)/2
    
        self.N = 1.0/self.s/(self.D1 + 2 * self.C1)
        self.k = 1.0/(self.n - 1)
    
        self.NA = self.N * self.A
        self.Ns = self.N * self.s
        self.NC = self.Ns * self.C1
        self.F = 1 - self.fa * self.fa/self.n
        self.G = self.s * self.n/self.fa
        self.cdfMa = self.cdf(self.m - self.a * self.s)
        self.cdfPa = self.cdf(self.m + self.a * self.s)


    def cdf(self, x):
        d = (x - self.m)/self.s
        if(d < -self.a):
            if(self.F - self.s * d/self.G > 0):
                return self.NC/pow(self.F - self.s * d/self.G, self.n - 1)
            else:
                return self.NC
        if(d > self.a):
            if(self.F + self.s * d/self.G > 0):
                return self.NC * (self.C - pow(self.F + self.s * d/self.G, 1 - self.n))
            else:
                return self.NC * self.C
        return self.Ns * (self.D - self.sqrtPiOver2 * math.erf(-d/self.sqrt2))


    def invcdf(self, u):
        if(u < self.cdfMa):
            if self.NC/u > 0:
                return self.m + self.G * (self.F - pow(self.NC/u, self.k))
            else:
                return self.m + self.G * self.F
        if(u > self.cdfPa):
            if(self.C - u/self.NC > 0):
                return self.m - self.G * (self.F - pow(self.C - u/self.NC, -self.k))
            else:
                return self.m - self.G * self.F
        return self.m - self.sqrt2 * self.s * erfinv((self.D - u/self.Ns)/self.sqrtPiOver2)
    

class ResParams:
    def __init__(self, RTRK):
        self.eta = 0
        self.kRes = [1.0, 1.0]
        self.nTrk = [[1.0 for i in range(RTRK+1)] for j in range(2)]
        self.rsPar = [[1.0 for i in range(RTRK)] for j in range(3)]
        self.cb = [CrystallBall() for i in range(RTRK)]
        

class RocRes:

    def __init__(self, RETA, RTRK, RMIN):
        self.RETA = RETA
        self.RTRK = RTRK
        self.RMIN = RMIN    
        self.resol = [ResParams(RTRK) for i in range(RETA)]

    def RocRes(self, RTRK):
        NETA = 0
        NTRK = 0
        NMIN = 0
        r = ResParams(RTRK)
        r, resol = resol, r

    def etaBin(self, eta):
        for i in range(self.RETA - 1): 
            if (eta < self.resol[i+1].eta):
                return i
        return self.RETA-1

    def trkBin(self, x, h, T):
        for i in range(self.RTRK - 1): 
            if(x < self.resol[h].nTrk[T][i+1]):
                return i
        return self.RTRK-1

    def rndm(self, H, F, w):
        rp = self.resol[H]
        return rp.nTrk[MC][int(F)] + (rp.nTrk[MC][int(F)+1] - rp.nTrk[MC][int(F)]) * w

    def Sigma(self, pt, H, F):
        dpt = pt - 45
        rp = self.resol[H]
        return rp.rsPar[0][int(F)] + rp.rsPar[1][int(F)] * dpt + rp.rsPar[2][int(F)] * dpt*dpt

    def kSpread(self, gpt, rpt, eta, n, w):
        H = self.etaBin(math.fabs(eta))
        if n > self.RMIN:
            F = n - self.RMIN
        else:
            F = 0
        v = self.rndm(H, F, w)
        D = self.trkBin(v, H, Data)
        kold = gpt / rpt
        rp = self.resol[H]
        u = rp.cb[int(F)].cdf((kold - 1.0)/rp.kRes[MC]/self.Sigma(gpt, H, F))
        knew = 1.0 + rp.kRes[Data] * self.Sigma(gpt, H, D) * rp.cb[D].invcdf(u)
        if(knew < 0):
            return 1.0
        return kold/knew

    #def kSpread(self, gpt, rpt, eta):
    #     H = etaBin(fabs(eta))
    #     k = resol[H].kRes
    #     x = gpt/rpt
    #     return x/(1.0 + (x - 1.0) * k[Data]/k[MC])

    def kSmear(self, pt, eta, T, v, u):
        H = etaBin(math.fabs(eta))
        F = trkBin(v, H)
        rp = resol[H]
        x = rp.kRes[T] * Sigma(pt, H, F) * rp.cb[F].invcdf(u)
        return 1.0/(1.0 + x)
        
    def kSmear(self, pt, eta, T, v, u, n):
        H = etaBin(math.fabs(eta))
        F = n - NMIN
        if(T == Data):
            F = trkBin(rndm(H, F, w), H, Data)
        rp = resol[H]
        x = rp.kRes[T] * Sigma(pt, H, F) * rp.cb[F].invcdf(u)
        return 1.0/(1.0 + x)

    def kExtra(self, pt, eta, nlayers, u, w):
        H = etaBin(math.fabs(eta))
        if n > NMIN:
            F = n - NMIN
        else:
            F = 0
        rp = resol[H]
        v = rp.nTrk[MC][F] + (rp.nTrk[MC][F+1] - rp.nTrk[MC][F]) * w
        D = trkBin(v, H, Data)
        RD = rp.kRes[Data] * Sigma(pt, H, D)
        RM = rp.kRes[MC] * Sigma(pt, H, F)
        if RD > RM:
            x = sqrt(RD * RD - RM * RM) * rp.cb[F].invcdf(u)
        else:
            x = 0
        if(x <= -1):
            return 1.0
        return 1.0/(1.0 + x)

    def kExtra(self, pt, eta, nlayers, u):
        H = etaBin(math.fabs(eta))
        if n > NMIN:
            F = n - NMIN
        else:
            F = 0
        rp = resol[H]
        d = rp.kRes[Data]
        m = rp.kRes[MC]
        if d > m:
            x = sqrt(d * d - m * m) * Sigma(pt, H, F) * rp.cb[F].invcdf(u)
        else:
            x = 0
        if(x <= -1):
            return 1.0
        return 1.0/(1.0 + x)

    def getRes(self, s, m):
        return RC[s][m].RR


class CorParams:
    M = 1.0
    A = 1.0


class RocOne:
    def __init__(self, RETA, RTRK, RMIN, NPHI):
        self.RR = RocRes(RETA, RTRK, RMIN)
        self.CP = [[[CorParams() for i in range(16)] for j in range(14)] for k in range(2)]

class RoccoR:

        
    def __init__(self, filename):
        self.MPHI = -3.14159
        self.RMIN = 0
        self.RTRK = 0
        self.RETA = 0
        self.nmem = []
        self.tvar = []
        self.etabin = []
        self.BETA = []
        self.RC = []
        self.pi = 3.14159
        with open(filename) as f:
            for line in f.readlines():
                word = line.split()
                if(word[0] == "NSET"):
                    self.nset = int(word[1])
                elif(word[0] == "NMEM"):
                    for i in range(self.nset):
                        self.nmem.append(int(word[i+1]))
                elif(word[0] == "TVAR"):
                    for i in range(self.nset):
                        self.tvar.append(int(word[i+1]))
                elif(word[0] == "RMIN"):
                    self.RMIN = int(word[1])
                elif(word[0] == "RTRK"):
                    self.RTRK = int(word[1])
                elif(word[0] == "RETA"):
                    self.RETA = int(word[1])
                    for i in range(self.RETA+1):
                        self.BETA.append(float(word[i+2]))
                    for i in range(self.nset):
                        tmp = [RocOne(self.RETA, self.RTRK, self.RMIN, self.NPHI) for j in range(self.nmem[i])]
                        self.RC.append(tmp)
                elif(word[0] == "CPHI"):
                    self.NPHI = int(word[1])
                    self.DPHI = 2*self.pi/self.NPHI
                elif(word[0] == "CETA"):
                    self.NETA = int(word[1])
                    for i in range(self.NETA+1):
                        self.etabin.append(float(word[i+2]))
                else:
                    self.sys = int(word[0])
                    self.mem = int(word[1])
                    self.rc = self.RC[self.sys][self.mem]
                    self.rc.RR.NETA = self.RETA
                    self.rc.RR.NTRK = self.RTRK
                    self.rc.RR.NMIN = self.RMIN
                    self.resol = self.rc.RR.resol
                    for ir in range(len(self.resol)):
                        self.r = self.resol[ir]
                        self.r.eta = self.BETA[ir]
                    self.cp = self.rc.CP
                    if(word[2] == "R"):
                        self.var = int(word[3])
                        self.bin = int(word[4])
                        for i in range(self.RTRK):
                            if (self.var == 0): 
                                self.resol[self.bin].rsPar[self.var][i] = float(word[i+5])
                            elif (self.var == 1): 
                                self.resol[self.bin].rsPar[self.var][i] = float(word[i+5])
                            elif (self.var == 2): 
                                self.resol[self.bin].rsPar[self.var][i] = float(word[i+5])
                                self.resol[self.bin].rsPar[self.var][i] = self.resol[self.bin].rsPar[self.var][i]/100
                            elif (self.var == 3): 
                                self.resol[self.bin].cb[i].s = float(word[i+5])
                            elif (self.var == 4): 
                                self.resol[self.bin].cb[i].a = float(word[i+5])
                            elif (self.var == 5): 
                                self.resol[self.bin].cb[i].n = float(word[i+5])
                    elif(word[2] == "T"):
                        self.t = int(word[3])
                        self.bin = int(word[4])
                        for i in range(self.RTRK+1): 
                            self.resol[self.bin].nTrk[self.t][i] = float(word[i+5])
                    elif(word[2] == "F"): 
                        self.t = int(word[3])
                        for i in range(self.RETA):
                            self.resol[i].kRes[self.t] = float(word[i+4])
                    elif(word[2] == "C"):
                        self.t = int(word[3])
                        self.var = int(word[4])
                        self.bin = int(word[5])
                        for i in range(self.NPHI):
                            self.x = self.cp[self.t][self.bin][i]
                            if(self.var == 0):
                                self.x.M = float(word[i+6])
                                self.x.M = 1.0 + self.x.M/100
                            elif(self.var == 1):
                                self.x.A = float(word[i+6])
                                self.x.A = self.x.A/100
        #for rcs in self.RC:
        #    for rcm in rcs:
        #        for r in rcm.RR.resol:
        #            for i in r.cb: i.RoccoR()

    def etaBin(self, x):
        for i in range(self.NETA-1):
            if(x < self.etabin[i+1]):
                return i
        return self.NETA-1

    def phiBin(self, x):
        ibin = (x - self.MPHI)/self.DPHI
        if(ibin < 0):
            return 0
        if(ibin >= self.NPHI):
            return self.NPHI-1
        return ibin

    def kScaleDT(self, Q, pt, eta, phi, s, m):
        H = etaBin(eta)
        F = phiBin(phi)
        return 1.0/(RC[s][m].CP[DT][H][F].M + Q*RC[s][m].CP[DT][H][F].A*pt)

    def kScaleMC(self, Q, pt, eta, phi, s, m):
        H = etaBin(eta)
        F = phiBin(phi)
        return 1.0/(RC[s][m].CP[MC][H][F].M + Q*RC[s][m].CP[MC][H][F].A*pt)

    def kSpreadMC(self, Q, pt, eta, phi, gt, s, m):
        rc = RC[s][m]
        H = etaBin(eta)
        F = phiBin(phi)
        k = 1.0/(rc.CP[MC][H][F].M + Q*rc.CP[MC][H][F].A*pt)
        return k*rc.RR.kSpread(gt, k*pt, eta)

    def kSmearMC(self, Q, pt, eta, phi, n, u, s, m):
        rc = RC[s][m]
        H = etaBin(eta)
        F = phiBin(phi)
        k = 1.0/(rc.CP[MC][H][F].M + Q*rc.CP[MC][H][F].A*pt)
        return k*rc.RR.kExtra(k*pt, eta, n, u)

    def kScaleFromGenMC(self, Q, pt, eta, phi, n, gt, w, s, m):
        rc = self.RC[s][m]
        H = int(self.etaBin(eta))
        F = int(self.phiBin(phi))
        k = 1.0/(rc.CP[MC][H][F].M + Q*rc.CP[MC][H][F].A*pt)
        return k*rc.RR.kSpread(gt, k*pt, eta, n, w)

    def kScaleAndSmearMC(self, Q, pt, eta, phi, n, u, w, s, m):
        rc = RC[s][m]
        H = etaBin(eta)
        F = phiBin(phi)
        k = 1.0/(rc.CP[MC][H][F].M + Q*rc.CP[MC][H][F].A*pt)
        return k*rc.RR.kExtra(k*pt, eta, n, u, w)

    def kGenSmear(self, pt, eta, v, u, TT, s, m):
        return RC[s][m].RR.kSmear(pt, eta, TT, v, u)

    def kScaleDTerror(self, Q, pt, eta, phi):
        sum = 0
        for s in range(nset):
            for i in range(nmem[s]):
                d = kScaleDT(Q, pt, eta, phi, s, i) - kScaleDT(Q, pt, eta, phi, 0, 0)
                sum += d*d/nmem[s]
        return sqrt(sum)

    def kSpreadMCerror(self, Q, pt, eta, phi, gt):
        sum = 0
        for s in range(nset):
            for i in range(nmem[s]):
                d = kSpreadMC(Q, pt, eta, phi, gt, s, i) - kSpreadMC(Q, pt, eta, phi, gt, 0, 0)
                sum += d*d/nmem[s]
        return sqrt(sum)

    def kSmearMCerror(self, Q, pt, eta, phi, n, u):
        sum = 0
        for s in range(nset):
            for i in range(nmem[s]):
                d = kSmearMC(Q, pt, eta, phi, n, u, s, i) - kSmearMC(Q, pt, eta, phi, n, u, 0, 0)
                sum += d*d/nmem[s]
        return sqrt(sum)

    def kScaleFromGenMCerror(self, Q, pt, eta, phi, n, gt, w):
        sum = 0
        for s in range(nset):
            for i in range(nmem[s]):
                d = kScaleFromGenMC(Q, pt, eta, phi, n, gt, w, s, i) - kScaleFromGenMC(Q, pt, eta, phi, n, gt, w, 0, 0)
                sum += d*d/nmem[s]
        return sqrt(sum)

    def kScaleAndSmearMCerror(self, Q, pt, eta, phi, n, u, w):
        sum = 0
        for s in range(nset):
            for i in range(nmem[s]):
                d = kScaleAndSmearMC(Q, pt, eta, phi, n, u, w, s, i) - kScaleAndSmearMC(Q, pt, eta, phi, n, u, w, 0, 0)
                sum += d*d/nmem[s]
        return sqrt(sum)
    
    def getM(self, T, H, F, s=0, m=0):
        return RC[s][m].CP[T][H][F].M

    def getA(self, T, H, F, s=0, m=0):
        return RC[s][m].CP[T][H][F].A

    def getK(self, T, H, s=0, m=0):
        return RC[s][m].RR.resol[H].kRes[T]
