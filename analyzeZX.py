import ROOT
from ROOT import TLorentzVector
import math
import numpy as np



def setCavasAndStyles(canvasName, c, stat):
    #setup canvas
    c = ROOT.TCanvas(canvasName,"myPlots",0,0,800,600)
    c.cd(1)
    c.SetLogy(0)
    ROOT.gStyle.SetOptStat(stat)
    ROOT.gStyle.SetPalette(1)



def setHistProperties(hist, lineWidth, lineStyle, lineColor, fillStyle, fillColor, xAxisTitle, yAxisTitle):
    if not(hist):
        return -1
    hist.SetLineWidth(lineWidth)
    hist.SetLineStyle(lineStyle)
    hist.SetLineColor(lineColor)
    # fill
    hist.SetFillStyle(fillStyle)
    hist.SetFillColor(fillColor)
    # divisions, offsets, sizes
    hist.GetXaxis().SetNdivisions(510)
    hist.GetYaxis().SetNdivisions(510)
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.GetYaxis().SetTitleSize(0.05)
    hist.GetXaxis().SetTitleOffset(1.2)
    hist.GetYaxis().SetTitleOffset(1.2)
    # titles
    if (xAxisTitle!="skip"):
        hist.GetXaxis().SetTitle(xAxisTitle)
    if (yAxisTitle!="skip"):
        hist.GetYaxis().SetTitle(yAxisTitle)
    # return
    return 0


def setNEvents(processFileName):
    lNevents = 1
    if (processFileName=="Data"):
        lNEvents = 1
    if (processFileName=="DY10"):
        lNEvents = 37951928.0
    if (processFileName=="DY50"): 
        lNEvents = 99795992.0
    if (processFileName=="TT"): 
        lNEvents = 63667448.0
    if (processFileName=="WZ"):
        lNEvents = 6739437.0
    if (processFileName=="ZZ"):
        lNEvents = 97457264.0
    return lNEvents




def analyzeZX(fTemplateTree, Nickname, varName = "ptl3"):
    print ("--- Initiating the analyzeZX procedure for file nicknamed as: "+ Nickname +".")

    LUMI_INT = 59700
    lineWidth = 2
    leg_xl = 0.50
    leg_xr = 0.90
    leg_yb = 0.72 
    leg_yt = 0.90
    

    varAxLabel = ""
    
    var_plotHigh = 120
    var_plotLow = 60
    var_nBins = 20
    varAxLabel = "m_{Z1}"
    
    if (varName=="mEt"):
        var_plotHigh = 50
        var_plotLow = 0
        var_nBins = 10
        varAxLabel = "E_{T,miss}"
    

    PtlBins = [5.,10.,20.,30.,40.,50.,80.]
    PtlBins = np.array(PtlBins)
    PtlBinsMu = [5.,7.,10.,20.,30.,40.,50.,80.]
    PtlBinsMu = np.array(PtlBinsMu)
    
    #initiate numerator and denominator histograms for FR computation

    binWidth = ((int) (100*(var_plotHigh - var_plotLow)/var_nBins))/100.
    sUnit = "GeV"    
    
    
    if (varName=="ptl3"):
        h1D_dummy = ROOT.TH1D("dummy", "dummy",6, PtlBins)
        setHistProperties(h1D_dummy,1,1,1,0,0,varAxLabel,"Misidentification rate")
        #define FR numerator histograms

        h1D_FRel_EB   = ROOT.TH1D("h1D_FRel_EB","h1D_FRel_EB",6, PtlBins) 
        h1D_FRel_EB.Sumw2()
        h1D_FRel_EE   = ROOT.TH1D("h1D_FRel_EE","h1D_FRel_EE",6, PtlBins) 
        h1D_FRel_EE.Sumw2()
        
        h1D_FRmu_EB   = ROOT.TH1D("h1D_FRmu_EB","h1D_FRmu_EB",7, PtlBinsMu) 
        h1D_FRmu_EB.Sumw2()
        h1D_FRmu_EE   = ROOT.TH1D("h1D_FRmu_EE","h1D_FRmu_EE",7, PtlBinsMu) 
        h1D_FRmu_EE.Sumw2()
        
        # define FR denominator histograms
        h1D_FRel_EB_d   = ROOT.TH1D("h1D_FRel_EB_d","h1D_FRel_EB_d",6, PtlBins) 
        h1D_FRel_EB_d.Sumw2()
        h1D_FRel_EE_d   = ROOT.TH1D("h1D_FRel_EE_d","h1D_FRel_EE_d",6, PtlBins) 
        h1D_FRel_EE_d.Sumw2()
        
        h1D_FRmu_EB_d   = ROOT.TH1D("h1D_FRmu_EB_d","h1D_FRmu_EB_d",7, PtlBinsMu) 
        h1D_FRmu_EB_d.Sumw2()
        h1D_FRmu_EE_d   = ROOT.TH1D("h1D_FRmu_EE_d","h1D_FRmu_EE_d",7, PtlBinsMu) 
        h1D_FRmu_EE_d.Sumw2()    
    else:

        h1D_dummy = ROOT.TH1D("dummy", "dummy", var_nBins, var_plotLow, var_plotHigh)
        setHistProperties(h1D_dummy,1,1,1,0,0,varAxLabel,"Misidentification rate")

        # define FR numerator histograms
        h1D_FRel_EB   = ROOT.TH1D("h1D_FRel_EB","h1D_FRel_EB",var_nBins, var_plotLow, var_plotHigh)
        h1D_FRel_EB.Sumw2()
        h1D_FRel_EE   = ROOT.TH1D("h1D_FRel_EE","h1D_FRel_EE",var_nBins, var_plotLow, var_plotHigh)
        h1D_FRel_EE.Sumw2()
        h1D_FRmu_EB   = ROOT.TH1D("h1D_FRmu_EB","h1D_FRmu_EB",var_nBins, var_plotLow, var_plotHigh) 
        h1D_FRmu_EB.Sumw2()
        h1D_FRmu_EE   = ROOT.TH1D("h1D_FRmu_EE","h1D_FRmu_EE",var_nBins, var_plotLow, var_plotHigh) 
        h1D_FRmu_EE.Sumw2()
    
        # define FR denominator histograms
        h1D_FRel_EB_d   = ROOT.TH1D("h1D_FRel_EB_d","h1D_FRel_EB_d",var_nBins, var_plotLow, var_plotHigh) 
        h1D_FRel_EB_d.Sumw2()
        h1D_FRel_EE_d   = ROOT.TH1D("h1D_FRel_EE_d","h1D_FRel_EE_d",var_nBins, var_plotLow, var_plotHigh) 
        h1D_FRel_EE_d.Sumw2()
        h1D_FRmu_EB_d   = ROOT.TH1D("h1D_FRmu_EB_d","h1D_FRmu_EB_d",var_nBins, var_plotLow, var_plotHigh) 
        h1D_FRmu_EB_d.Sumw2()
        h1D_FRmu_EE_d   = ROOT.TH1D("h1D_FRmu_EE_d","h1D_FRmu_EE_d",var_nBins, var_plotLow, var_plotHigh) 
        h1D_FRmu_EE_d.Sumw2()


    CR_var_plotHigh = 870.0
    CR_var_plotLow = 70.0
    CR_var_nBins = 40    

   # define CR histograms
    h1D_m4l_2P2F = ROOT.TH1D("h1D_m4l_2P2F","h1D_m4l_2P2F",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_2P2F.Sumw2()
    h1D_m4l_3P1F = ROOT.TH1D("h1D_m4l_3P1F","h1D_m4l_3P1F",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_3P1F.Sumw2()
    h1D_m4l_4P   = ROOT.TH1D("h1D_m4l_4P","h1D_m4l_4P",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_4P.Sumw2()
    
    # define CR histograms
    h1D_m4l_2P2F_2e2mu = ROOT.TH1D("h1D_m4l_2P2F_2e2mu","h1D_m4l_2P2F_2e2mu",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_2P2F_2e2mu.Sumw2()
    h1D_m4l_3P1F_2e2mu = ROOT.TH1D("h1D_m4l_3P1F_2e2mu","h1D_m4l_3P1F_2e2mu",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_3P1F_2e2mu.Sumw2()
    h1D_m4l_4P_2e2mu   = ROOT.TH1D("h1D_m4l_4P_2e2mu","h1D_m4l_4P_2e2mu",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_4P_2e2mu.Sumw2()
    
    # define CR histograms
    h1D_m4l_2P2F_2mu2e = ROOT.TH1D("h1D_m4l_2P2F_2mu2e","h1D_m4l_2P2F_2mu2e",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_2P2F_2mu2e.Sumw2()
    h1D_m4l_3P1F_2mu2e = ROOT.TH1D("h1D_m4l_3P1F_2mu2e","h1D_m4l_3P1F_2mu2e",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_3P1F_2mu2e.Sumw2()
    h1D_m4l_4P_2mu2e   = ROOT.TH1D("h1D_m4l_4P_2mu2e","h1D_m4l_4P_2mu2e",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_4P_2mu2e.Sumw2()
    
    # define CR histograms
    h1D_m4l_2P2F_4e = ROOT.TH1D("h1D_m4l_2P2F_4e","h1D_m4l_2P2F_4e",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_2P2F_4e.Sumw2()
    h1D_m4l_3P1F_4e = ROOT.TH1D("h1D_m4l_3P1F_4e","h1D_m4l_3P1F_4e",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_3P1F_4e.Sumw2()
    h1D_m4l_4P_4e   = ROOT.TH1D("h1D_m4l_4P_4e","h1D_m4l_4P_4e",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_4P_4e.Sumw2()
    
    # define CR histograms
    h1D_m4l_2P2F_4mu = ROOT.TH1D("h1D_m4l_2P2F_4mu","h1D_m4l_2P2F_4mu",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_2P2F_4mu.Sumw2()
    h1D_m4l_3P1F_4mu = ROOT.TH1D("h1D_m4l_3P1F_4mu","h1D_m4l_3P1F_4mu",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_3P1F_4mu.Sumw2()
    h1D_m4l_4P_4mu   = ROOT.TH1D("h1D_m4l_4P_4mu","h1D_m4l_4P_4mu",CR_var_nBins, CR_var_plotLow, CR_var_plotHigh) 
    h1D_m4l_4P_4mu.Sumw2()




    isData = ("Data" in Nickname)
    iEvt = -1
    nentries = fTemplateTree.GetEntries()
    lNEvents = setNEvents(Nickname)

    for event in fTemplateTree:
        iEvt+=1
        if(iEvt%50000==0):
            print ("---- Processing event: " + str(iEvt) + "/" + str(nentries))     
        # weight
        weight = event.eventWeight

        if (isData):
            weight = 1
 
        if not(isData):
            if (Nickname=="DY10"):
                weight *= 18610.0*LUMI_INT/lNEvents
                        
            if (Nickname=="DY50"):
                weight *= 6225.4*LUMI_INT/lNEvents

            if (Nickname=="TT"):
                weight *= 87.31*LUMI_INT/lNEvents

            if (Nickname=="WZ"):
                weight *= 4.67*LUMI_INT/lNEvents

            if (Nickname=="ZZ"):
                weight *= 1.256*LUMI_INT*event.k_qqZZ_qcd_M*event.k_qqZZ_ewk/lNEvents


        if (event.passedZ1LSelection):

            lep_tight = event.lep_tightId[event.lep_Hindex[2]]
            lep_iso = event.lep_RelIsoNoFSR[event.lep_Hindex[2]]
            idL3 = event.lep_id[event.lep_Hindex[2]]
            lep = ROOT.TLorentzVector()
            lep.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[2]],event.lep_eta[event.lep_Hindex[2]],event.lep_phi[event.lep_Hindex[2]],event.lep_mass[event.lep_Hindex[2]])
            pTL3  = lep.Pt()
            etaL3 = lep.Eta()
            phiL3 = lep.Phi()
            
            
            lep_1 = ROOT.TLorentzVector()
            lep_2 = ROOT.TLorentzVector()
            lep_1.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[0]],event.lep_eta[event.lep_Hindex[0]],event.lep_phi[event.lep_Hindex[0]],event.lep_mass[event.lep_Hindex[0]])
            lep_2.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[1]],event.lep_eta[event.lep_Hindex[1]],event.lep_phi[event.lep_Hindex[1]],event.lep_mass[event.lep_Hindex[1]])
            
            massZ1 = (lep_1+lep_2).M()


            TestVar=False
            FillVar=0.
            
            if (varName=="mZ1"):
                TestVar= 1
                FillVar= massZ1
            
            if (varName=="mEt"):
                TestVar= 1
                FillVar= event.met
            
            if (varName=="ptl3"):
                TestVar= (math.fabs(massZ1-91.188)<7) and (event.met<25) 
                FillVar= pTL3

            if ((abs(idL3) == 11) and (math.fabs(etaL3) < 1.497) and TestVar):
                h1D_FRel_EB_d.Fill(FillVar, weight)
                #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[EB_d], Hist_fakes[EB_d], Hist_BDfakes[EB_d], Hist_conv[EB_d],false)
                if (lep_tight and TestVar):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[EB_n], Hist_fakes[EB_n],Hist_BDfakes[EB_n],Hist_conv[EB_n],false)
                    h1D_FRel_EB.Fill(FillVar, weight)

            if ((abs(idL3) == 11) and (math.fabs(etaL3) > 1.497) and TestVar):
                h1D_FRel_EE_d.Fill(FillVar, weight)
                #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[EE_d], Hist_fakes[EE_d],Hist_BDfakes[EE_d], Hist_conv[EE_d],false)
                
                if (lep_tight and TestVar):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[EE_n], Hist_fakes[EE_n], Hist_BDfakes[EE_n], Hist_conv[EE_n],false)
                    h1D_FRel_EE.Fill(FillVar, weight)
           
            if ((abs(idL3) == 13) and (math.fabs(etaL3) < 1.2) and TestVar):
                h1D_FRmu_EB_d.Fill(FillVar, weight)
                #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[MB_d], Hist_fakes[MB_d], Hist_BDfakes[MB_d], Hist_conv[MB_d],false)
                
                if (lep_tight and (lep_iso < 0.35) and TestVar):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[MB_n], Hist_fakes[MB_n],Hist_BDfakes[MB_n], Hist_conv[MB_n],false)
                    h1D_FRmu_EB.Fill(FillVar, weight)

            if ((abs(idL3) == 13) and (math.fabs(etaL3) > 1.2) and TestVar):
                h1D_FRmu_EE_d.Fill(FillVar, weight)
                #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[ME_d], Hist_fakes[ME_d],Hist_BDfakes[ME_d], Hist_conv[ME_d],false)
                
                if (lep_tight and (lep_iso<0.35) and TestVar):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, FillVar,weight,Hist_prompt[ME_n], Hist_fakes[ME_n],Hist_BDfakes[ME_n], Hist_conv[ME_n],false)
                    h1D_FRmu_EE.Fill(FillVar, weight)
  

        elif (event.passedZXCRSelection and varName == "ptl3"):

            lep_tight = []
            lep_iso = []
            idL = []
            for k in range(4):
                lep_tight.append(event.lep_tightId[event.lep_Hindex[k]])
                lep_iso.append(event.lep_RelIsoNoFSR[event.lep_Hindex[k]])
                idL.append(event.lep_id[event.lep_Hindex[k]])
        
            


            lep_3 = ROOT.TLorentzVector()
            lep_3.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[2]], event.lep_eta[event.lep_Hindex[2]], event.lep_phi[event.lep_Hindex[2]], event.lep_mass[event.lep_Hindex[2]])
            pTL3  = lep_3.Pt()
            etaL3 = lep_3.Eta()
            phiL3 = lep_3.Phi()

            lep_4 = ROOT.TLorentzVector()
            lep_4.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[3]], event.lep_eta[event.lep_Hindex[3]], event.lep_phi[event.lep_Hindex[3]], event.lep_mass[event.lep_Hindex[3]])
            pTL4  = lep_4.Pt()
            etaL4 = lep_4.Eta()
            phiL4 = lep_4.Phi()
            DR = math.sqrt((phiL3-phiL4)*(phiL3-phiL4) + (etaL3-etaL4)*(etaL3-etaL4))
            
            lep_1 = ROOT.TLorentzVector()
            lep_2 = ROOT.TLorentzVector()

            lep_1.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[0]], event.lep_eta[event.lep_Hindex[0]], event.lep_phi[event.lep_Hindex[0]], event.lep_mass[event.lep_Hindex[0]])
            lep_2.SetPtEtaPhiM(event.lep_pt[event.lep_Hindex[1]], event.lep_eta[event.lep_Hindex[1]], event.lep_phi[event.lep_Hindex[1]], event.lep_mass[event.lep_Hindex[1]])
            
            massZ1 = (lep_1+lep_2).M()
            nFailedLeptons1 = not(lep_tight[0] and ((abs(idL[0])==11) or (abs(idL[0])==13 and lep_iso[0]<0.35)))
            nFailedLeptons2 = not(lep_tight[1] and ((abs(idL[1])==11) or (abs(idL[1])==13 and lep_iso[1]<0.35)))
            nFailedLeptonsZ1 = nFailedLeptons1 + nFailedLeptons2

            nFailedLeptons3 = not(lep_tight[2] and ((abs(idL[2])==11) or (abs(idL[2])==13 and lep_iso[2]<0.35)))
            nFailedLeptons4 = not(lep_tight[3] and ((abs(idL[3])==11) or (abs(idL[3])==13 and lep_iso[3]<0.35)))
            nFailedLeptonsZ2 = nFailedLeptons3 + nFailedLeptons4
            
            nFailedLeptons = nFailedLeptonsZ1 + nFailedLeptonsZ2


            #nFailedLeptonsZ1 = not (lep_tight[0] and ((abs(idL[0])==11) or (abs(idL[0])==13 and lep_iso[0]<0.35))) + not (lep_tight[1] and ((abs(idL[1])==11) or (abs(idL[1])==13 and lep_iso[1]<0.35)))
            #nFailedLeptonsZ2 = not (lep_tight[2] and ((abs(idL[2])==11) or (abs(idL[2])==13 and lep_iso[2]<0.35))) + not (lep_tight[3] and ((abs(idL[3])==11) or (abs(idL[3])==13 and lep_iso[3]<0.35)))          
            #nFailedLeptons = nFailedLeptonsZ1 + nFailedLeptonsZ2



            # fill 1D hists

            if (nFailedLeptons == 0):
                h1D_m4l_4P.Fill(event.mass4l, weight)

                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==44):
                    h1D_m4l_4P_4e.Fill(event.mass4l, weight)
                
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==52):
                    h1D_m4l_4P_4mu.Fill(event.mass4l, weight)
                
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==48):
                    h1D_m4l_4P_2e2mu.Fill(event.mass4l, weight)
                    
            if (nFailedLeptons == 1):
                h1D_m4l_3P1F.Fill(event.mass4l, weight)
                #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_3P1F], CR[Fake][_3P1F],CR[BDfake][_3P1F],CR[Conv][_3P1F],false)
                
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==44):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_3P1F_4e], CR[Fake][_3P1F_4e],CR[BDfake][_3P1F_4e],CR[Conv][_3P1F_4e],false)
                    h1D_m4l_3P1F_4e.Fill(event.mass4l, weight)
            
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==52):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_3P1F_4mu], CR[Fake][_3P1F_4mu], CR[BDfake][_3P1F_4mu],CR[Conv][_3P1F_4mu],false)
                    h1D_m4l_3P1F_4mu.Fill(event.mass4l, weight)

                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==48):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_3P1F_2e2mu], CR[Fake][_3P1F_2e2mu],CR[BDfake][_3P1F_2e2mu],CR[Conv][_3P1F_2e2mu],false)
                    if (abs(idL[2])+abs(idL[3])==22):
                        h1D_m4l_3P1F_2mu2e.Fill(event.mass4l, weight)

                    if (abs(idL[2])+abs(idL[3])==26):
                        h1D_m4l_3P1F_2e2mu.Fill(event.mass4l, weight)
     
            if (nFailedLeptons == 2):
                h1D_m4l_2P2F.Fill(event.mass4l, weight)
                #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_2P2F], CR[Fake][_2P2F], CR[BDfake][_2P2F],CR[Conv][_2P2F],false)
                
                
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==44):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_2P2F_4e], CR[Fake][_2P2F_4e], CR[BDfake][_2P2F_4e],CR[Conv][_2P2F_4e],false)
                    h1D_m4l_2P2F_4e.Fill(event.mass4l, weight)
                
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==52):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_2P2F_4mu], CR[Fake][_2P2F_4mu],CR[BDfake][_2P2F_4mu],CR[Conv][_2P2F_4mu],false)
                    h1D_m4l_2P2F_4mu.Fill(event.mass4l, weight)
                
                if ((abs(idL[0])+abs(idL[1])+abs(idL[2])+abs(idL[3]))==48):
                    #PartOrigin(lep_matchedR03_PdgId, lep_matchedR03_MomId, lep_matchedR03_MomMomId,lep_Hindex,lep_id, mass4l,weight,CR[Prom][_2P2F_2e2mu], CR[Fake][_2P2F_2e2mu],CR[BDfake][_2P2F_2e2mu],CR[Conv][_2P2F_2e2mu],false)
                    
                    if (abs(idL[2])+abs(idL[3])==22):
                        h1D_m4l_2P2F_2mu2e.Fill(event.mass4l, weight)
                    if (abs(idL[2])+abs(idL[3])==26):
                        h1D_m4l_2P2F_2e2mu.Fill(event.mass4l, weight)
                    
                
      


        # Storing the plots
    isData_string = "Data"
    if not (isData):
        isData_string = "MC"

    SaveRootFile = ROOT.TFile("Hist_"+isData_string+"_"+varName+"_"+Nickname+".root", "RECREATE")


    # C++ kod odavde
       
    
    
    h1D_FRel_EE_n = h1D_FRel_EE.Clone()
    h1D_FRmu_EE_n = h1D_FRmu_EE.Clone()
    h1D_FRel_EB_n = h1D_FRel_EB.Clone()
    h1D_FRmu_EB_n = h1D_FRmu_EB.Clone()
    
    
    # divide hists to get the fake rates
    h1D_FRel_EB_n.Divide(h1D_FRel_EB_d)
    h1D_FRel_EE_n.Divide(h1D_FRel_EE_d)
    h1D_FRmu_EB_n.Divide(h1D_FRmu_EB_d)
    h1D_FRmu_EE_n.Divide(h1D_FRmu_EE_d)
    
    h1D_FRel_EB_n.GetYaxis().SetRangeUser(0.01,0.35) 
    h1D_FRel_EE_n.GetYaxis().SetRangeUser(0.01,0.35)
    h1D_FRmu_EB_n.GetYaxis().SetRangeUser(0.04,0.35)
    h1D_FRmu_EE_n.GetYaxis().SetRangeUser(0.04,0.35)
    #Save histograms in .root file
    
    
    h1D_FRel_EB.SetName("Data_FRel_EB_n")
    h1D_FRel_EB.Write()
    h1D_FRel_EE.SetName("Data_FRel_EE_n") 
    h1D_FRel_EE.Write()
    h1D_FRmu_EB.SetName("Data_FRmu_EB_n") 
    h1D_FRmu_EB.Write()
    h1D_FRmu_EE.SetName("Data_FRmu_EE_n") 
    h1D_FRmu_EE.Write()
    
    h1D_FRel_EB_d.SetName("Data_FRel_EB_d") 
    h1D_FRel_EB_d.Write()
    h1D_FRel_EE_d.SetName("Data_FRel_EE_d") 
    h1D_FRel_EE_d.Write()
    h1D_FRmu_EB_d.SetName("Data_FRmu_EB_d") 
    h1D_FRmu_EB_d.Write()
    h1D_FRmu_EE_d.SetName("Data_FRmu_EE_d") 
    h1D_FRmu_EE_d.Write()
    
    
    h1D_FRel_EB_n.SetName("Data_FRel_EB") 
    h1D_FRel_EB_n.Write()
    h1D_FRel_EE_n.SetName("Data_FRel_EE") 
    h1D_FRel_EE_n.Write()
    h1D_FRmu_EB_n.SetName("Data_FRmu_EB") 
    h1D_FRmu_EB_n.Write()
    h1D_FRmu_EE_n.SetName("Data_FRmu_EE") 
    h1D_FRmu_EE_n.Write()
    
    # store slimmed tree and histograms in .root file
    
    h1D_m4l_2P2F.SetName("h1D_m4l_2P2F") 
    h1D_m4l_2P2F.Write()
    h1D_m4l_2P2F_2e2mu.SetName("h1D_m4l_2P2F_2e2mu") 
    h1D_m4l_2P2F_2e2mu.Write()
    h1D_m4l_2P2F_2mu2e.SetName("h1D_m4l_2P2F_2mu2e") 
    h1D_m4l_2P2F_2mu2e.Write()
    h1D_m4l_2P2F_4e.SetName("h1D_m4l_2P2F_4e") 
    h1D_m4l_2P2F_4e.Write()
    h1D_m4l_2P2F_4mu.SetName("h1D_m4l_2P2F_4mu") 
    h1D_m4l_2P2F_4mu.Write()
    
    h1D_m4l_3P1F.SetName("h1D_m4l_3P1F") 
    h1D_m4l_3P1F.Write()
    h1D_m4l_3P1F_2e2mu.SetName("h1D_m4l_3P1F_2e2mu") 
    h1D_m4l_3P1F_2e2mu.Write()
    h1D_m4l_3P1F_2mu2e.SetName("h1D_m4l_3P1F_2mu2e") 
    h1D_m4l_3P1F_2mu2e.Write()
    h1D_m4l_3P1F_4e.SetName("h1D_m4l_3P1F_4e") 
    h1D_m4l_3P1F_4e.Write()
    h1D_m4l_3P1F_4mu.SetName("h1D_m4l_3P1F_4mu") 
    h1D_m4l_3P1F_4mu.Write()
    
    SaveRootFile.Close()

    