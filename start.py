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
                hostnamePiece = line.split(":")
                return hostnamePiece[1].strip()
            else:
                hostnamePiece = " "
        return hostnamePiece

    def diskArray (self):
        # lsblk detect disks and save disks and partitions in arrays
        textLineDisk = []
        diskCommand = self.shellCMD("lsblk -o NAME,SIZE,MOUNTPOINT,TYPE")
        diskCommandLine = diskCommand.split('\n')
        for linedisk in diskCommandLine:
                if "disk" in linedisk:
                    diskIndice = diskCommandLine.index(linedisk) + 1
                    diskContentList = []
                    diskContentList.append(linedisk)
                    for lineSubDisk in diskCommandLine[diskIndice:]:
                        if "disk" in lineSubDisk:
                            break
                        else:
                            diskContentList.append(lineSubDisk)
                    textLineDisk.append(diskContentList)
        return textLineDisk

    def diskInfo(self, diskProperty, diskText):
        # Find disk property and return then
        for disk in self.diskArray():
            for diskSection in disk:
                if diskProperty in diskSection:
                    diskSectionSplitText = disk[0].split()
                    diskPath = "/dev/" + diskSectionSplitText[0] + diskText
                    return diskPath 
        return "Sin datos"
    
    def diskInfoLVM(self):
        lvmListDisk = []
        for disk in self.diskArray():
            for diskSection in disk:
                lvmDiskInfo = []
                if "disk" in diskSection:
                    partsDisk = diskSection.split()
                    lvmDiskInfo.append(partsDisk[0])
                if "lvm" in diskSection:
                    partsDisk = diskSection.split()
                    lvmDiskInfo.append(partsDisk[0])
                    lvmDiskInfo.append(partsDisk[1])
                    lvmDiskInfo.append(partsDisk[2])
                lvmListDisk.append(lvmDiskInfo)
        return lvmListDisk

    def shellCMD(self, shellCMD):
        outcommand = subprocess.run(shellCMD, shell=True, capture_output=True, text=True)
        return outcommand.stdout
    
systemOS = linuxSpec()

fileSpecs = open("specs.txt", "a")
fileSpecs.write("Características Generales\n")
fileSpecs.write("Nombre de host:\t\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("hostname"))
fileSpecs.write("Versión del sistema operativo:\t\t\t\t")
fileSpecs.write(systemOS.getOS() + "\n")
fileSpecs.write("Dirección IP:\t\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("hostname -I"))
fileSpecs.write("Versión base del kernel:\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("uname -sr"))
fileSpecs.write("Versión del kernel:\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("uname -vmo"))
fileSpecs.write("Fecha de instalación original:\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("ls -lct --time-style=long /etc | tail -1 | awk '{print $6, $7}'"))
fileSpecs.write("Fabricante del sistema:\t\t\t\t\t\t")
fileSpecs.write(systemOS.getHostnameData("Hardware Vendor"))
fileSpecs.write("\n")
fileSpecs.write("Modelo el sistema:\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.getHostnameData("Hardware Model"))
fileSpecs.write("\n")
fileSpecs.write("Tipo de sistema:\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.getHostnameData("Architecture"))
fileSpecs.write("\n")
fileSpecs.write("Procesador(es) virtual(es):\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("nproc"))
fileSpecs.write("Versión del BIOS:\t\t\t\t\t\t\t")
fileSpecs.write(systemOS.shellCMD("dmidecode -s bios-version"))
#### Salto por prueba
fileSpecs.write("\n")
####
textDisk = str(len(systemOS.diskArray())) + ' unidades\n'
fileSpecs.write("Discos duros virtuales:\t\t\t\t\t\t")
fileSpecs.write(textDisk)
fileSpecs.write("Ubicación de discos en host:\t\t\t\t\n")
fileSpecs.write("Unidades lógicas de almacenamiento:\t\t\t")
fileSpecs.write(textDisk)
textDiskSO = "\t\t\t\t\t\t\t\t\t\t\t" + systemOS.diskInfo("boot", " para SO") + "\n"
fileSpecs.write(textDiskSO)
testDiskCache = "\t\t\t\t\t\t\t\t\t\t\t" + systemOS.diskInfo("/var/cache/ecarto", " para caché de mapas") + "\n"
fileSpecs.write(testDiskCache)
fileSpecs.write("Particionado del sistema (LVM):\t\t\t\n")

print(systemOS.diskInfoLVM())