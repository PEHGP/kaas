#!/usr/bin/env python
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2,urllib,re,time,getopt,sys,BeautifulSoup,os
class CurlWeb:
	def __init__(self,Key,Mail="ngsplatform@163.com",jobid="no",ResultFileName="Results"):
		self.fungi="sce, ago, kla, ppa, vpo, cgr, dha, pic, lel, cal, yli, ncr, mgr, fgr, ssl, bfu, ani, afm, aor, ang, pcs, cpw, ure, tml, spo, cne, ppl, mpr, uma, mgl, ecu"
		self.gene="hsa, dme, cel, ath, sce, cho, eco, nme, hpy, rpr, bsu, lla, cac, mge, mtu, ctr, bbu, syn, bth, dra, aae, mja, ape"
		self.euk="hsa, mmu, rno, dre, dme, cel, ath, sce, ago, cal, spo, ecu, pfa, cho, ehi, eco, nme, hpy, bsu, lla, mge, mtu, syn, aae, mja, ape"
		self.pro="hsa, dme, ath, sce, pfa, eco, sty, hin, pae, nme, hpy, rpr, mlo, bsu, sau, lla, spn, cac, mge, mtu, ctr, bbu, syn, aae, mja, afu, pho, ape"
		self.Mail=Mail
		self.jobid=jobid
		self.ResultFileName=ResultFileName
		self.Key=Key
	def CurlKaas(self,FastaFile,MissionName,Org,Way,Type):
		#self.ResultFileName=ResultFileName
		#self.Mail=Mail
		#self.jobid="no"
		register_openers() #must need
		if Type=="p":
			datagen, headers = multipart_encode({"file": open(FastaFile,"rb"),"uptype":"q_file","qname":MissionName,"mail":self.Mail,"dbmode":"manual","org_list":Org,"way":Way,"mode":"compute"})
		elif Type=="n":
			datagen, headers = multipart_encode({"file": open(FastaFile,"rb"),"peptide2":"n","uptype":"q_file","qname":MissionName,"mail":self.Mail,"dbmode":"manual","org_list":Org,"way":Way,"mode":"compute"})
		request = urllib2.Request("http://www.genome.jp/kaas-bin/kaas_main/kaas_main", datagen, headers)
		fd=urllib2.urlopen(request)
		for x in fd.readlines():
			x=x.rstrip()
			print x
			m=re.search("job ID:(.*?)</p>",x)
			if m:
				self.jobid=m.group(1).replace(" ","")
				flag=1
				#print self.jobid
				#if not self.jobid:
				#	print "web can't submit data."
				#	sys.exit()
		print self.jobid
	def GetKaasResults(self):
		if not os.path.exists("map"):
			os.mkdir("map")
		urllib2.urlopen("http://www.genome.jp/kaas-bin/kaas_main?mode=brite&id=%s&mail=%s&key=%s"%(self.jobid,self.Mail,self.Key))
		#BRITE hierarchies
		Fc=open(self.ResultFileName+"_KEGG_Orthology.keg","w")
		Fc.write(urllib2.urlopen("http://www.genome.jp/kegg-bin/download_htext?htext=q00001.keg&format=htext&filedir=/tools/kaas/files/log/result/%s"%self.jobid).read())
		Fc.close()
		Fc=open(self.ResultFileName+"_KEGG_modules.keg","w")
		Fc.write(urllib2.urlopen("http://www.genome.jp/kegg-bin/download_htext?htext=q00002.keg&format=htext&filedir=/tools/kaas/files/log/result/%s"%self.jobid).read())
		Fc.close()
		Fc=open(self.ResultFileName+"_KEGG_reaction_modules.keg","w")
		Fc.write(urllib2.urlopen("http://www.genome.jp/kegg-bin/download_htext?htext=q00003.keg&format=htext&filedir=/tools/kaas/files/log/result/%s"%self.jobid).read())
		Fc.close()
		l=urllib2.urlopen("http://www.genome.jp/kaas-bin/kaas_main?mode=map&id=%s&mail=%s&key=%s"%(self.jobid,self.Mail,self.Key)).read()#need change
		#print l
		Fq=open("map/query.ko","w")
		Fq.write(urllib2.urlopen("http://www.genome.jp/tools/kaas/files/dl/%s/query.ko"%self.jobid).read())
		Fq.close()
		fr=open(self.ResultFileName+".stat","w")
		#print l
		p=re.compile("<input type=\"hidden\" name=\"unclassified\" value=\"(.*?)\">",re.S) #match
		m=p.search(l)
		k=m.group(1)
		#print k
		register_openers()
		datagen, headers = multipart_encode({"org_name":"ko","sort":"pathway","default":"#bfffbf","reference":"white","unclassified":k})
		request = urllib2.Request("https://www.genome.jp/kegg-bin/color_pathway_object", datagen, headers)
		fd=urllib2.urlopen(request).readlines()
		#print fd
		self.PathWayUrlList=[]
		for x in fd:
			x=x.rstrip()
			if "show_pathway" in x:
				soup=BeautifulSoup.BeautifulSoup(x)
				l=soup.findAll("a")
				fr.write("#"+l[0].text+" "+x.split("</a>")[1].split("&nbsp;")[0]+"\t"+l[1].text+"\n")
				PngName=l[0].get('href').split("/")[-1].split(".")[0]
				self.PathWayUrlList.append(["http://www.genome.jp"+l[0].get('href'),PngName])
			elif "_bget" in x:
				soup=BeautifulSoup.BeautifulSoup(x)
				l=soup.findAll("a")
				fr.write(l[0].text+"\t"+x.split("</a>")[1].strip()+"\n")
		fr.close()
	def GetPathWayImage(self):
		red={}
		for u in self.PathWayUrlList:
			PathWay=urllib2.urlopen(u[0]).read()
			psoup=BeautifulSoup.BeautifulSoup(PathWay)
			for I in psoup.findAll("img"):
				iu=I.get("src")
				#print iu
				if u[1] in iu:
					ImgUrl=iu
					break
			#print ImgUrl
			try:
				temp=red[ImgUrl]
			except:
				red[ImgUrl]=0
				Fpng=open("map/"+u[1]+".png","w")
				try:
					Fpng.write(urllib2.urlopen("http://www.genome.jp"+ImgUrl).read())
				except:
					print ImgUrl
				Fpng.close()
	def FormatResults(self):
		fg=open(self.ResultFileName+".gmt","w")
		fc=open(self.ResultFileName+".stat.change","w")
		#os.system("tar -xzvf %s"%(self.ResultFileName+".tar.gz"))
		dg={}
		dd={}
		for x in open("map/query.ko"):
			x=x.rstrip()
			l=x.split("\t")
			if len(l)>1:
				if not l[1] in dg:
					dg[l[1]]=[l[0]]
				else:
					dg[l[1]].append(l[0])
		for x in open(self.ResultFileName+".stat"):
			x=x.rstrip()
			m=re.search("^#",x)
			if not m:
				l=x.split("\t")
				p=l[0].split(":")[1]
				#dd[p]=l[1]
				dd[pa].append(p)
				fc.write(l[0]+"\t"+",".join(dg[p])+"\t"+l[1]+"\n")
			else:
				fc.write(x+"\n")
				pa=x.split("\t")[0].replace("#","").replace(" ","_")
				dd[pa]=[]
		for x in dd:
			print x,len(dd[x])
			l=x.split("__")
			g=[]
			for y in dd[x]:
				g+=dg[y]
			fm=l[1]+"\t"+l[0]+"\t"+"\t".join(g)
			fg.write(fm+"\n")
		fc.close()
		fg.close()
		dfg={}
		dfgn={}
		for x in open(self.ResultFileName+".stat.change"):
			x=x.rstrip()
			if x.startswith("#"):
				continue
			l=x.split("\t")
			for g in l[1].split(","):
				if not g in dfg:
					dfg[g]=[]
				if not g in dfgn:
					dfgn[g]=[]
				#print l
				if ";" in l[2]:
					dfg[g].append(l[0].split(":")[1]+":"+l[2].split(";")[1])
					dfgn[g].append(l[2].split(";")[0])
				else:
					dfg[g].append(l[0].split(":")[1]+":"+l[2])
					dfgn[g].append("-")
		fgn=open(self.ResultFileName+"_gene.xls","w")
		fgn.write("gene\tabbreviation\tdescription\n")
		for g in dfg:
			fm=g+"\t"+";".join(list(set(dfgn[g])))+"\t"+";".join(list(set(dfg[g])))
			fgn.write(fm+"\n")
		fgn.close()
	def StatisticsLevelB(self,FileQ):
		Fr=open(FileQ.split(".")[0]+"_levelB.xls","w")#need change
		Fr.write("Category\tnum\n")
		d={}
		dl=[]
		for x in open(FileQ):
			x=x.rstrip()
			if x.startswith("B"):
				m=re.search("<b>(.*)</b>",x)
				if m:
					#print m.group(1)
					term=m.group(1)
					dl.append(term)
					d[term]=[]
			if x.startswith("D"):
				l=x.split()
				d[term].append(l[1])
		for x in dl:
			Fr.write(x+"\t"+str(len(set(d[x])))+"\n")
		Fr.close()
if __name__=="__main__":
	def KaasOption():
		print "\n-h\thelp"
		print "-f\tfasta file #!!"
		print "-n\tMission name DF:query"
		print "-m\tE-mail DF:ngsplatform@163.com"
		print "-l\torganisms list(fungi,gene,euk,pro) DF:fungi"
		print "-w\tAssignment method(b:BBH(bi-directional best hit),s:SBH(single-directional best hit)) DF:b"
		print "-g\tcustom organisms list file(opt)"
		print "-t\tprotein or nucleic(p,n) DF:p"
		print "-o\toutput file DF:results"
		print "--justformat\tjust do format result.gmt and result.stat.change,not do kegg(y,n) DF:n\n"
		print "example:kaas.py -f t.fasta -t p -n test -m test@126.com -l fungi -w b --justformat n -o test\n\n\tkaas.py -f t.fasta -t p -n test -m test@126.com -g org.txt -w b --justformat n -o test\n\njust do format:kaas.py --justformat y -o result\n"
		print "Note:custom organisms list file must have one line like this:hsa, dme, cel, ath\n\n\tthe final result are test.stat, test.tar.gz,test.gmt,test.stat.change\n"
		sys.exit()
	try:
		options,args = getopt.getopt(sys.argv[1:],"hf:n:m:l:g:w:o:t:",["justformat="])
	except getopt.GetoptError:
		KaasOption()
	FastaFile=""
	MissionName="query"
	Email="ngsplatform@163.com"
	Org="fungi"
	Way="b"
	OutPut="results"
	Type="p"
	Format="n"
	for name,value in options:
		if name=="-h":
			KaasOption()
		if name=="-f":
			FastaFile=value
			if not os.path.exists(FastaFile):
				print "File is not exist."
				KaasOption()
			elif os.stat(FastaFile).st_size==0:
				print "File is empty."
				KaasOption()
		elif name=="-n":
			if value!="":
				MissionName=value
		elif name=="-m":
			if value!="":
				Email=value
		elif name=="-l":
			if not value in ["fungi","gene","euk","pro"]:
				print "-l must be gene,euk,pro or fungi"
				KaasOption()
			else:
				Org=value
		elif name=="-g":
			try:
				lf=open(value).readlines()
			except:
				print "can't open %s"%(value)
				KaasOption()
			Org=lf[0].rstrip()
		elif name=="-w":
			if not value in ["b","s"]:
				print "-w must be b or s"
				KaasOption()
			else:
				Way=value
		elif name=="-t":
			if not value in ["p","n"]:
				print "-t must be p or n"
				KaasOption()
			else:
				Type=value
		elif name=="--justformat":
			if value!="":
				Format=value
		elif name=="-o":
			if value!="":
				OutPut=value
	if Format=="y":
		p=CurlWeb(Mail=Email,ResultFileName=OutPut)
		p.FormatResults()
	elif FastaFile and MissionName and Email and Org and Way and OutPut and Type:
		print " ".join(sys.argv)
		p=CurlWeb(Mail=Email,ResultFileName=OutPut)
		if Org=="gene":
			Org=p.gene
		elif Org=="euk":
			Org=p.euk
		elif Org=="pro":
			Org=p.pro
		elif Org=="fungi":
			Org=p.fungi
		p.CurlKaas(FastaFile,MissionName,Org,Way,Type)
		print p.jobid
		p.GetKaasResults()
		p.FormatResults()
		FimageUrl=open("image.url","w")
		for x in p.PathWayUrlList:
			FimageUrl.write(x+"\n") 
		FimageUrl.close()
		p.GetPathWayImage()
	else:
		KaasOption()
