import subprocess
import sys
args = sys.argv

dirname = args[1]
initiate_file = args[2]
subprocess.run( ["python3" , "calc_angle_final.py" , initiate_file , dirname + "/angle.csv"] )

subprocess.run(['python3' , 'clustering_final.py' , dirname + "/angle.csv", dirname + "/cluster.pickle"])

subprocess.run(['python3' , 'threshold_final.py' , dirname + '/cluster.pickle' , dirname + '/selected.txt'])