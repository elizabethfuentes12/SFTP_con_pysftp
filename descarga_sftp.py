import pysftp
import zipfile
import os
import shutil

import pandas as pd

myHostname = "myHostname"
myUsername = "usuario"
myPassword = "contraseña"

#Esta funcion navega en un directorio y encuentra la carpeta con el nombre que le interesa en sub-carpeta

carpeta="tipo_carpeta"
subcarpeta="202004"

#Esta funcion 

def leer_SFTP(myHostname,myUsername,myPassword,carpeta,subcarpeta):
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("OK: conexion exitosa")
        # Selecciona la carpeta en la cual quieres navegar
        sftp.cwd(carpeta)
        # informa el directorio al cual quieres acceder Obtain structure of the remote directory '/var/www/vhosts'
        directory_structure = sftp.listdir()
       
    
        for attr in directory_structure:
            #Puedes imprimir la estructura  en el caso de que quieras conocerlo
            #print (attr.filename, attr)

            if (attr.find(subcarpeta))!=-1:
                tree=carpeta+str(attr)
                print(tree)
                print("OK:Lectura carpetas")

                #Ahora la descarga
                sftp.cwd(tree)
                directory_structure = sftp.listdir()
                for doc in directory_structure:
                    #print (attr.filename, attr)
                    if (doc.find("Reportes OLT diario - Local Reports"))!=-1:
                        localFilePath=doc
                        print(localFilePath)

                remoteFilePath = tree+"/"+localFilePath
                print(remoteFilePath)
                sftp.get(remoteFilePath, localFilePath)
                print("OK: Descarga",localFilePath)
                procesa_archivo(localFilePath,str(attr))
            print("OK: Mes",attr)

def descargar_SFTP(myHostname,myUsername,myPassword,carpeta):
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection succesfully stablished ... ")
        sftp.cwd(carpeta)
        directory_structure = sftp.listdir()
        for attr in directory_structure:
            #print (attr.filename, attr)
            if (attr.find("Reportes OLT diario - Local Reports"))!=-1:
                localFilePath=attr

        # Define the file that you want to download from the remote directory
        remoteFilePath = carpeta+localFilePath

        # Define the local path where the file will be save
        sftp.get(remoteFilePath, localFilePath)
        print("OK: Descarga",localFilePath)
        return localFilePath

#Un plus en el caso de que el archivo sea .zip

def procesa_archivo(localFilePath,mes):
    # open and extract all files in the zip
    password = None
    z = zipfile.ZipFile(localFilePath, "r")
    try:
        z.extractall(pwd=password)
    except:
        print('Error')
        pass
    
    print("OK: UNZIP")
    z.close()
    os.remove(localFilePath)