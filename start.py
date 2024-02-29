import subprocess

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
fileSpecs.write("Fabricante del sistema:\t\t\t\t")
