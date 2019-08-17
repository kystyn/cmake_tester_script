import subprocess
import os

testAddr = 'git@github.com:kystyn/cmake_tester.git'
testDir = 'test'

def updateRepo( repoAddress, repoDir ):
    if not os.path.exists(repoDir):
        subprocess.run(["mkdir", repoDir])
        os.chdir(repoDir)
        subprocess.run(["git init"], shell = True)
        subprocess.run(["git remote add origin " + repoAddress], shell = True)
        subprocess.run(["git pull origin master"], shell = True)
    else:
        os.chdir(repoDir)
        subprocess.run(["git pull origin master"], shell = True)
'git@github.com:kystyn/cmake_tester.git'

updateRepo(testAddr, testDir)