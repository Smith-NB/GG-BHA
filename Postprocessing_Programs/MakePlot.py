#!/usr/bin/env python3

import sys, getopt
import matplotlib.pyplot as plt

def main(argv):
   help_string = 'MakePlot.py [-o] [--options]\n'
   help_string += '\t-h:\tprint this message\n'
   help_string += '\t-s:\tdisplay similarity data\n'
   help_string += '\t\tlong option: --sim\n'
   help_string += '\t-p:\tdisplay probability data\n'
   help_string += '\t\tlong option: --prob\n'
   help_string += '\t-n:\tdisplay new cluster energy data\n'
   help_string += '\t\tlong option: --newE\n'
   help_string += '\t-d:\tdisplay the plot instead of saving it\n'
   help_string += '\t\tlong option: --display\n'
   help_string += '\t-q:\tquality of saved image. Follow arg with int (dpi)\n'
   help_string += '\t\tdefault dpi = 200\n'
   help_string += '\t\tlong option: --quality\n'
   help_string += '\t-f:\tfile name of plot (no file extension).\n'
   help_string += '\t\tdefault name = "plot.png"\n'
   help_string += '\t\tlong option: --filename\n'
   dpi = 200
   display = False
   data_to_plot = {"sim": False, "prob": False, "newE": False, "hopE": False}
   name = "plot.png"
   try:
      opts, args = getopt.getopt(argv,"hspnedq:f:",["sim","prob", "newE", "hopE", "display", "quality=", "filename="])
   except getopt.GetoptError:
      print(help_string)
      sys.exit(2)
   for opt, arg in opts:

      if opt == '-h':
         print(help_string)
         sys.exit()

      elif opt in ("-s", "--sim"):
         sim = open("sim.txt", "r")
         sim_arr = []
         for line in sim:
            sim_arr.append(float(line.rstrip()))
         sim.close()
         data_to_plot["sim"] = True

      elif opt in ("-p", "--prob"):
         prob = open("prob.txt", "r")
         prob_arr = []
         for line in prob:
            prob_arr.append(float(line.rstrip()))
         prob.close()
         data_to_plot["prob"] = True

      elif opt in ("-n", "--newE"):
         if 'new_E_arr' not in locals():
            new_E = open("new_E.txt", "r")
            new_E_arr = []
            for line in new_E:
               new_E_arr.append(float(line.rstrip()))
            new_E.close()
         data_to_plot["newE"] = True

      elif opt in ("-e", "--hopE"):
         if 'new_E_arr' not in locals():
            new_E = open("new_E.txt", "r")
            new_E_arr = []
            for line in new_E:
               new_E_arr.append(float(line.rstrip()))
            new_E.close()
            data_to_plot["hopE"] = True

      elif opt in ("-d", "--display"):
         display = True

      elif opt in ("-q", "--quality"):
         try:
            dpi = int(arg)
         except ValueError:
            print("dpi argument must be an int. Exiting.")
            sys.exit(2)

      elif opt in ("-f", "--filename"):
         name = arg
         if not name.endswith(".png"):
            name += ".png"

   step = open("step.txt", "r")
   curr_E = open("curr_E.txt", "r")
   step_arr = []
   curr_E_arr = []
   for line in step:
      step_arr.append(int(line.rstrip()))
   for line in curr_E:
      curr_E_arr.append(float(line.rstrip()))

   if not data_to_plot["sim"] and not data_to_plot["prob"] and not data_to_plot["hopE"]:
      plt.plot(step_arr, curr_E_arr, color='g', label="Energy of accepted cluster")
      plt.ylabel(r'Energy ($\epsilon$)')  # we already handled the x-label with ax1
      plt.ylim([-174, -160])
      plt.xlabel('Step no.')
      plt.legend()
      if data_to_plot["newE"]:
         plt.plot(step_arr, new_E_arr, color='b', linestyle='None', marker='.', label="Energy of proposed cluster")
   elif data_to_plot["hopE"]:
      hop_E_arr = []
      for a, b in zip(curr_E_arr, new_E_arr):
         hop_E_arr.append(b - a)

      fig, ax1 = plt.subplots()
      ax1.set_xlabel('Step no.')
      ax1.set_ylabel(r'Energy of cluster ($\epsilon$)')
      plt.ylim([-174, -160])
      handles = []
      labels = []

      l1, = ax1.plot(step_arr, curr_E_arr, color='g', label="Energy of accepted cluster")
      handles.append(l1)
      labels.append("Energy of accepted cluster")

      if data_to_plot["newE"]:
         l2, = ax1.plot(step_arr, new_E_arr, color='b', linestyle='None', marker='.', label="Energy of proposed cluster")
         handles.append(l2)
         labels.append("Energy of proposed cluster")

      ax2 = ax1.twinx()
      ax2.set_ylabel(r'Energy of hop ($\epsilon$)') 
      l3, = ax2.plot(step_arr, hop_E_arr, color='#FF8C00', linestyle='None', marker='.', label="Energy of attempted hop")
      handles.append(l3)
      labels.append("Energy of attempted hop") 

      ax2.legend(loc='lower left')
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0 + box.height * 0.1,
                  box.width, box.height * 0.9])
      ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15),
               fancybox=True, shadow=True, ncol=4)
   else:
      fig, ax1 = plt.subplots()
      ax1.set_xlabel('Step no.')
      ax1.set_ylabel(r'Energy ($\epsilon$)')
      plt.ylim([-174, -160])
      handles = []
      labels = []

      l1, = ax1.plot(step_arr, curr_E_arr, color='g', label="Energy of accepted cluster")
      handles.append(l1)
      labels.append("Energy of accepted cluster")

      if data_to_plot["newE"]:
         l2, = ax1.plot(step_arr, new_E_arr, color='b', linestyle='None', marker='.', label="Energy of proposed cluster")
         handles.append(l2)
         labels.append("Energy of proposed cluster")
      ax2 = ax1.twinx()

      ax2.set_ylabel("Percentage")
      plt.ylim([0, 100])
      if data_to_plot["sim"]:
         l3, = ax2.plot(step_arr, sim_arr, color='r', linestyle='None', marker='.', label='Similarity')
         handles.append(l3)
         labels.append("Similarity")
      if data_to_plot["prob"]:
         l4, = ax2.plot(step_arr, prob_arr, color='#800080', linestyle='None', marker='.', label='Probability')
         handles.append(l4)
         labels.append("Probability")

      ax2.legend(loc='lower left')
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0 + box.height * 0.1,
                  box.width, box.height * 0.9])
      ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15),
               fancybox=True, shadow=True, ncol=4)
   if display:
      plt.show()
   else:
      plt.savefig(name, dpi=dpi)
if __name__ == "__main__":
   main(sys.argv[1:])