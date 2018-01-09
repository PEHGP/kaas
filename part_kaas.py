#!/usr/bin/env python
import sys
from kaas import CurlWeb
if len(sys.argv)!=5:
	print "part_kaas.py <jobid> <email> <prefix> <key>"
	sys.exit()
jobid=sys.argv[1]
email=sys.argv[2]
prefix=sys.argv[3]
key=sys.argv[4]
p=CurlWeb(key,Mail=email,jobid=jobid,ResultFileName=prefix)
p.GetKaasResults()
p.FormatResults()
p.GetPathWayImage()
p.StatisticsLevelB(prefix+"_KEGG_Orthology.keg")
