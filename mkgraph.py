#!/usr/bin/env python

import sys, os.path, time, rrdtool
from pysnmp.entity.rfc3413.oneliner import cmdgen

def main(host,port,community,oid):

    cg = cmdgen.CommandGenerator()
    comm_data = cmdgen.CommunityData('test', community)
    transport = cmdgen.UdpTransportTarget((host, int(port)))
    errInd, errStatus, errIdx, result = cg.getCmd(comm_data, transport, oid)

    if not errInd and not errStatus:
        rrdfile = "./example.rrd"
        exists = os.path.exists(rrdfile)
        if exists == False:
            rrdtool.create(rrdfile,
                "DS:laLoad1:GAUGE:600:U:U",
                "RRA:AVERAGE:0.5:1:288",
                "RRA:AVERAGE:0.5:6:336",
                "RRA:AVERAGE:0.5:12:720",
                "RRA:AVERAGE:0.5:288:1000",
                "RRA:MAX:0.5:1:288",
                "RRA:MAX:0.5:6:336",
                "RRA:MAX:0.5:12:720",
                "RRA:MAX:0.5:288:1000",
                "RRA:MIN:0.5:1:288",
                "RRA:MIN:0.5:6:336",
                "RRA:MIN:0.5:12:720",
                "RRA:MIN:0.5:288:1000",)

        print result[0][1]
        rrdtool.update(rrdfile, "%d:%f" % ( int(time.time() ), float(result[0][1].prettyPrint()) ))

        rrdtool.graph ("./example.png",
            "--title", "Load",
            "DEF:data=%s:laLoad1:AVERAGE" % rrdfile,
            "AREA:data#ff6600",
            "--vertical-label=Load Average",
            "-l 0",
            "-u 2.0",
            "-r",
            "--color", "BACK#000000",
            "--color", "CANVAS#000000",
            "--color", "FONT#ffffff",
            "--color", "GRID#ffffff",
            "--color", "MGRID#ffffff",
            "--color", "ARROW#ffffff",
            "GPRINT:data:AVERAGE:AVERAGE %lf %s\l",
            "LINE1:1.0#00ff00:1.0 Warning Level",
            "LINE1:2.0#ff0000:2.0 Critical Level",)

if __name__ == '__main__':

    argvs = sys.argv
    argc = len(argvs)
    if (argc != 5):
        print 'Usage: You should specify 3 parameters to %s' % argvs[0]
        print '1: host name'
        print '2: port number'
        print '3: community name'
        print '4: oid'
        quit()

    main(argvs[1], argvs[2], argvs[3], argvs[4])
