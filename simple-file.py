########################################################################################
#                                                                                      #
#               A simple introductional notebook to HEP analysis in python             #
#       In this notebook you can find an easy set of commands that show the basic      #
#       computing techniques commonly used in high energy physics (HEP) analyzes.      #
#       It also shows how to create a histogram, fill it and draw it, using ROOT       #
#       (https://root.cern.ch/). ROOT is a scientific software framework that          #
#       provides all the functionalities needed to deal with big data processing,      #
#       statistical analysis, visualisation and storage.                               #
#                                                                                      #
# Run this script by typing:                                                           #
#       >> python A-simple-example.py                                                  #
#                                                                                      #
#       At the end you get a plot with the number of leptons.                          #
########################################################################################



#ROOT is imported to read the files in the .root data format.
import ROOT

ROOT.gROOT.SetBatch(ROOT.kFALSE)

#def pair_is_SFOC( charge_i, charge_j, type_i, type_j):
# 		if charge_i != (-charge_j): return False
#    	if type_i != type_j: return False
#      return True
#
#def pair_is_DFOC( charge_i, charge_j, type_i, type_j):
# 		if charge_i != (-charge_j): return False
#    	if type_i == type_j: return False
#      return True
#
#def pair_is_SFSC( charge_i, charge_j, type_i, type_j):
# 		if charge_i != (charge_j): return False
#    	if type_i != type_j: return False
#      return True

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



# Here we open the data that we want to analyse, which is in the form of a .root file. A .root file consists of a tree having branches and leaves.
samples = [
		"mc_345060.ggH125_ZZ4lep.4lep.root",
		"mc_363490.llll.4lep.root",
      "data_A.4lep.root",
      "data_B.4lep.root",
      "data_C.4lep.root",
      "data_D.4lep.root"
	      ]


output_dir = "/project/atlas/users/mvozak/Bsc/output/"
lumi_data = 10



flavour_channels = [ "4m", "4e", "2e2m", "2m2e", "inc" ]
combination_type = ["SFOC", "DFOC", "SFSC" ]


#def get_event_flavour_channel( lead_pair, second_pair ):


for sample in samples:
   folder_name = "MC"
   isMC        = True

   if "data" in sample: 
      folder_name = "Data"
      isMC        = False

   f = ROOT.TFile.Open("/data/atlas/users/mvozak/opendata/4lep/{}/{}".format( folder_name ,sample ) )
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
   
   for channel in flavour_channels:
      h_map1d[channel + "/m4l"]   = ROOT.TH1F(channel + "/m4l","Inv mass 4l: Invariant mass of 4l; m_{4l} [GeV]; Events ",250, 50, 550)
      h_map1d[channel + "/m12"]   = ROOT.TH1F(channel + "/m12","Inv mass 12: Invariant mass of m12; m_{12} [GeV]; Events ",200, 0, 200)
      h_map1d[channel + "/m23"]   = ROOT.TH1F(channel + "/m23","Inv mass 23: Invariant mass of m23; m_{23} [GeV]; Events ",200, 0, 200)
      

      h_map1d[channel + "/ptall"] = ROOT.TH1F(channel + "/ptall","Transverse momenta of leptons: Transverse momenta of leptons; p_{Tall} [GeV]; Events ",150, 0, 150)
      h_map1d[channel + "/pt1"]   = ROOT.TH1F(channel + "/pt1","Transverse momenta of 1st lepton: Transverse momenta of the 1st lepton; p_{T1} [GeV]; Events ",150, 0, 150)
      h_map1d[channel + "/pt2"]   = ROOT.TH1F(channel + "/pt2","Transverse momenta of 2nd lepton: Transverse momenta of the 2nd lepton; p_{T2} [GeV]; Events ",150, 0, 150)
      h_map1d[channel + "/pt3"]   = ROOT.TH1F(channel + "/pt3","Transverse momenta of 3rd lepton: Transverse momenta of the 3rd lepton; p_{T3} [GeV]; Events ",150, 0, 150)
      h_map1d[channel + "/pt4"]   = ROOT.TH1F(channel + "/pt4","Transverse momenta of 4rd lepton: Transverse momenta of the 4rd lepton; p_{T4} [GeV]; Events ",150, 0, 150)

      h_map1d[channel + "/etaall"]  = ROOT.TH1F(channel + "/etaall","Pseudorapidity of leptons: Pseudorapidity of leptons; #eta_{all}; Events ",54, -2.7, 2.7)
      h_map1d[channel + "/eta1"]  = ROOT.TH1F(channel + "/eta1","Pseudorapidity of 1st lepton: Pseudorapidity of the 1st lepton; #eta_{1}; Events ",54, -2.7, 2.7)
      h_map1d[channel + "/eta2"]  = ROOT.TH1F(channel + "/eta2","Pseudorapidity of 2nd lepton: Pseudorapidity of the 2nd lepton; #eta_{2}; Events ",54, -2.7, 2.7)
      h_map1d[channel + "/eta3"]  = ROOT.TH1F(channel + "/eta3","Pseudorapidity of 3rd lepton: Pseudorapidity of the 3rd lepton; #eta_{3}; Events ",54, -2.7, 2.7)
      h_map1d[channel + "/eta4"]  = ROOT.TH1F(channel + "/eta4","Pseudorapidity of 4rd lepton: Pseudorapidity of the 4rd lepton; #eta_{4}; Events ",54, -2.7, 2.7)


      h_map1d[channel + "/phiall"]  = ROOT.TH1F(channel + "/phiall","Azimuthal angle of all leptons: Azimuthal angle of the all leptons; #phi_{all}/#pi ; Events ",20, -1, 1)
      h_map1d[channel + "/phi1"]  = ROOT.TH1F(channel + "/phi1","Azimuthal angle of 1st lepton: Azimuthal angle of the 1st lepton; #phi_{1}/#pi ; Events ",20, -1, 1)
      h_map1d[channel + "/phi2"]  = ROOT.TH1F(channel + "/phi2","Azimuthal angle of 2nd lepton: Azimuthal angle of the 2nd lepton; #phi_{2}/#pi ; Events ",20, -1, 1)
      h_map1d[channel + "/phi3"]  = ROOT.TH1F(channel + "/phi3","Azimuthal angle of 3rd lepton: Azimuthal angle of the 3rd lepton; #phi_{3}/#pi ; Events ",20, -1, 1)
      h_map1d[channel + "/phi4"]  = ROOT.TH1F(channel + "/phi4","Azimuthal angle of 4rd lepton: Azimuthal angle of the 4rd lepton; #phi_{4}/#pi ; Events ",20, -1, 1)

      h_map1d[channel + "/njets"]  = ROOT.TH1F(channel + "/njets","Number of jets: Number of jets; njets; Events ", 6, -0.5, 5.5)
      h_map1d[channel + "/ptjall"] = ROOT.TH1F(channel + "/ptjall","Transverse momenta of jets: Transverse momenta of jets; p_{T}^{all jets} [GeV]; Events ",150, 0, 150)
   
   # Loop over the data (in the tree) and store it in the histogram.
   #       Here you could place any cuts you want to apply, before filling the histogram
   
   cut_map = {}
   it = 0
   for event in tree:
       #print("Event position : {}".format(it) )
       if it > 10: break

       cut_map = reset_cut_map(cut_map)
       #print(it)
   
       #print("lep pt branch: ", tree.lep_pt)
       #print(len(tree.lep_pt)) 
   
       #Check for the Trigger
       print( "Trig E: ", tree.trigE, " trigM: ", tree.trigM )
       if not tree.trigE and not tree.trigM: continue
       print("pass trigger")
   
       #print(tree.XSection)
       sum_lv = ROOT.TLorentzVector()
   
       for i in range(len(tree.lep_pt)):
   	   lv = ROOT.TLorentzVector()
   	   lv.SetPtEtaPhiE( tree.lep_pt[i], tree.lep_eta[i], tree.lep_phi[i], tree.lep_E[i] )
   	   sum_lv += lv
   	
   
   
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

         #Now select whichever pairs we want, for now only sfos
         if pair_type != "SFOC": continue

         labeled_pairs.append( [ilep, jlep, pair_type] )

       #print("Labelled pairs")
       #print(labeled_pairs)
       #two sfos with close to zmass selection
       #Make sure that indices don't repeat in the different pairs      
       #sfos_pairs = []


       #FIXME: It can happen that there no 2SFOS (none or only one), for now skip!
       if len(labeled_pairs) < 2: continue

       #First finding leading pair
       mZ        = 91.1876
       min_mZ_dif= 99999999
       lead_pair = -1
       for ip, pair in enumerate(labeled_pairs):
         dilep = ROOT.TLorentzVector()
         
         for ilep in (pair[0], pair[1] ):
            lep = ROOT.TLorentzVector()
            lep.SetPtEtaPhiE( tree.lep_pt[ilep], tree.lep_eta[ilep], tree.lep_phi[ilep], tree.lep_E[ilep] )
            dilep += lep

         #print("dilep M{}".format(dilep.M()))
         #print(" pair {},  difference: {}".format( ip, abs(mZ - (dilep.M()*0.001) ) )  )
         if( abs(mZ - (dilep.M()*0.001) ) < min_mZ_dif ):
            #print("New lead pair! min diff", min_mZ_dif)
            min_mZ_dif = abs(mZ - (dilep.M()*0.001) ) 
            lead_pair  = ip


       #Now find the second pair, which does not contain the leptons from the first lead pair
       second_pair = -1
       for ip, pair in enumerate(labeled_pairs):
          if ip == lead_pair: continue

          #print("second pair {}".format(ip) )
          for ilep in (pair[0], pair[1] ):
               #print("ilep {}  first lead {} second lead {}".format( ilep, labeled_pairs[lead_pair][0], labeled_pairs[lead_pair][1] ) )
               if( ilep != labeled_pairs[lead_pair][0] and ilep != labeled_pairs[lead_pair][1] ):
                   #print("Checking second pair")
                   second_pair = ip

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
       #print("lead: ",   labeled_pairs[lead_pair])
       #print("second: ", labeled_pairs[second_pair])


       #Identify flavour for the channels:
       lead_pair_flavour = ""
       if( abs(tree.lep_type[ labeled_pairs[lead_pair][0] ] ) == 11) :   lead_pair_flavour = "2e" 
       elif( abs(tree.lep_type[ labeled_pairs[lead_pair][0] ] ) == 13) : lead_pair_flavour = "2m" 
       else: 
         #print("FIXME: warning should not happen")
         pass


       second_pair_flavour = ""
       if( abs(tree.lep_type[ labeled_pairs[second_pair][0] ] ) == 11) :   second_pair_flavour = "2e" 
       elif( abs(tree.lep_type[ labeled_pairs[second_pair][0] ] ) == 13) : second_pair_flavour = "2m" 
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

   

       #FILLING THE HISTOGRAMS!!
       finalWeight = 1.
       if isMC:
         finalWeight *= tree.XSection * 1000 * lumi_data * tree.mcWeight * (1./tree.SumWeights)

         #Add pile up reweighting
         finalWeight *= tree.scaleFactor_PILEUP
         print( tree.scaleFactor_PILEUP )


         #Apply lepton SFs
         #lep_isTightID
         #scaleFactor_MUON/ELE

   
   
       #h_map1d["m4l"].Fill(  sum_lv.M()*0.001, finalWeight  )
       fill_1d( "m4l",   sum_lv.M()*0.001, finalWeight, h_map1d, cut_map )
       fill_1d( "njets", tree.jet_n,       finalWeight, h_map1d, cut_map )


       for j in range(0, len(tree.jet_pt)):
         fill_1d( "ptjall",  tree.jet_pt[j]*0.001, finalWeight, h_map1d, cut_map )

       for i in range(0, lep_n):

         #We are not ready for 5 and more leptons ...
         if(i > 3): continue

         fill_1d( "pt{}".format(i+1), tree.lep_pt[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "eta{}".format(i+1), tree.lep_eta[i], finalWeight, h_map1d, cut_map )
         fill_1d( "phi{}".format(i+1), tree.lep_phi[i]/(3.14159265359), finalWeight, h_map1d, cut_map )

         fill_1d( "ptall",  tree.lep_pt[i]*0.001, finalWeight, h_map1d, cut_map )
         fill_1d( "etaall", tree.lep_eta[i], finalWeight, h_map1d, cut_map )
         fill_1d( "phiall", tree.lep_phi[i]/(3.14159265359), finalWeight, h_map1d, cut_map )


       #Fill lead and second quantities 
       for ip, pair_id in enumerate([lead_pair, second_pair]):
         dilep = ROOT.TLorentzVector()
         
         for ilep in (labeled_pairs[pair_id][0], labeled_pairs[pair_id][1]):
            lep = ROOT.TLorentzVector()
            lep.SetPtEtaPhiE( tree.lep_pt[ilep], tree.lep_eta[ilep], tree.lep_phi[ilep], tree.lep_E[ilep] )
            dilep += lep

         #FIXME: dangerous!
         label = "12" 
         if ip != 0: label = "23"

         #h_map1d["m{}".format(label)].Fill(  (dilep.M() )*0.001, finalWeight  )
         fill_1d( "m{}".format(label),  (dilep.M() )*0.001, finalWeight, h_map1d, cut_map )

      #TODO!!!! FILL HISTOGRAMS WITH PARTICULAR EVENT FLAVOUR!


       it += 1


   print "Histogram is filled" # Signifies the end of the event loop above
   f_out = ROOT.TFile("{}/proccessed_{}".format(output_dir, sample), "RECREATE" )

   for channel in flavour_channels:
      f_out.cd()
      f_out.mkdir(channel)
      f_out.cd(channel)

      print(channel)
      for name, hist in h_map1d.items():
         if channel not in name: continue

         print("old name", name)
         tmp_name = name.replace( "{}/".format(channel), "" )
         print("saving new name:", tmp_name)
         hist.SetName( tmp_name )
         hist.Write()
   #hist.Write()
   
   f_out.Close()
	
	# Now want to draw the histogram, and set the fill colour
	#hist.SetLineColor(ROOT.kBlack)
	#hist.SetLineWidth(2)
	#hist.SetFillColor(ROOT.kAzure)
	#hist.Draw("HIST")
	
	# Draw the canvas, which contains the histogram
	#canvas.Update()
	
	# The following lines allow the canvas to be displayed,
	#       until you press enter in the command line.
	#try:
	#    __IPYTHON__
	#except:
	#    raw_input('Press Enter to exit')
	
	# Next we can also normalise the histogram (so the integral is 1), to allow us to see the proportions. By doing this, you can directly read of the y-axis what fraction of events fall into each bin.
	#scale = hist.Integral()
	#hist.Scale(1/scale)
	
	# Set some new colour settings for the histogram
	#hist.SetLineColor(ROOT.kBlack)
	#hist.SetLineWidth(2)
	#hist.SetFillColor(ROOT.kViolet)
	#
	## Again we re-draw the histogram and canvas.
	#hist.Draw("HIST")
	#canvas.Draw()
	#canvas.Print("my_hist.jpg")
	#
	#try:
	#    __IPYTHON__
	#except:
	#    raw_input('Press Enter to exit')
	
	##############################################################################################################################################
	#
	#       Exercise to try: How could you select to have exactly 2 leptons (i.e. lep_n ==2) ?
	#               You can check if you've done it correctly by looking at the resulting histograms. What do you expect will change?
	#               What do you notice about the number of entries in the histogram now?
	#               *Hint*: There's a comment above indicating where in the code you should place your cuts.
	#
	#       Bonus exercise: Can you try plotting another variable instead of "number of leptons"?
	#               e.g. What about the number of jets?
	#               *Hint*: the number of jets variable is labelled "jet_n" in the tree.
	#               You might also need to change the x-axis range of the histogram.
	#
	##############################################################################################################################################
