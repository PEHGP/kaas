#kaas
[KEGG Automatic Annotation Server](http://www.genome.jp/tools/kaas/) Localization

##Get Started
###Requires
- [python](http://www.python.org/downloads/)>=2.6(not support python3.0)
- python module:[poster](https://pypi.python.org/pypi/poster/0.4);[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

###Install
```
git clone git@github.com:PEHGP/kaas.git
```
if you don't install git.You can download kaas[here](https://github.com/PEHGP/kaas/archive/master.zip).

###How to use   
```
python kaas.py -h

-h	help
-f	fasta file #requires
-n	Mission name Default:query
-m	E-mail #requires
-l	organisms list(fungi,gene,euk,pro) Default:fungi
-w	Assignment method(b:BBH(bi-directional best hit),
		s:SBH(single-directional best hit)) Default:b
-g	custom organisms list file(opt)
-t	protein or nucleic(p,n) Default:p
-o	output file Default:results
--justformat 
just format result.gmt and result.stat.change,not execute kegg(y,n) Default:n

example:

kaas.py -f t.fasta -t p -n test -m test@126.com -l fungi -w b --justformat n -o test

kaas.py -f t.fasta -t p -n test -m test@126.com -g org.txt -w b --justformat n -o test

just do format:kaas.py --justformat y -o result

Note:custom organisms list file must have one line like this:hsa, dme, cel, ath

	the final result are test.stat, test.tar.gz,test.gmt,test.stat.change
```

