########################################################################################
#ROOT is imported to read the files in the .root data format.
import ROOT

ROOT.gROOT.SetBatch(ROOT.kFALSE)

def check_pair_type( charge_i, charge_j, type_i, type_j, debug = False ):
   pair_type = ""

   if debug:
      print( "type i: {} type j: {}".format(type_i, type_j ) )
      print( "charge i: {} charge j: {}".format(charge_i, charge_j ) )
   
   if type_i != type_j: pair_type += "DF"
   else:                pair_type += "SF"
   
   if charge_i == charge_j : pair_type += "SC"
   else:                     pair_type += "OC"
   
   return pair_type


def isElectron(lep_id):
   return abs(lep_id) == 11

def isMuon(lep_id):
   return abs(lep_id) == 13


def reset_cut_map(cmap):
   cmap["2e2m"] = False 
   cmap["2m2e"] = False
   cmap["4e"]   = False
   cmap["4m"]   = False
   cmap["inc"]  = True
   return cmap


def pass_event_flavour(flavour, cmap):
   if   flavour == "4m":   cmap["4m"]   = True
   elif flavour == "4e":   cmap["4e"]   = True
   elif flavour == "2m2e": cmap["2m2e"] = True
   elif flavour == "2e2m": cmap["2e2m"] = True
   return cmap 


def fill_1d( hist_core_name, value, weight, h_map, cut_map ):

   for cut, decision in cut_map.items():
      if not decision: continue

      h_name =  "{}/{}".format( cut, hist_core_name)
      h_map[h_name].Fill( value, weight )

def fill_2d( hist_core_name, xvalue, yvalue, weight, h_map, cut_map ):

   for cut, decision in cut_map.items():
      if not decision: continue

      h_name =  "{}/{}".format( cut, hist_core_name)
      h_map[h_name].Fill( xvalue, yvalue, weight )


def get_pair_4mom( tree, lep1, lep2 ):
   dilep = ROOT.TLorentzVector()
   
   for ilep in ( lep1, lep2 ):
      lep = ROOT.TLorentzVector()
      lep.SetPtEtaPhiE( tree.lep_pt[ilep], tree.lep_eta[ilep], tree.lep_phi[ilep], tree.lep_E[ilep] )
      dilep += lep

   return dilep

def print_lepton(tree, ilep):
 print( "lep {} type {} charge {} lep pt {} eta {} track iso {} et iso {} d0sig {} z0sintheta {}".format( ilep, tree.lep_type[ilep], tree.lep_charge[ilep], tree.lep_pt[ilep], tree.lep_eta[ilep], (tree.lep_ptcone30[ilep]/tree.lep_pt[ilep]), (tree.lep_etcone20[ilep] / tree.lep_pt[ilep] ),    ( abs(tree.lep_trackd0pvunbiased[ilep])/tree.lep_tracksigd0pvunbiased[ilep]), ( abs(tree.lep_z0[ilep]*ROOT.TMath.Sin( lv.Theta() )) ) ) ) 

def isGoodLepton(tree, ilep):
 if( (tree.lep_pt[ilep] > 5000.) and  
     ( abs( tree.lep_eta[ilep]) < 2.5) and 
     ( (tree.lep_ptcone30[ilep]/tree.lep_pt[ilep]) < 0.3) and
     ( (tree.lep_etcone20[ilep] / tree.lep_pt[ilep]) < 0.3 ) ):
    return True
 else: 
    return False

def isGoodMuon(tree, ilep, lv):
  if( abs(tree.lep_type[ilep] ) == 13  and
    ( abs(tree.lep_trackd0pvunbiased[ilep])/tree.lep_tracksigd0pvunbiased[ilep] < 3) and
    ( abs(tree.lep_z0[ilep]*ROOT.TMath.Sin( lv.Theta() )) < 0.5) ):
          return True
  else: 
     return False

def isGoodElectron(tree, ilep, lv):
  if( abs(tree.lep_type[ilep] ) == 11  and
    ( tree.lep_pt[ilep] > 7000. )      and 
    ( abs( tree.lep_eta[ilep]) < 2.47) and 
    ( abs(tree.lep_trackd0pvunbiased[ilep])/tree.lep_tracksigd0pvunbiased[ilep] < 5) and
    ( abs(tree.lep_z0[ilep]*ROOT.TMath.Sin( lv.Theta() )) < 0.5) 
    ):
        return True
  else: return False


def isGoodJet(tree, ijet):
   if( tree.jet_pt[ijet] > 30000. and abs(tree.jet_eta[ijet]) < 4.4): return True
   else: return False

# Here we open the data that we want to analyse, which is in the form of a .root file. A .root file consists of a tree having branches and leaves.
samples = [
 #  "mc_160155.ggH125_ZZ4lep.root",                                                                                                                                                   
 #  "mc_160205.VBFH125_ZZ4lep.root",                                                                                                                                                  
 #  "mc_341947.ZH125_ZZ4lep.4lep.root",                                                                                                                                               
 #  "mc_341964.WH125_ZZ4lep.4lep.root",                                                                                                                                               
 #  "mc_361106.Zee.4lep.root",                                                                                                                                                        
 #  "mc_361107.Zmumu.4lep.root",                                                                                                                                                      
 #  "mc_363356.ZqqZll.4lep.root",                                                                                                                                                     
 #  "mc_363358.WqqZll.4lep.root",                                                                                                                                                     
 #  "mc_363491.lllv.4lep.root",                                                                                                                                                       
 #  "mc_363492.llvv.4lep.root",                                                                                                                                                       
 #  "mc_410000.ttbar_lep.4lep.root",                                                                                                                                                  
 #  "mc_Others.4lep.root",
 #  "data.4lep.root",
   
#   "mc_410155.ttW.4lep.root",
#   "mc_410218.ttee.4lep.root",
#   "mc_410219.ttmumu.4lep.root",

"mc_345060.ggH125_ZZ4lep.4lep.root",
"mc_341122.ggH125_tautaull.4lep.root",
"mc_341155.VBFH125_tautaull.4lep.root",
"mc_341947.ZH125_ZZ4lep.4lep.root",
"mc_341964.WH125_ZZ4lep.4lep.root",
"mc_344235.VBFH125_ZZ4lep.4lep.root",
"mc_345323.VBFH125_WW2lep.4lep.root",
"mc_345324.ggH125_WW2lep.4lep.root",
"mc_345325.WpH125J_qqWW2lep.4lep.root",
"mc_345327.WpH125J_lvWW2lep.4lep.root",
"mc_345336.ZH125J_qqWW2lep.4lep.root",
"mc_345337.ZH125J_llWW2lep.4lep.root",
"mc_345445.ZH125J_vvWW2lep.4lep.root",

	"mc_363490.llll.4lep.root",
   "mc_363356.ZqqZll.4lep.root",
   "mc_410000.ttbar_lep.4lep.root",
   "mc_363491.lllv.4lep.root",
#
#"mc_364114.Zee_PTV0_70_CVetoBVeto.4lep.root",
#"mc_364115.Zee_PTV0_70_CFilterBVeto.4lep.root",
#"mc_364116.Zee_PTV0_70_BFilter.4lep.root",
#"mc_364117.Zee_PTV70_140_CVetoBVeto.4lep.root",
#"mc_364118.Zee_PTV70_140_CFilterBVeto.4lep.root",
#"mc_364119.Zee_PTV70_140_BFilter.4lep.root",
#"mc_364120.Zee_PTV140_280_CVetoBVeto.4lep.root",
#"mc_364121.Zee_PTV140_280_CFilterBVeto.4lep.root",
#"mc_364122.Zee_PTV140_280_BFilter.4lep.root",
#"mc_364123.Zee_PTV280_500_CVetoBVeto.4lep.root",
#"mc_364124.Zee_PTV280_500_CFilterBVeto.4lep.root",
#"mc_364125.Zee_PTV280_500_BFilter.4lep.root",
#"mc_364126.Zee_PTV500_1000.4lep.root",
#"mc_364127.Zee_PTV1000_E_CMS.4lep.root",
#"mc_364100.Zmumu_PTV0_70_CVetoBVeto.4lep.root",
#"mc_364101.Zmumu_PTV0_70_CFilterBVeto.4lep.root",
#"mc_364102.Zmumu_PTV0_70_BFilter.4lep.root",
#"mc_364103.Zmumu_PTV70_140_CVetoBVeto.4lep.root",
#"mc_364104.Zmumu_PTV70_140_CFilterBVeto.4lep.root",
#"mc_364105.Zmumu_PTV70_140_BFilter.4lep.root",
#"mc_364106.Zmumu_PTV140_280_CVetoBVeto.4lep.root",
#"mc_364107.Zmumu_PTV140_280_CFilterBVeto.4lep.root",
#"mc_364108.Zmumu_PTV140_280_BFilter.4lep.root",
#"mc_364109.Zmumu_PTV280_500_CVetoBVeto.4lep.root",
#"mc_364110.Zmumu_PTV280_500_CFilterBVeto.4lep.root",
#"mc_364111.Zmumu_PTV280_500_BFilter.4lep.root",
#"mc_364112.Zmumu_PTV500_1000.4lep.root",
#"mc_364113.Zmumu_PTV1000_E_CMS.4lep.root",
#"mc_364128.Ztautau_PTV0_70_CVetoBVeto.4lep.root",
#"mc_364129.Ztautau_PTV0_70_CFilterBVeto.4lep.root",
#"mc_364130.Ztautau_PTV0_70_BFilter.4lep.root",
#"mc_364131.Ztautau_PTV70_140_CVetoBVeto.4lep.root",
#"mc_364132.Ztautau_PTV70_140_CFilterBVeto.4lep.root",
#"mc_364133.Ztautau_PTV70_140_BFilter.4lep.root",
#"mc_364134.Ztautau_PTV140_280_CVetoBVeto.4lep.root",
#"mc_364135.Ztautau_PTV140_280_CFilterBVeto.4lep.root",
#"mc_364136.Ztautau_PTV140_280_BFilter.4lep.root",
#"mc_364137.Ztautau_PTV280_500_CVetoBVeto.4lep.root",
#"mc_364138.Ztautau_PTV280_500_CFilterBVeto.4lep.root",
#"mc_364139.Ztautau_PTV280_500_BFilter.4lep.root",
#"mc_364140.Ztautau_PTV500_1000.4lep.root",

"mc_361106.Zee.4lep.root",
"mc_361107.Zmumu.4lep.root",
"mc_361108.Ztautau.4lep.root",

#Data periods
      "data_A.4lep.root",
      "data_B.4lep.root",
      "data_C.4lep.root",
      "data_D.4lep.root"
	      ]


output_dir = "/project/atlas/users/mvozak/ATLASOD/output/"
lumi_data = 10


flavour_channels = [ "4m", "4e", "2e2m", "2m2e", "inc" ]
combination_type = ["SFOC", "DFOC", "SFSC" ]

#def get_event_flavour_channel( lead_pair, second_pair ):

for sample in samples:

   print "Working on sample: ", sample
   folder_name = "MC"
   isMC        = True

   if "data" in sample: 
      folder_name = "Data"
      isMC        = False

   f = ROOT.TFile.Open("/data/atlas/users/mvozak/opendata/4lep/{}/{}".format( folder_name ,sample ) )
   #f = ROOT.TFile.Open("/data/atlas/users/mvozak/opendata/4lep/OldInput/{}".format( sample ) )
   # Define a 'canvas' on which to draw a histogram. Its name is "canvas" and its header is "plot a variable". The two following arguments define the width and the height of the canvas.
   #canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
   #canvas.cd()
   # Here we define a tree named "tree" to extract the data from the input .root file.
   tree = f.Get("mini")
   number_entries = tree.GetEntries()
   print "Number of entries in the tree = ", number_entries
   
   # Define a histogram. Its name is variable and the header of the histogram is "Example plot: Number of leptons". It's x and y axis labels are in the next 2 arguments. The three following arguments indicate that this histogram contains 5 bins which have a range from -0.5 to 4.5.
   #hist    = ROOT.TH1F("variable","Example plot: Number of leptons; Number of leptons; Events ",5,-0.5,4.5)
   #hist = ROOT.TH1F("inv_mass","Inv mass: HZZ->4l; m_{4l}; Events ",250, 50, 550)
   h_map1d = {} 
   cutflow = {} 
   h_map2d = {} 
   
   cutflow["cutflow"]   = ROOT.TH1F("cutflow", "cutflow: cutflow; cuts; Events ", 10, -0.5, 9.5)

   for channel in flavour_channels:

      h_map1d[channel + "/m4l"]   = ROOT.TH1F(channel + "/m4l","Inv mass 4l: Invariant mass of 4l; m_{4l} [GeV]; Events ",250, 50, 550)
      h_map1d[channel + "/m4l_zoom"]   = ROOT.TH1F(channel + "/m4l_zoom","Inv mass 4l: Invariant mass of 4l; m_{4l} [GeV]; Events ",23, 80, 172)
      h_map1d[channel + "/m12"]   = ROOT.TH1F(channel + "/m12","Inv mass 12: Invariant mass of m12; m_{12} [GeV]; Events ",200, 0, 200)
      h_map1d[channel + "/m23"]   = ROOT.TH1F(channel + "/m23","Inv mass 23: Invariant mass of m23; m_{23} [GeV]; Events ",200, 0, 200)
      h_map1d[channel + "/m12_zoom"]   = ROOT.TH1F(channel + "/m12_zoom","Inv mass 12: Invariant mass of m12; m_{12} [GeV]; Events ",28, 50, 106)
      h_map1d[channel + "/m23_zoom"]   = ROOT.TH1F(channel + "/m23_zoom","Inv mass 23: Invariant mass of m23; m_{23} [GeV]; Events ",62, 16, 140)
      h_map1d[channel + "/njets"]  = ROOT.TH1F(channel + "/njets","Number of jets: Number of jets; njets; Events ", 6, -0.5, 5.5)

      h_map2d[channel + "/m12_vs_m23"]   = ROOT.TH2F(channel + "/m12_vs_m23","Inv mass 12 vs mass 23: Invariant mass of m12 vs m23; m_{12} [GeV]; m_{23} ", 100, 0, 200, 75, 0, 150)

      h_map1d[channel + "/jall_pt"] = ROOT.TH1F(channel + "/jall_pt","Transverse momenta of jets: Transverse momenta of jets; p_{T}^{all jets} [GeV]; Events ",150, 0, 150)
      h_map1d[channel + "/jall_jvt"] = ROOT.TH1F(channel + "/jall_jvt","Jvt of jets: Jvt of jets; jvt^{all jets}; Events ",10, 0, 5)

      h_map1d[channel + "/nleptons"]  = ROOT.TH1F(channel + "/nleptons","Number of leptons: Number of leptons; nleptons; Events ", 8, -0.5, 7.5)
      h_map1d[channel + "/met"]  = ROOT.TH1F(channel + "/met", "Transverse missing energy: Transverse missing energy; p_{T}^{miss} [GeV]; Events ", 150, 0, 150)

      for i in ["all", "1", "2", "3", "4", "quad"]:

         h_map1d[channel + "/lep{}_E".format(i)]   = ROOT.TH1F(channel + "/lep{}_E".format(i)," Energy of lepton " + i +": Energy of lepton " + i + "; p_{T} [GeV]; Events ",150, 0, 150)
         h_map1d[channel + "/lep{}_eta".format(i)]  = ROOT.TH1F(channel + "/lep{}_eta".format(i), "Pseudorapidity of lepton "+i+": Pseudorapidity of lepton "+i+"; #eta_{l}; Events ",54, -2.7, 2.7)
         h_map1d[channel + "/lep{}_phi".format(i)]  = ROOT.TH1F(channel + "/lep{}_phi".format(i), "Azimuthal angle of lepton "+i+": Azimuthal angle of lepton "+i+"; #phi_{l}; Events ",20, -1, 1)
         h_map1d[channel + "/lep{}_pt".format(i)]   = ROOT.TH1F(channel + "/lep{}_pt".format(i),"Transverse momenta of lepton "+i+": Transverse momenta of lepton "+i+"; p_{Tl} [GeV]; Events ",150, 0, 150)

         if i != "quad":
            h_map1d[channel + "/lep{}_z0".format(i)]   = ROOT.TH1F(channel + "/lep{}_z0".format(i)," z0 of lepton " + i +": z0 of lepton " + i + "; z_{0} ; Events ",100, -1, 1)
            h_map1d[channel + "/lep{}_d0".format(i)]   = ROOT.TH1F(channel + "/lep{}_d0".format(i)," d0 of lepton " + i +": d0 of lepton " + i + "; d_{0} ; Events ",100, -5, 5)
            h_map1d[channel + "/lep{}_isTight".format(i)]   = ROOT.TH1F(channel + "/lep{}_isTight".format(i)," ID of lepton " + i +": ID of lepton " + i + "; isTight ; Events ", 2, -0.5, 1.5)
            h_map1d[channel + "/lep{}_ptcone30".format(i)]   = ROOT.TH1F(channel + "/lep{}_ptcone30".format(i),"Sum of track momenta in the cone lep "+i+": Sum of track momenta in the cone lep "+i+"; p_{Tl} [GeV]; Events ",50, 0, 10)
            h_map1d[channel + "/lep{}_etcone20".format(i)]   = ROOT.TH1F(channel + "/lep{}_etcone20".format(i),"Sum of calo energy in the cone lep "+i+": Sum of calo energy in the cone lep "+i+"; p_{Tl} [GeV]; Events ",50, 0, 10)

   # Loop over the data (in the tree) and store it in the histogram.
   #       Here you could place any cuts you want to apply, before filling the histogram
   
   cut_map = {}
   it = 0
   for it, event in enumerate(tree):

       finalWeight = 1.
       if isMC:
         mcWeight    = tree.XSection * 1000 * lumi_data * tree.mcWeight * (1./tree.SumWeights)
         scaleFactor = tree.scaleFactor_PILEUP *  tree.scaleFactor_LepTRIGGER * tree.scaleFactor_MUON * tree.scaleFactor_ELE
         finalWeight = mcWeight*scaleFactor

         #print("X-section: {}".format(tree.XSection))
         #print("mcWeight: {}".format(tree.mcWeight))
         #print("SumOfWeights: {}".format(tree.SumWeights))
         #Add pile up reweighting
         #finalWeight *= tree.scaleFactor_PILEUP
         #print( "PU SF", tree.scaleFactor_PILEUP )
         #Adding Trigger scale factors
         #finalWeight *= tree.scaleFactor_LepTRIGGER
         #print( "Lep TRIGGER SF", tree.scaleFactor_LepTRIGGER )
         #Adding lepton scale factors
         #finalWeight *= tree.scaleFactor_MUON
         #finalWeight *= tree.scaleFactor_ELE
         #print("Getting muon SF {}".format(tree.scaleFactor_MUON ))
         #print("Getting ele SF {}".format( tree.scaleFactor_ELE ))
         #print("Final MC weight:".format( finalWeight ))

       #if finalWeight > 10:
       #  print("LARGE WEIGHT")
       #elif finalWeight == 0:
       #  print("ZERO WEIGHT")

       cutflow["cutflow"].Fill( 0, finalWeight )
       #print("Event position : {}".format(it) )
       #if it > 50: break
       #if( (it % 25000) == 0): print("Events processed: ", it)
       if( (it % 10000) == 0): print("Events processed: ", it)

       cut_map = reset_cut_map(cut_map)
       #print(it)
   
       #print("lep pt branch: ", tree.lep_pt)
       #print(len(tree.lep_pt)) 
   

       #Check for the Trigger
       #print( "Trig E: ", tree.trigE, " trigM: ", tree.trigM )
       if not tree.trigE and not tree.trigM: 
          print("NO TRIGGER!")
          continue
       #print("pass trigger")
       cutflow["cutflow"].Fill( 1, finalWeight )
   
       #print(tree.XSection)
       sum_lv = ROOT.TLorentzVector()
   
       nGoodLeptons = 0
       for i in range(len(tree.lep_pt)):
         lv = ROOT.TLorentzVector()
         lv.SetPtEtaPhiE( tree.lep_pt[i], tree.lep_eta[i], tree.lep_phi[i], tree.lep_E[i] )
         sum_lv += lv

         #print_lepton(tree, i)
         isGoodLep = isGoodLepton(tree, i)
         isGoodMu  = isGoodMuon(tree, i, lv)
         isGoodEle = isGoodElectron(tree, i, lv)
         if( isGoodLep and (isGoodMu or isGoodEle)): nGoodLeptons += 1
         else: 
            pass
            #print("Not a good lepton!")

   	
   
       lep_n     = len(tree.lep_pt)
       lep_ids   = [lep for lep in range(0, lep_n)]
       all_pairs = [(a, b) for idx, a in enumerate(lep_ids) for b in lep_ids[idx + 1:]]
       #print("All pairs")
       #print(all_pairs)
   
       #Now categorise each combination based on combination (SFOS, ...)
       labeled_pairs = []
       for pair in all_pairs:
         #print(pair, type(pair)) 
         ilep = pair[0]
         jlep = pair[1]
         #print("i {} j {}".format(ilep, jlep) )
         pair_type = check_pair_type( tree.lep_charge[ilep], tree.lep_charge[jlep], tree.lep_type[ilep], tree.lep_type[jlep] )
         #print(pair_type)

         pair_4mom = get_pair_4mom(tree, ilep, jlep )


         #Now select whichever pairs we want, for now only sfos
         if pair_type != "SFOC": continue

         labeled_pairs.append( [ilep, jlep, pair_type, pair_4mom] )

       #print("Labelled pairs")
       #print(labeled_pairs)
       #two sfos with close to zmass selection

       #Make sure that indices don't repeat in the different pairs      
       
       #sfos_pairs = []

       #FIXME: It can happen that there no 2SFOS (none or only one), for now skip!
       #print("number of pairs",  labeled_pairs)
       if len(labeled_pairs) < 2: continue
       cutflow["cutflow"].Fill( 2, finalWeight )

       #For now kill all cases with more than 4 leptons
       if lep_n > 4: continue
       cutflow["cutflow"].Fill( 3, finalWeight )

       #for ilep in range(0, lep_n):
       #   print("ilep {} type {} charge {}".format( ilep, tree.lep_type[ilep], tree.lep_charge[ilep] ) )
       #print(labeled_pairs)

       mZ        = 91.1876

       #for ip, pair in enumerate(labeled_pairs):
       #   print("ip{} ilep {} jlep {} type {} invmass {} diff {}".format(ip, pair[0], pair[1], pair[2], pair[3].M()*0.001, (abs( abs((pair[3]).M()*0.001) - mZ )) ))
       #Figure out the leading and subleading pairs
       labeled_pairs = sorted(labeled_pairs, key=lambda dilep_pair_info: abs( abs((dilep_pair_info[3]).M()*0.001) - mZ ) ) #, reverse=True )
       #should be sorted by now
       #print(labeled_pairs)
       #for ip, pair in enumerate(labeled_pairs):
       #   print("ip{} ilep {} jlep {} type {} invmass {}".format(ip, pair[0], pair[1], pair[2], pair[3].M()*0.001 ))
       #Check if additional pairs contain the same leptons if so kill the event!
       isValidSecondPair = False

       lead_pair   = 0
       if labeled_pairs > 1:

            #Put in only pairs that do not contain the same leptons!
            for ipair in range(1, len(labeled_pairs) ):
               isValidPair = True
               for ilep in [ (labeled_pairs[ipair][0]), (labeled_pairs[ipair][1] ) ]:

                  #Check against lead pair (in practice if more leptons should check recursively against all previously formed pairs)
                  isValidPair = isValidPair and ( ilep != labeled_pairs[0][0] and ilep != labeled_pairs[0][1] )
                  #print("ilep {} lead1 {} lead2 {} decision {}".format( ilep, labeled_pairs[0][0], labeled_pairs[0][1], isValidPair) )

               if isValidPair: 
                  second_pair = ipair
                  isValidSecondPair = True
               #else:
               #   isValidSecondPair = False

       if not isValidSecondPair: 
          #print("Kill!")
          continue

       cutflow["cutflow"].Fill( 4, finalWeight )


       if nGoodLeptons != 4:
          #print("NO ALL GOOD LEPTONS!")
          continue

       cutflow["cutflow"].Fill( 5, finalWeight )

       #print("second pair ", second_pair)
       #Works because of the sorting! Should be careful though ...
       #second_pair = 1
       #First finding leading pair
       #min_mZ_dif= 99999999
       #lead_pair = -1
       #for ip, pair in enumerate(labeled_pairs):
       #  dilep = ROOT.TLorentzVector()
       #  
       #  for ilep in (pair[0], pair[1] ):
       #     lep = ROOT.TLorentzVector()
       #     lep.SetPtEtaPhiE( tree.lep_pt[ilep], tree.lep_eta[ilep], tree.lep_phi[ilep], tree.lep_E[ilep] )
       #     dilep += lep

       #  #print("dilep M{}".format(dilep.M()))
       #  #print(" pair {},  difference: {}".format( ip, abs(mZ - (dilep.M()*0.001) ) )  )
       #  if( abs(mZ - (dilep.M()*0.001) ) < min_mZ_dif ):
       #     #print("New lead pair! min diff", min_mZ_dif)
       #     min_mZ_dif = abs(mZ - (dilep.M()*0.001) ) 
       #     lead_pair  = ip


       ##Now find the second pair, which does not contain the leptons from the first lead pair
       #second_pair = -1
       #for ip, pair in enumerate(labeled_pairs):
       #   if ip == lead_pair: continue

       #   #print("second pair {}".format(ip) )
       #   for ilep in (pair[0], pair[1] ):
       #        #print("ilep {}  first lead {} second lead {}".format( ilep, labeled_pairs[lead_pair][0], labeled_pairs[lead_pair][1] ) )
       #        if( ilep != labeled_pairs[lead_pair][0] and ilep != labeled_pairs[lead_pair][1] ):
       #            #print("Checking second pair")
       #            second_pair = ip

       #ERROR!!
       if lead_pair == -1:
          print("First pair err: SHOULD NOT HAPPEN!")

       if  second_pair == -1: 
          print("Second pair err: SHOULD NOT HAPPEN!")
          print(labeled_pairs)
          for pair in all_pairs:
            #print(pair, type(pair)) 
            ilep = pair[0]
            jlep = pair[1]
            #print("i {} j {}".format(ilep, jlep) )
            #pair_type = check_pair_type( tree.lep_charge[ilep], tree.lep_charge[jlep], tree.lep_type[ilep], tree.lep_type[jlep], True )
            #print(pair_type)

      
         
       #Printing selected pairs
       #print("Processing event") 
       #print("lead: ",   labeled_pairs[lead_pair])
       #print("second: ", labeled_pairs[second_pair])
       #for ip, ipair in enumerate(labeled_pairs):
       #     print(ipair)
       #     print("ipair {} ilep {} charge {} type {}".format(ip, ipair[0], tree.lep_charge[ ipair[0] ], tree.lep_type[ ipair[0] ]  ) )
       #     print("ipair {} ilep {} charge {} type {}".format(ip, ipair[1], tree.lep_charge[ ipair[1] ], tree.lep_type[ ipair[1] ]  ) )

       #     print("Dilepton type: {} Inv mass: {}".format( ipair[2], ipair[3].M()*0.001 ))

       #Identify flavour for the channels (4e,4m,2e2m,2m2e):
       lead_pair_flavour = ""
       if(   isElectron( tree.lep_type[ labeled_pairs[lead_pair][0] ] ) ) : lead_pair_flavour = "2e" 
       elif( isMuon(tree.lep_type[ labeled_pairs[lead_pair][0] ] ))    : lead_pair_flavour = "2m"   
       else: 
         #print("FIXME: warning should not happen")
         pass


       second_pair_flavour = ""
       if( isElectron(tree.lep_type[ labeled_pairs[second_pair][0] ] ) ) :   second_pair_flavour = "2e" 
       elif( isMuon(tree.lep_type[ labeled_pairs[second_pair][0] ] ) ) : second_pair_flavour = "2m" 
       else: 
         #print("FIXME: warning should not happen")
         pass

       event_4l_flavour = ""
       if( lead_pair_flavour == second_pair_flavour ):
            event_4l_flavour = lead_pair_flavour
            event_4l_flavour = event_4l_flavour.replace( "2", "4" )
       else:
            event_4l_flavour = lead_pair_flavour + second_pair_flavour


       #print("EVENT FLAVOUR {}".format(event_4l_flavour) )
       cut_map = pass_event_flavour(event_4l_flavour, cut_map)
       #for cut, decision in cut_map.items():
       #  print("cut {} decision {}".format(cut,decision))

       #for ilep in range(len(tree.lep_pt) ):
       #     print("ilep {} pt {}".format(ilep, tree.lep_pt[ilep]))

   
       #h_map1d["m4l"].Fill(  sum_lv.M()*0.001, finalWeight  )
       fill_1d( "m4l",        sum_lv.M()*0.001, finalWeight, h_map1d, cut_map )
       fill_1d( "m4l_zoom",   sum_lv.M()*0.001, finalWeight, h_map1d, cut_map )
       #fill_1d( "njets",      tree.jet_n,       finalWeight, h_map1d, cut_map )

       fill_1d( "nleptons", lep_n,   finalWeight, h_map1d, cut_map )
       fill_1d( "met", tree.met_et*0.001,   finalWeight, h_map1d, cut_map )

       nGoodJets = 0
       for ijet in range(0, len(tree.jet_pt) ):
         goodJet = isGoodJet(tree, ijet) 

         if not goodJet: continue

         nGoodJets += 1

         fill_1d( "jall_pt",   tree.jet_pt[ijet]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "jall_jvt",  tree.jet_jvt[ijet], finalWeight, h_map1d, cut_map )

       #fill_1d( "njets", tree.jet_n, finalWeight, h_map1d, cut_map )
       fill_1d( "njets", nGoodJets, finalWeight, h_map1d, cut_map )

       for i in range(0, lep_n):

         #We are not ready for 5 and more leptons ...
         if(i > 3): continue

         fill_1d( "lep{}_pt".format(i+1), tree.lep_pt[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "lep{}_eta".format(i+1), tree.lep_eta[i], finalWeight, h_map1d, cut_map )
         fill_1d( "lep{}_phi".format(i+1), tree.lep_phi[i]/(3.14159265359), finalWeight, h_map1d, cut_map )

         fill_1d( "lep{}_ptcone30".format(i+1), tree.lep_ptcone30[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "lep{}_etcone20".format(i+1), tree.lep_etcone20[i]*0.001, finalWeight, h_map1d, cut_map )

         fill_1d( "lep{}_E".format(i+1), tree.lep_E[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "lep{}_z0".format(i+1), tree.lep_z0[i], finalWeight, h_map1d, cut_map )
         fill_1d( "lep{}_d0".format(i+1), tree.lep_trackd0pvunbiased[i], finalWeight, h_map1d, cut_map )
         fill_1d( "lep{}_isTight".format(i+1), (1 if tree.lep_isTightID[i] else 0), finalWeight, h_map1d, cut_map )

         fill_1d( "lepall_pt",  tree.lep_pt[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "lepall_eta", tree.lep_eta[i], finalWeight, h_map1d, cut_map )
         fill_1d( "lepall_phi", tree.lep_phi[i]/(3.14159265359), finalWeight, h_map1d, cut_map )

         fill_1d( "lepall_E" , tree.lep_E[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "lepall_z0", tree.lep_z0[i], finalWeight, h_map1d, cut_map )
         fill_1d( "lepall_d0", tree.lep_trackd0pvunbiased[i], finalWeight, h_map1d, cut_map )
         fill_1d( "lepall_isTight", (1 if tree.lep_isTightID[i] else 0), finalWeight, h_map1d, cut_map )



       lepton_quad = ROOT.TLorentzVector()


       #labeled_pairs[]
       #Fill lead and second quantities 
       m12, m23 = None, None
       for ip, pair_id in enumerate([lead_pair, second_pair]):

         #OBSOLETE
         #dilep = ROOT.TLorentzVector()
         #for ilep in (labeled_pairs[pair_id][0], labeled_pairs[pair_id][1]):
         #   lep = ROOT.TLorentzVector()
         #   lep.SetPtEtaPhiE( tree.lep_pt[ilep], tree.lep_eta[ilep], tree.lep_phi[ilep], tree.lep_E[ilep] )
         #   dilep += lep

         lepton_quad += labeled_pairs[pair_id][3]
         #FIXME: Very dangerous!
         label = "12" 
         m12   = labeled_pairs[pair_id][3]
         if ip != 0: 
            label = "23"
            m23 = labeled_pairs[pair_id][3]

         #h_map1d["m{}".format(label)].Fill(  (dilep.M() )*0.001, finalWeight  )
         fill_1d( "m{}".format(label),  ( (labeled_pairs[pair_id][3]).M() )*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "m{}_zoom".format(label),  ( (labeled_pairs[pair_id][3]).M() )*0.001, finalWeight, h_map1d, cut_map )


       fill_2d( "m12_vs_m23",  (m12.M())*0.001, m23.M()*0.001, finalWeight, h_map2d, cut_map )

       fill_1d( "lepquad_pt",       lepton_quad.Pt()*0.001, finalWeight, h_map1d, cut_map )
       fill_1d( "lepquad_eta",      lepton_quad.Eta(), finalWeight, h_map1d, cut_map )
       fill_1d( "lepquad_phi",      lepton_quad.Phi()/(3.14159265359), finalWeight, h_map1d, cut_map )
       fill_1d( "lepquad_E",        lepton_quad.E()*0.001, finalWeight, h_map1d, cut_map )
       #fill_1d( "lepquad_ptcone30", tree.lep_ptcone30[i]*0.001, finalWeight, h_map1d, cut_map )
       #fill_1d( "lepquad_etcone20", tree.lep_etcone20[i]*0.001, finalWeight, h_map1d, cut_map )
       #fill_1d( "lepquad_z0",       tree.lep_z0[i], finalWeight, h_map1d, cut_map )
       #fill_1d( "lepquad_d0",       tree.lep_trackd0pvunbiased[i], finalWeight, h_map1d, cut_map )
       #fill_1d( "lepquad_isTight",  (1 if tree.lep_isTightID[i] else 0), finalWeight, h_map1d, cut_map )

       #it += 1

   print "Histogram is filled" # Signifies the end of the event loop above
   f_out = ROOT.TFile("{}/proccessed_{}".format(output_dir, sample), "RECREATE" )

   for channel in flavour_channels:
      f_out.cd()
      f_out.mkdir(channel)
      f_out.cd(channel)

      print(channel)
      for name, hist in h_map1d.items():
         if channel not in name: continue

         #print("old name", name)
         tmp_name = name.replace( "{}/".format(channel), "" )
         #print("saving new name:", tmp_name)
         hist.SetName( tmp_name )
         hist.Write()

   #Save cutflow histograms
   f_out.cd()
   for cf, hist in cutflow.items():
         hist.Write()
   
   f_out.Close()
	
