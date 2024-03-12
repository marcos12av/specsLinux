import subprocess

class linuxSpec:

    def getOS(self):
        lineTextOS = (subprocess.run(["lsb_release", "-d"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
        splitLineTextOS = lineTextOS.split()
        os = " ".join(splitLineTextOS[1:])
        return os
    
    def getHostnameData(self, keyword):
        hostnamectlText = self.shellCMD("hostnamectl")
        hostnamectlTextLines = hostnamectlText.split('\n')
        for line in hostnamectlTextLines:
            if keyword in line:
                hardwareVendor = line.split(":")
                return hardwareVendor[1].strip()
            else:
                hardwareVendor = " "
                return hardwareVendor
    
    def shellCMD(self, shellCMD):
        outcommand = subprocess.run([shellCMD], stdout=subprocess.PIPE).stdout.decode("utf-8")
        return outcommand
    
systemOS = linuxSpec()

fileSpecs = open("specs.txt", "a")
fileSpecs.write("Características Generales\n")
fileSpecs.write("Nombre de host:\t\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("hostname"))
fileSpecs.write("Versión del sistema operativo:\t\t\t\t")
fileSpecs.write(systemOS.getOS() + "\n")
fileSpecs.write("Dirección IP:\t\t\t\t\t\t\t\t")
cmd = "\"hostname\", \"-I\""
print(cmd)
print("\n")
fileSpecs.write(systemOS.shellCMD(cmd))

fileSpecs.write("Versión base del kernel:\t\t\t\t\t")
fileSpecs.write(subprocess.run(["uname", "-sr"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
fileSpecs.write("Versión del kernel:\t\t\t\t\t\t\t")
fileSpecs.write(subprocess.run(["uname", "-vmo"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
fileSpecs.write("Fecha de instalación original:\t\t\t\t")
command = "ls -lct --time-style=long /etc | tail -1 | awk '{print $6, $7}'"
outcommand = subprocess.run(command, shell=True, capture_output=True, text=True)
fileSpecs.write(outcommand.stdout)
fileSpecs.write("Fabricante del sistema:\t\t\t\t\t\t")
fileSpecs.write(getHostnameData("Hardware Vendor"))
fileSpecs.write("\n")
fileSpecs.write("Modelo el sistema:\t\t\t\t\t\t\t")
fileSpecs.write(getHostnameData("Hardware Model"))
fileSpecs.write("\n")
fileSpecs.write("Tipo de sistema:\t\t\t\t\t\t\t")
fileSpecs.write(getHostnameData("Architecture"))
fileSpecs.write("\n")
fileSpecs.write("Procesador(es) virtual(es):\t\t\t\t\t")
fileSpecs.write(subprocess.run(["nproc"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
fileSpecs.write("Versión del BIOS:\t\t\t\t\t\t\t")
fileSpecs.write(subprocess.run(["dmidecode", "-s", "bios-version"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
#### Salto para pruebas
fileSpecs.write("\n")
# Get disks number and unids label

def diskInfo (diskProperty, diskText):
    textLineDisk = []
    findText = None

    # lsblk detect disks and save disks and partitions in arrays
    outcommand = subprocess.run("lsblk", stdout=subprocess.PIPE).stdout.decode("utf-8")
    outcommandlines = outcommand.split('\n')
    for linedisk in outcommandlines:
            if "disk" in linedisk:
                diskIndice = outcommandlines.index(linedisk) + 1
                diskContentList = []
                diskContentList.append(linedisk)
                for linesubdisk in outcommandlines[diskIndice:]:
                    if "disk" in linesubdisk:
                        break
                    else:
                        diskContentList.append(linesubdisk)
                textLineDisk.append(diskContentList)

    # Find disk property and return then
    for disk in textLineDisk:
        for diskSection in disk:
            if diskProperty in diskSection:
                diskSectionSplitText = disk[0].split(" ")
                diskPath = "/dev/" + diskSectionSplitText[0] + diskText
                return diskPath
     
textDisk = str(len(textLineDisk)) + ' unidades\n'

fileSpecs.write("Discos duros virtuales:\t\t\t\t\t\t")
fileSpecs.write(textDisk)
fileSpecs.write("Ubicación de discos en host:\t\t\t\t\n")
fileSpecs.write("Unidades lógicas de almacenamiento:\t\t\t")
fileSpecs.write(textDisk)
 

textDiskSO = "\t\t\t\t\t\t\t\t\t\t\t" + diskInfo("boot", " para SO") + "\n"
fileSpecs.write(textDiskSO)

testDiskCache = "\t\t\t\t\t\t\t\t\t\t\t" + diskInfo("/var/cache/ecarto", " para caché de mapas") + "\n"
fileSpecs.write(testDiskCache)
fileSpecs.write("Particionado del sistema (LVM):\t\t\t")

fileSpecs.write(textDiskSO)