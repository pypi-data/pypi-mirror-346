import os
import shutil

from modulitiz_micro.ModuloColorText import ModuloColorText
from modulitiz_micro.ModuloListe import ModuloListe
from modulitiz_micro.files.ModuloFiles import ModuloFiles
from modulitiz_micro.sistema.ModuloSystem import ModuloSystem
from modulitiz_micro.util.wheel.ModuloCheckTestNamingConvention import ModuloCheckTestNamingConvention
from modulitiz_micro.util.wheel.ModuloToml import ModuloToml
from modulitiz_micro.files.git.ModuloGit import ModuloGit


class ModuloBuildWheel(object):
	CMD_PYTHON="python"
	PATTERN_NOMEFILE_WHEEL="{}-{}-{}-none-any.whl"
	MAX_VERSION_TO_KEEP=10
	
	def __init__(self,moduleName:str,percorsoFileMain:str):
		self.moduleName=moduleName
		self.moduleNameNormalized=moduleName.replace("_","-")
		
		self.percorsoCartellaSource=os.path.dirname(percorsoFileMain)
		self.percorsoCartellaRoot=os.path.dirname(self.percorsoCartellaSource)
		self.git=ModuloGit(os.path.dirname(self.percorsoCartellaRoot))
		self.skipUnitTest=False
		
		self.moduloToml=ModuloToml("pyproject.toml")
		self.moduloTestNamingConventions=ModuloCheckTestNamingConvention(moduleName,self.percorsoCartellaSource)
		self.versionOld=None
		self.versionNew=None
		self.filenameWheel=None
	
	def doWork(self):
		self.versionOld=self.moduloToml.retrieveVersion()
		self.skipUnitTest=input("Skip unit test? y, n (default = n):")=='y'
		# chiedo quale versione aumentare (major, minor, bug fix)
		versionType=input("Which version increment? 1=major, 2=minor, 3=bug fix (default = 2):")
		if versionType=="":
			versionType=2
		else:
			versionType=int(versionType)
		# calcolo la prossima versione
		self.__computeVersionNew(versionType)
		# stampo info
		msg=f"Build {self.moduleName} {self.versionNew}"
		ModuloSystem.setTitoloFinestra(msg)
		print("""{}
		============================================================
				{} (from version {})
		============================================================
		{}""".format(ModuloColorText.GRASSETTO,msg,self.versionOld,ModuloColorText.DEFAULT))
		# cambio cartella
		os.chdir(self.percorsoCartellaSource)
		if self.__doUnitTests() is True:
			return
		# aggiorno versione
		self.moduloToml.updateVersion(self.versionNew)
		# costruisco wheel
		ModuloSystem.systemCallPrintOutput(f'{self.CMD_PYTHON} -m pip install -U build twine==6.0.1',None)
		print()
		percorsoCartellaOut=os.path.dirname(self.percorsoCartellaRoot)
		percorsoCartellaOut=ModuloFiles.pathJoin(ModuloFiles.pathJoin(percorsoCartellaOut,"wheels"),self.moduleNameNormalized)
		cmd='{} -m build --wheel --outdir "{}"'.format(self.CMD_PYTHON,percorsoCartellaOut)
		ModuloSystem.systemCallPrintOutput(cmd,None)
		print()
		# cancello cartelle temporanee
		shutil.rmtree(ModuloFiles.pathJoin(self.percorsoCartellaSource,"build"))
		shutil.rmtree(ModuloFiles.pathJoin(self.percorsoCartellaSource,self.moduleName+".egg-info"))
		# installo wheel
		self.filenameWheel=self.PATTERN_NOMEFILE_WHEEL.format(self.moduleName,self.versionNew,self.moduloToml.retrieveMinPyVersion())
		percorsoWheel=ModuloFiles.pathJoin(percorsoCartellaOut,self.filenameWheel)
		cmd='{} -m pip install -U "{}"'.format(self.CMD_PYTHON,percorsoWheel)
		ModuloSystem.systemCallPrintOutput(cmd,None)
		print()
		# aggiungo il file al repo
		self.git.inner.index.add(percorsoWheel)
		# se presenti, cancello le versioni troppo vecchie
		print()
		oldFilenames=ModuloListe.humanOrder(os.listdir(percorsoCartellaOut))[:-self.MAX_VERSION_TO_KEEP]
		if len(oldFilenames)==0:
			return
		print("Cancello le versioni troppo vecchie:")
		for file in oldFilenames:
			deletedFilename=self.git.inner.index.remove(ModuloFiles.pathJoin(percorsoCartellaOut,file),working_tree=True)
			print("\n".join(deletedFilename))
		print("Uploading to Pypi")
		cmd='{} -m twine upload "{}"'.format(self.CMD_PYTHON,percorsoWheel)
		ModuloSystem.systemCallPrintOutput(cmd,None)
	
	def __doUnitTests(self) -> bool:
		if self.skipUnitTest is True:
			return False
		nomefileTest=ModuloFiles.pathJoin(self.percorsoCartellaSource,"test/TestMain.py")
		print("Check file and class naming conventions...")
		errors=self.moduloTestNamingConventions.doWork()
		if not ModuloListe.isEmpty(errors):
			errorsCount=len(errors)
			print("There %s %d error%s:"%("are" if errorsCount>1 else "is",errorsCount,"s" if errorsCount>1 else ""))
			for error in errors:
				print(error)
			return True
		print("Starting tests...")
		cmd='%s "%s"'%(self.CMD_PYTHON,nomefileTest)
		rows=[]
		for row in ModuloSystem.systemCallYieldOutput(cmd,None):
			print("%s>>>%s %s"%(ModuloColorText.BLU,ModuloColorText.DEFAULT,row))
			rows.append(row)
		rows=reversed(rows[-10:])
		rows=[x.strip() for x in rows]
		rows=[x if x!="" and x!=ModuloColorText.DEFAULT else None for x in rows]
		rows=ModuloListe.eliminaElementiVuoti(rows)
		lastRow=rows[0]
		PATTERN_TO_PRINT="""{}
	==================================================
			{}
	==================================================
	"""+ModuloColorText.DEFAULT
		if lastRow!="OK":
			print(PATTERN_TO_PRINT.format(ModuloColorText.ROSSO,"ERRORE nei test"))
			return True
		print(PATTERN_TO_PRINT.format(ModuloColorText.VERDE,"test completati con successo"))
		return False
	
	def __computeVersionNew(self,versionType:int):
		arr=[int(x) for x in self.versionOld.split(".")]
		arr[versionType-1]+=1
		if versionType!=len(arr):
			for i in range(versionType,len(arr)):
				arr[i]=0
		arr=[str(x) for x in arr]
		self.versionNew=".".join(arr)
