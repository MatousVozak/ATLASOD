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

ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("ATLAS");
ROOT.gROOT.ForceStyle();


def create_dummy(hist, fixed_value=0):

  dummy = hist.Clone()
  dummy.SetDirectory(0)

  nbins = dummy.GetNbinsX()
  xmin  = dummy.GetBinLowEdge(1)
  xmax  = dummy.GetBinLowEdge(nbins) + dummy.GetBinWidth(nbins)

  dummy.SetLineColor(ROOT.kBlack)

  for i in range(1, nbins+1):
    dummy.SetBinContent(i,fixed_value)
    dummy.SetBinError(i,0)

  return dummy, xmin, xmax

# Here we open the data that we want to analyse, which is in the form of a .root file. A .root file consists of a tree having branches and leaves.
samples = [
		"mc_345060.ggH125_ZZ4lep.4lep.root",
		"mc_363490.llll.4lep.root",
    "mc_410000.ttbar_lep.4lep.root",
    "mc_363491.lllv.4lep.root",

    #"zmumu.root",
    #"zee.root",
    #"ztautau.root",
    "mc_361106.Zee.4lep.root",
    "mc_361107.Zmumu.4lep.root",
    #"mc_361108.Ztautau.4lep.root",
#proccessed_mc_363356.ZqqZll.4lep.root  proccessed_mc_363358.WqqZll.4lep.root

    #"data.4lep.root",
    "data16.root",
	  ]


input_dir = "/project/atlas/users/mvozak/ATLASOD/output/"
plot_dir  = "/project/atlas/users/mvozak/ATLASOD/figures/"
lumi_data = 10

def get_sample_id(sample):
  if   "363490" in sample: return "ZZ"
  elif "345060" in sample: return "HZZ"
  elif "410000" in sample: return "ttbar"
  elif "363491" in sample: return "WZ"
  elif "zmumu" in sample or "Zmumu" in sample:  return "Zmumu"
  elif "zee" in sample or "Zee" in sample:  return "Zee"
  elif "ztautau" in sample or "Ztautau" in sample:  return "Ztautau"
  elif "zll" in sample:  return "Zll"
  elif "data" in sample:  return "data"
  else:
    return sample

def get_short_name(sample):
  if   "ZZ"     in sample: return "gg -> ZZ -> 4l"
  elif "HZZ"    in sample: return "gg -> H -> ZZ -> 4l"
  elif "ttbar"  in sample: return "ttbar"
  elif "WZ" in sample: return "WZ"
  elif "Zmumu"  in sample: return "Zmumu"
  elif "Zee"    in sample: return "Zee"
  elif "Ztautau"in sample: return "Ztautau"
  elif "Zll"    in sample: return "Zll"
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


cWheel = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kAzure]
mWheel = [20, 21, 22, 23, 24, 25, 26, 27, 28 ]
title_size = 20
title_font = 43
label_size = 10
label_font = 43
ytitle_offset = 1.
xtitle_offset = 2.

#event_channels = ["4m", "4e", "2m2e", "2e2m"]#, "inc"]
event_channels = ["inc", "4m", "4e", "2m2e", "2e2m"]
for event_channel in event_channels:
#stackChannels = True 
 for h_name in ["m4l", "m12",  "m23", "m4l_zoom", "m12_zoom", "m23_zoom",
               "lep1_pt", "lep2_pt", "lep3_pt", "lep4_pt", "lepall_pt",
              # "lep1_ptcone30", "lep2_ptcone30", "lep3_ptcone30", "lep4_ptcone30", "lepall_ptcone30",
              # "lep1_etcone20", "lep2_etcone20", "lep3_etcone20", "lep4_etcone20", "lepall_etcone20",
              # "lep1_E", "lep2_E", "lep3_E", "lep4_E", "lepall_E",
              # "lep1_eta", "lep2_eta", "lep3_eta", "lep4_eta", "lepall_eta",
              # "lep1_phi", "lep2_phi", "lep3_phi", "lep4_phi", "lepall_phi",
              # "lep1_z0", "lep2_z0", "lep3_z0", "lep4_z0", "lepall_z0",
              # "lep1_d0", "lep2_d0", "lep3_d0", "lep4_d0", "lepall_d0",
              # "lep1_isTight", "lep2_isTight", "lep3_isTight", "lep4_isTight", "lepall_isTight",
               "met", "njets", "nleptons", "jall_pt", "jall_jvt" ]:
   #event_channel = "4m"
   #h_name = "m4l"
   
   hists = {}
   
   for sample in samples:
      print("Working on sample {}".format(sample))
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

      if "_pt" in full_hname: h.Rebin(5)

      #Store in the dictionary for later use
      #hists[sample] = h_inc
      id_name = get_sample_id(sample)
      #hists[sample] = h
      print("Adding {} to the hist".format(id_name))
      hists[id_name] = h
      
      f.Close()
   
   #event_channel = "inc"

   #Stack histograms
   stack 	   = None #ROOT.THStack("hs","");
   data      = None
   for name, hist in hists.items():
      if "data" in name: 
        print("data skipping")
        data = hist
      else:
         pass
          #FIXME: obsolete
         #if stack == None: stack = hist
         #else: stack.Add( hist )
         #stacked_mc[name] = stack


  #Creating ordered stack
  #-----------------------------------------
   h_stacks  = {} # Stacking order: zjets, ttbar, WZ, ZZ, HZZ
   mc_list   = []
  # if "Zjets" in hists:
  #    h_stacks["Zjets"] =  hists["Zjets"] 
  #    mc_list.append("Zjets")
  #FIXME: does not cover Zee and Ztautau case
   #elif "Zmumu" in hists:
   #   h_stacks["ttbar"] =  stack.Clone("ttbar")
   #   mc_list.append("ttbar")

   #   h_stacks["Zjets"] =  hists["Zmumu"].Clone() 
   #   h_stacks["Zjets"].Add( hists["Zee"] )
   #   h_stacks["Zjets"].Add( hists["Ztautau"] )

   #   mc_list.append("Zjets")

   #   if stack == None: stack = h_stacks["Zjets"].Clone()
   #   else: stack.Add( h_stacks["Zjets"] )

   if "Zmumu" in hists:
      if stack == None: stack = hists["Zmumu"].Clone()
      else: stack.Add( hists["Zmumu"] )
      h_stacks["Zmumu"] =  stack.Clone("Zmumu")
      mc_list.append("Zmumu")
   else: print("ZMUMU NOT IN THE HISTOGRAMS")

   if "Ztautau" in hists:
      if stack == None: stack = hists["Ztautau"].Clone()
      else: stack.Add( hists["Ztautau"] )
      h_stacks["Ztautau"] =  stack.Clone("Ztautau")
      mc_list.append("Ztautau")
   else: print("ZTAUTAU NOT IN THE HISTOGRAMS")

   if "Zee" in hists:
      if stack == None: stack = hists["Zee"].Clone()
      else: stack.Add( hists["Zee"] )
      h_stacks["Zee"] =  stack.Clone("Zee")
      mc_list.append("Zee")
   else: print("ZEE NOT IN THE HISTOGRAMS")
   #print(h_stacks)

   if "ttbar" in hists:
      if stack == None: stack = hists["ttbar"].Clone()
      else: stack.Add( hists["ttbar"] )
      #h = h_stacks["Zjets"].Clone("ttbar")
      #h.Add( hists["ttbar"])
      h_stacks["ttbar"] =  stack.Clone("ttbar")
      mc_list.append("ttbar")


   else: print("TTBAR NOT IN THE HISTOGRAMS")

   if "WZ" in hists:

      if stack == None: stack = hists["WZ"].Clone()
      else: stack.Add( hists["WZ"] )
      #h = h_stacks["ttbar"].Clone("WZ")
      #h.Add( hists["WZ"])
      h_stacks["WZ"] =  stack.Clone("WZ")
      mc_list.append("WZ")
   else: print("WZ NOT IN THE HISTOGRAMS")

   if "ZZ" in hists:
      if stack == None: stack = hists["ZZ"].Clone()
      else: stack.Add( hists["ZZ"] )
      #h = h_stacks["WZ"].Clone("ZZ")
      #h.Add( hists["ZZ"])
      h_stacks["ZZ"] =  stack.Clone("ZZ")
      mc_list.append("ZZ")
   else: print("ZZ NOT IN THE HISTOGRAMS")

   if "HZZ" in hists:
      if stack == None: stack = hists["HZZ"].Clone()
      else: stack.Add( hists["HZZ"] )
      #h = h_stacks["ZZ"].Clone("HZZ")
      #h.Add( hists["HZZ"])

      h_stacks["HZZ"] =  stack.Clone("HZZ")
      mc_list.append("HZZ")
   else: print("HZZ NOT IN THE HISTOGRAMS")

   #stack = h_stacks["HZZ"]
  #-----------------------------------------
  #TODO: 2D plotting

   # Define a 'canvas' on which to draw a histogram. Its name is "canvas" and its header is "plot a variable". The two following arguments define the width and the height of the canvas.
   canvas = ROOT.TCanvas("canvas","plot a variable",800,600)
   canvas.cd()

   top_hist_dummy, xmin,xmax = create_dummy(stack)
   hist_dummy, _,_ = create_dummy(stack, 1.)

   ###-------- Drawing top pad with distributions
   mainPad = ROOT.TPad("mainpad", "mainpad", 0, 0.4, 1 ,1)
   mainPad.Draw()
   mainPad.SetTopMargin(0.1)
   mainPad.SetBottomMargin(0.02)
   mainPad.SetLeftMargin(0.13)
   mainPad.cd()

   top_hist_dummy.Draw()
   top_hist_dummy.GetXaxis().SetLabelSize(0)

   #ymax = hists[process_of_interest].GetMaximum()
   #ymin = hists[process_of_interest].GetMinimum()
   ymax = stack.GetMaximum()
   ymin = stack.GetMinimum()

   top_hist_dummy.GetYaxis().SetRangeUser(0.01, 1.4*ymax)
   top_hist_dummy.GetYaxis().SetTitle("nEntries")
   #top_hist_dummy.GetYaxis().SetRangeUser(0., 2.)
   #top_hist_dummy.SetTitle(cut_name)

   top_hist_dummy.GetYaxis().SetTitleSize( title_size)
   top_hist_dummy.GetYaxis().SetTitleFont( title_font)
   top_hist_dummy.GetYaxis().SetTitleOffset(ytitle_offset)

   top_hist_dummy.GetYaxis().SetLabelSize( label_size)
   top_hist_dummy.GetYaxis().SetLabelFont( label_font)
   
   leg = ROOT.TLegend(.50,.60,.80,.80)
   leg.SetBorderSize(0)
   leg.SetFillColor(0)
   leg.SetFillStyle(0)
   leg.SetTextFont(42)
   leg.SetTextSize(0.035)
   
   #ROOT.gStyle.SetPalette(57)
   #cols = ROOT.TColor.GetPalette()
   
   

   #Higgs + SM ZZ
   if "HZZ" in h_stacks:
    h_stacks["HZZ"].SetLineColor(ROOT.kRed)
    h_stacks["HZZ"].SetFillColor(ROOT.kRed)
    leg.AddEntry(h_stacks["HZZ"], get_short_name("345060") , 'f')
    h_stacks["HZZ"].Draw("same hist")

   #Just SM ZZ
   if "ZZ" in h_stacks:
    h_stacks["ZZ"].SetLineColor(ROOT.kAzure + 7)
    h_stacks["ZZ"].SetFillColor(ROOT.kAzure + 7)
    leg.AddEntry(h_stacks["ZZ"], get_short_name("363490") , 'f')
    h_stacks["ZZ"].Draw("same hist")

   if "WZ" in h_stacks:
    h_stacks["WZ"].SetLineColor(ROOT.kBlue + 1)
    h_stacks["WZ"].SetFillColor(ROOT.kBlue + 1)
    leg.AddEntry(h_stacks["WZ"], "WZ" , 'f')
    h_stacks["WZ"].Draw("same hist")

   if "ttbar" in h_stacks:
    h_stacks["ttbar"].SetLineColor(ROOT.kGreen - 3)
    h_stacks["ttbar"].SetFillColor(ROOT.kGreen - 3)
    leg.AddEntry(h_stacks["ttbar"], "ttbar" , 'f')
    h_stacks["ttbar"].Draw("same hist")

   #Zjets
   #if "Zjets" in h_stacks:
   # h_stacks["Zjets"].SetLineColor(ROOT.kMagenta + 3)
   # h_stacks["Zjets"].SetFillColor(ROOT.kMagenta + 3)
   # leg.AddEntry(h_stacks["Zjets"], "Z+jets" , 'f')
   # h_stacks["Zjets"].Draw("same hist")

   if "Zee" in h_stacks:
    h_stacks["Zee"].SetLineColor(ROOT.kRed + 2)
    h_stacks["Zee"].SetFillColor(ROOT.kRed + 2)
    leg.AddEntry(h_stacks["Zee"], "Zee" , 'f')
    h_stacks["Zee"].Draw("same hist")

   if "Ztautau" in h_stacks:
    h_stacks["Ztautau"].SetLineColor(ROOT.kOrange + 5)
    h_stacks["Ztautau"].SetFillColor(ROOT.kOrange + 5)
    leg.AddEntry(h_stacks["Ztautau"], "Ztautau" , 'f')
    h_stacks["Ztautau"].Draw("same hist")

   if "Zmumu" in h_stacks:
    h_stacks["Zmumu"].SetLineColor(ROOT.kBlue - 5)
    h_stacks["Zmumu"].SetFillColor(ROOT.kBlue - 5)
    leg.AddEntry(h_stacks["Zmumu"], "Zmumu" , 'f')
    h_stacks["Zmumu"].Draw("same hist")

   data.SetLineColor(ROOT.kBlack)
   data.SetMarkerStyle(20)
   data.SetMarkerSize(0.5)
   data.SetMarkerColor(ROOT.kBlack)
   leg.AddEntry(data, "Data 16" , 'pl')
   data.Draw("same E")


   #Plot all combinations over
   #for name, hist in stacked_mc.items():
   #	print("Plotting hist: {} with int {}".format(name, hist.Integral() ))
   #	hist = dress_histogram(name, hist)	
   #	hist.Draw("same hist")
   leg.Draw("same")

   mainPad.RedrawAxis()

   ###-------- Drawing bottom pad with distributions
   canvas.cd()
   bottomPad = ROOT.TPad("bottompad", "bottompad", 0, 0, 1 ,0.4)
   bottomPad.Draw()
   bottomPad.SetLeftMargin(0.13)
   bottomPad.SetTopMargin(0.05)
   bottomPad.SetBottomMargin(0.3)
   bottomPad.cd()

   #hist_dummy, xmin,xmax = create_dummy(hists["stack"])
   #hist.SetRangeUser()
   hist_dummy.GetYaxis().SetTitle("data/SM")
   #hist_dummy.GetYaxis().SetRangeUser(0., 2.)
   hist_dummy.GetYaxis().SetRangeUser(0., 5.)
   hist_dummy.SetTitle("")

   hist_dummy.GetYaxis().SetTitleSize( title_size)
   hist_dummy.GetYaxis().SetTitleFont( title_font)
   hist_dummy.GetXaxis().SetTitleSize( title_size)
   hist_dummy.GetXaxis().SetTitleFont( title_font)

   hist_dummy.GetYaxis().SetLabelSize( label_size)
   hist_dummy.GetYaxis().SetLabelFont( label_font)

   hist_dummy.GetYaxis().SetTitleOffset(ytitle_offset)
   hist_dummy.GetXaxis().SetTitleOffset(xtitle_offset)


   hist_dummy.Draw()


   #Ratio between data and SM
   r_data_sm = data.Clone("r_data_sm")
   r_data_sm.Divide( stack )
   r_data_sm.SetMarkerStyle(20)
   r_data_sm.SetMarkerSize(0.5)
   r_data_sm.SetMarkerColor(ROOT.kBlack)
   r_data_sm.Draw("same E")

   r_sm = stack.Clone("r_sm")
   r_sm.Divide( stack )
   r_sm.SetFillColor( ROOT.kGray )
   r_sm.SetMarkerColor( ROOT.kGray )
   r_sm.SetMarkerSize( 0 )
   r_sm.Draw("same E2")

   bottomPad.RedrawAxis()

   
   canvas.Print("{}/{}_{}.pdf".format(plot_dir, h_name, event_channel))
