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
ROOT.gROOT.SetStyle("ATLAS");
ROOT.gROOT.ForceStyle();

# Here we open the data that we want to analyse, which is in the form of a .root file. A .root file consists of a tree having branches and leaves.
samples = [
		"mc_345060.ggH125_ZZ4lep.4lep.root",
		"mc_363490.llll.4lep.root",
      "data16.root"
	  ]


input_dir = "/project/atlas/users/mvozak/Bsc/output/"
plot_dir  = "/project/atlas/users/mvozak/Bsc/figures/"
lumi_data = 10


def get_short_name(sample):
	if   "363490" in sample: return "gg -> ZZ -> 4l"
	elif "345060" in sample: return "gg -> H -> ZZ -> 4l"
	else: return sample


def dress_histogram(name, hist):
	if   "363490" in name: 
		hist.SetFillColor(ROOT.kRed)
		hist.SetLineColor(ROOT.kRed)
	elif "345060" in name:
		hist.SetFillColor(ROOT.kBlue)
		hist.SetLineColor(ROOT.kBlue)
	else: 
		pass

	hist.SetTitle( get_short_name( name ) )
	return hist



#event_channels = ["4m", "4e", "2m2e", "2e2m"]#, "inc"]
event_channels = ["inc"]
for event_channel in event_channels:
#stackChannels = True 
 for h_name in ["m4l", "m12", "pt1", "pt2", "pt3", "pt4", "ptall", "etaall", "njets" ]:
   #event_channel = "4m"
   #h_name = "m4l"
   
   hists = {}
   
   for sample in samples:
      #Open a ROOT file
      f = ROOT.TFile.Open("{}/proccessed_{}".format(input_dir, sample), "READ")

      #h_inc = None 
     # for event_channel in event_channels:

        #    if stackChannels:
        #       #if event_channel
        #       pass

        #    #Retrieve a histogram
        #    full_hname = "{}/{}".format(event_channel, h_name)
        #    h = f.Get(full_hname)
        #    
        #    #Check whether the retrieval was done correctly
        #    if not h:
        #    	print("Histogram not properly loaded, is the name correct? {}".format(full_hname) )
        #    	exit()
        #    
        #    #Remove ownership of the histogram
        #    h.SetDirectory(0)
        #    if h_inc == None:
        #          h_inc = h
        #    else:
        #          h_inc.Add( h )

      #Retrieve a histogram
      full_hname = "{}/{}".format(event_channel, h_name)
      h = f.Get(full_hname)
      
      #Check whether the retrieval was done correctly
      if not h:
      	print("Histogram not properly loaded, is the name correct? {}".format(full_hname) )
      	exit()
      
      #Remove ownership of the histogram
      h.SetDirectory(0)

      #Store in the dictionary for later use
      #hists[sample] = h_inc
      hists[sample] = h
      
      f.Close()
   
   event_channel = "inc"
   # Define a 'canvas' on which to draw a histogram. Its name is "canvas" and its header is "plot a variable". The two following arguments define the width and the height of the canvas.
   canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
   canvas.cd()
   
   leg = ROOT.TLegend(.50,.60,.80,.80)
   leg.SetBorderSize(0)
   leg.SetFillColor(0)
   leg.SetFillStyle(0)
   leg.SetTextFont(42)
   leg.SetTextSize(0.035)
   
   #ROOT.gStyle.SetPalette(57)
   #cols = ROOT.TColor.GetPalette()
   
   
   
   #Stack histograms
   stack 	   = None #ROOT.THStack("hs","");
   data        = None
   for name, hist in hists.items():
      if "data" in name: 
        print("data skipping")
        data = hist
      else:
         if stack == None: stack = hist
         else: stack.Add( hist )
         #stacked_mc[name] = stack
   
   
   data.SetLineColor(ROOT.kBlack)
   data.SetMarkerStyle(20)
   data.SetMarkerSize(0.5)
   data.SetMarkerColor(ROOT.kBlack)
   leg.AddEntry(data, "Data 16" , 'pl')
   data.Draw("E")
   
   #Higgs + SM ZZ
   stack.SetLineColor(ROOT.kRed)
   stack.SetFillColor(ROOT.kRed)
   leg.AddEntry(stack, get_short_name("345060") , 'f')
   stack.Draw("same hist")
   
   #Just SM ZZ
   smzz = hists["mc_363490.llll.4lep.root"] #not very safe way to retrieve ..
   smzz.SetLineColor(ROOT.kBlue)
   smzz.SetFillColor(ROOT.kBlue)
   leg.AddEntry(smzz, get_short_name("363490") , 'f')
   smzz.Draw("same hist")
   
   
   #Plot all combinations over
   #for name, hist in stacked_mc.items():
   #	print("Plotting hist: {} with int {}".format(name, hist.Integral() ))
   #	hist = dress_histogram(name, hist)	
   #	hist.Draw("same hist")
   leg.Draw("same")
   
   canvas.Print("{}/{}_{}.pdf".format(plot_dir, h_name, event_channel))
