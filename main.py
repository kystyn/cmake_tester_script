import subprocess
import os

testAddr = 'git@github.com:kystyn/cmake_tester.git'
testDir = 'test'

studentAddr = 'git@github.com:kystyn/cmake_student.git'
studentDir = 'student'

buildDir = 'build'

generatorCMakeParam = 'Ninja'
generator = 'ninja'

def updateRepo( repoAddress, repoDir ):
    base = os.path.abspath(os.curdir)
    if not os.path.exists(repoDir):
        os.mkdir(repoDir)
        os.chdir(repoDir)
        subprocess.run(["git init"], shell = True)
        subprocess.run(["git remote add origin " + repoAddress], shell = True)
        subprocess.run(["git pull origin master"], shell = True)
    else:
        os.chdir(repoDir)
        subprocess.run(["git pull origin master"], shell = True)
    os.chdir(base)

# root and is relative to current file
def build( root, target ):
    base = os.path.abspath(os.curdir)
    os.chdir(root)
    if not os.path.exists(target):
        os.mkdir(target)
    subprocess.run(["cmake -B " + target + " -G " + generatorCMakeParam], shell = True)
    os.chdir(target)
    subprocess.run([generator], shell = True)
    os.chdir(base)

def includeTests():
    base = os.path.abspath(os.curdir)
    print(base)
    cmakefile = open(studentDir + '/CMakeLists.txt', 'a')
    cmakefile.write('include(' + base + '/' + testDir + '/CMakeLists.txt)')
    cmakefile.close()

def clear():
    base = os.path.abspath(os.curdir)
    os.chdir(studentDir)
    subprocess.run(["git stash"], shell = True)
    os.chdir(base + '/' + testDir)
    subprocess.run(["git stash"], shell=True)
    os.chdir(base)

def test( pathToExecutable, log ):
    base = os.path.abspath(os.curdir)
    os.chdir(pathToExecutable)
    subprocess.run(["ctest -O " + log], shell = True)
    os.chdir(base)

def main():
    updateRepo(testAddr, testDir)
    updateRepo(studentAddr, studentDir)
    includeTests()
    build(studentDir, buildDir)
    test(studentDir + '/' + buildDir, "log.txt")
    clear()

main()