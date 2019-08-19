import subprocess
import os
import json

testAddr = 'git@github.com:kystyn/cmake_tester.git'
testDir = 'test'

studentAddr = 'git@github.com:kystyn/cmake_student.git'
studentDir = 'student'

buildDir = 'build'

generatorCMakeParam = 'Ninja'
generator = 'ninja'

packageName = 'lesson'

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

def parseLog( pathToExecutable, logName ):
    base = os.path.abspath(os.curdir)
    os.chdir(pathToExecutable)
    log = open(logName, 'rt')

    testNo = 1
    testRes = {}
    nestedException = []
    for string in log:
        found = string.find('Test #' + str(testNo))
        if found != -1:
            testNo += 1
            splittedStr = string.split()
            curTestName = splittedStr[3]

            if string.find('Passed') != -1:
                curTestRes = True
            else:
                curTestRes = False
                nestedException.append(''.join([splittedStr[i] + ' ' for i in range(5, len(splittedStr))]))
            testRes.update({curTestName: curTestRes})

    os.chdir(base)
    return [testRes, nestedException]

# parseRes == [testRes, nestedException]
def genJson( fileName, parseRes ):
    outJson = {"data": []}
    outF = open(fileName, 'wt')

    failMsgNum = 0
    for testRes in parseRes[0].items():
        str = {
            "packageName": packageName,
            "methodName": testRes[0],
            "tags": [],
            "results": [{
                "status": "SUCCESSFUL" if testRes[1] else "FAILED",
                "failure": parseRes[1][failMsgNum] if not testRes[1] else None
            }]
        }
        failMsgNum += int(not testRes[1])
        outJson['data'].append(str)
    outF.write(json.dumps(outJson, indent = 4))
    outF.close()

def main():
    updateRepo(testAddr, testDir)
    updateRepo(studentAddr, studentDir)
    includeTests()
    build(studentDir, buildDir)
    test(studentDir + '/' + buildDir, "log.txt")
    parseRes = parseLog(studentDir + '/' + buildDir, "log.txt")
    genJson("test_result.json", parseRes)
    clear()

main()