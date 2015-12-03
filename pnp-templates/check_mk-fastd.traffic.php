<?php
# Perfdata
# tx_bytes=183404143448;;;;
# tx_packets=806928766;;;;
# rx_bytes=77587457814;;;;
# rx_packets=469840309;;;;

$unit = "B";
$unit_multiplier = 1;
$base = 1000; // Megabyte is 1000 * 1000

$bandwidth = $MAX[1]  * $unit_multiplier;
$warn      = $WARN[1] * $unit_multiplier;
$crit      = $CRIT[1] * $unit_multiplier;

$scale = 1;
$bwuom = ' ';

$warn      /= $scale;
$crit      /= $scale;
$bandwidth /= $scale;

$vertical_label_name = $bwuom . $unit . "/sec";

$range = min(10, $bandwidth);

$ds_name[1] = 'Fastd traffic';

#
$opt[1] = "--vertical-label \"$vertical_label_name\" -l -$range -u $range -X0 -b 1024 --title \"Fastd Traffic $hostname / $servicedesc\" ";
#$opt[1] = "--title \"Fastd traffic $hostname / $servicedesc\" ";
#
$def[1] =  "DEF:rx_bytes=$RRDFILE[4]:$DS[4]:MAX " ;
$def[1] .= "CDEF:intraffic=rx_bytes,$unit_multiplier,* ";
$def[1] .= "CDEF:inmb=intraffic,$scale,/ ";
$def[1] .= "AREA:inmb#00e060:\"in \" " ;
$def[1] .= "GPRINT:intraffic:LAST:\"%7.1lf %s$unit last \" ";
$def[1] .= "GPRINT:intraffic:AVERAGE:\"%7.1lf %s$unit avg \" ";
$def[1] .= "GPRINT:intraffic:MAX:\"%7.1lf %s$unit max\\n\" ";

$def[1] .= "DEF:tx_bytes=$RRDFILE[1]:$DS[1]:MAX " ;
$def[1] .= "CDEF:outtraffic=tx_bytes,$unit_multiplier,* ";
$def[1] .= "CDEF:minusouttraffic=outtraffic,-1,* ";
$def[1] .= "CDEF:outmb=outtraffic,$scale,/ ";
$def[1] .= "CDEF:minusoutmb=0,outmb,- ";
$def[1] .= "AREA:minusoutmb#0080e0:\"out \" " ;
$def[1] .= "GPRINT:outtraffic:LAST:\"%7.1lf %s$unit last \" ";
$def[1] .= "GPRINT:outtraffic:AVERAGE:\"%7.1lf %s$unit avg \" ";
$def[1] .= "GPRINT:outtraffic:MAX:\"%7.1lf %s$unit max \" ";

?>
