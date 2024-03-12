import subprocess

def shellCMD(CMD):
        #outcommand = subprocess.run([shellCMD], stdout=subprocess.PIPE).stdout.decode("utf-8")
        outcommand = subprocess.run(CMD, shell=True, capture_output=True, text=True)
        print(outcommand.stdout)
        return outcommand.stdout


hostnamectlText = shellCMD("hostnamectl")
hostnamectlTextLines = hostnamectlText.split('\n')
for line in hostnamectlTextLines:
    if "Architecture" in line:
        hardwareVendor = line.split(":")
        print (hardwareVendor[1].strip())
    else:
        hardwareVendor = "No"
        print(hardwareVendor)