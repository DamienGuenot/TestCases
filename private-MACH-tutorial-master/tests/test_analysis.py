import os
import subprocess
import unittest

tutorialDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tutorial/wing/run/")  # Path to current folder
inputfiles_dir = f"{tutorialDir}/INPUT/"  # Path to input files directory
# setupfiles_dir = f"{tutorialDir}/SETUP_files"  # Path to setup files directory


class TestMACHTutorial(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(tutorialDir)
        # define some commands for convenience
        self.mpiCmd = ["mpirun", "-n", f"{self.NPROCS}"]
        self.gridFlag = ["--gridFile", "INPUT/wing_vol_coarsen.cgns"]
        self.optFlag = ["--optOptions", "{'Major iterations limit': 0}"]
        # coarsen the CFD grid once
        os.chdir(inputfiles_dir)
        if not os.path.isfile("wing_vol_coarsen.cgns"):
            subprocess.run(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"], check=True)
        os.chdir(tutorialDir)

    def test_struct_meshing(self):
        subprocess.run(["python", "generate_wingbox.py"], check=True)

    def test_struct_loading(self):
        cmd = ["python", "cl_solve.py"]
        subprocess.run(self.mpiCmd + cmd + self.gridFlag, check=True)

    def test_struct_analysis(self):
        cmd = ["python", "struct_run.py"]
        subprocess.run(self.mpiCmd + cmd, check=True)

    def test_aerostruct_analysis(self):
        cmd = ["python", "as_run.py"]
        subprocess.run(self.mpiCmd + cmd + self.gridFlag, check=True)

    def test_struct_opt(self):
        cmd = ["python", "struct_opt.py", "--noPlot"]
        subprocess.run(self.mpiCmd + cmd + self.optFlag, check=True)

    def test_aerostruct_opt(self):
        # we need self.NPROCS to be even so we can have them split between cruise and maneuver
        self.assertEqual(self.NPROCS % 2, 0)
        cmd = [
            "python",
            "as_opt.py",
            "--npcruise",
            f"{self.NPROCS//2}",
            "--npmaneuver",
            f"{self.NPROCS//2}",
            "--shape",
        ]
        subprocess.run(self.mpiCmd + cmd + self.gridFlag + self.optFlag, check=True)


if __name__ == "__main__":
    unittest.main()
