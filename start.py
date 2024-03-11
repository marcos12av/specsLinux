import subprocess

def getHostnameData(keyword):
    outcommand = subprocess.run("hostnamectl", stdout=subprocess.PIPE).stdout.decode("utf-8")
    outcommandlines = outcommand.split('\n')
    linekeyword = ""
    for line in outcommandlines:
        if keyword in line:
            linekeyword = line
            hardwareVendor = linekeyword.split(":")
            hardwareVendor = hardwareVendor[1].strip()
            return hardwareVendor
            break
        else:
            hardwareVendor = " "
            return hardwareVendor
    

fileSpecs = open("specs.txt", "a")
fileSpecs.write("Características Generales\n")
fileSpecs.write("Nombre de host:\t\t\t\t\t\t\t\t")
fileSpecs.write(subprocess.run(["hostname"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
fileSpecs.write("Versión del sistema operativo:\t\t\t\t")
sentence = (subprocess.run(["lsb_release", "-d"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
palabras = sentence.split()
os = ""
for x in palabras[1:]:
    os += x + " "
os = os[:-1]
fileSpecs.write(os + "\n")
fileSpecs.write("Dirección IP:\t\t\t\t\t\t\t\t")
fileSpecs.write(subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE).stdout.decode("utf-8"))
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

# Get disks number and unids label
textLineDisk = []
incremental = 0

textLineOsDisk = []
textLinePartitionCache = []

outcommand = subprocess.run("lsblk", stdout=subprocess.PIPE).stdout.decode("utf-8")
outcommandlines = outcommand.split('\n')
valid = None
testDiskCache = ""
textDiskSO = ""
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

for disk in textLineDisk:
    print(disk)           
"""        if valid:
            if "boot" in line:
                lineWordsplit = linekeyword[incremental-1].split(" ")           
                textDiskSO = "/dev/" + lineWordsplit[0] + " para so"
                valid = False
            if "/var/cache/ecarto" in line:
                lineWordsplit = linekeyword[incremental-1].split(" ")
                testDiskCache = "/dev/" + lineWordsplit[0] + " para caché de mapas"
                valid = False
        #Buscar discos en las particiones 
"""        
textDisk = str(len(textLineDisk)) + ' unidades\n'

fileSpecs.write("Discos duros virtuales:\t\t\t\t\t\t")
fileSpecs.write(textDisk)
fileSpecs.write("Ubicación de discos en host:\t\t\t\t\n")
fileSpecs.write("Unidades lógicas de almacenamiento:\t\t\t")
fileSpecs.write(textDisk)
textDiskSO = "\t\t\t\t\t\t\t\t\t\t\t" + textDiskSO + "\n"
fileSpecs.write(textDiskSO)
testDiskCache = "\t\t\t\t\t\t\t\t\t\t\t" + testDiskCache + "\n"
fileSpecs.write(testDiskCache)
fileSpecs.write("Particionado del sistema (LVM):\t\t\t")

fileSpecs.write(textDiskSO)