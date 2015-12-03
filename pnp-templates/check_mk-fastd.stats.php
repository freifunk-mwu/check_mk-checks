<?php
# Perfdata
# peers_all=203;;;;
# peers_online=113;;;;
# peers_ipv4=107;;;;
# peers_ipv6=6;;;;
# uptime=92461545;;;;

$vertical_label_name = "Count";

#
# Peer Graph
#
$ds_name[1] = 'Fastd peers';
$opt[1]  = "--vertical-label \"$vertical_label_name\" --title \"Fastd peers $hostnam
e $servicedesc\" ";

$def[1]  = "DEF:peers_all=$RRDFILE[1]:$DS[1]:MAX " ;
$def[1] .= "AREA:peers_all#30f060:\"Total  \" " ;
$def[1] .= "GPRINT:peers_all:MIN:\"%4.0lf %s min \" ";
$def[1] .= "GPRINT:peers_all:LAST:\"%4.0lf %s last \" ";
$def[1] .= "GPRINT:peers_all:AVERAGE:\"%4.0lf %s avg \" ";
$def[1] .= "GPRINT:peers_all:MAX:\"%4.0lf %s max\\n\" ";

$def[1] .= "DEF:peers_online=$RRDFILE[2]:$DS[2]:MAX " ;
$def[1] .= "AREA:peers_online#3060f0:\"Online \" " ;
$def[1] .= "GPRINT:peers_online:MIN:\"%4.0lf %s min \" ";
$def[1] .= "GPRINT:peers_online:LAST:\"%4.0lf %s last \" ";
$def[1] .= "GPRINT:peers_online:AVERAGE:\"%4.0lf %s avg \" ";
$def[1] .= "GPRINT:peers_online:MAX:\"%4.0lf %s max \\n\" ";


#
# Protocol Graph
#
$ds_name[2] = 'Fastd protocols';
$opt[2]  = "--vertical-label \"$vertical_label_name\" --title \"Fastd protocols $hostname / $servicedesc\" ";

$def[2]  = "DEF:peers_ipv4=$RRDFILE[3]:$DS[3]:MAX " ;
$def[2] .= "AREA:peers_ipv4#FF3300:\"IPv4 \" " ;
$def[2] .= "GPRINT:peers_ipv4:LAST:\"%4.0lf %s last \" ";
$def[2] .= "GPRINT:peers_ipv4:AVERAGE:\"%4.0lf %s avg \" ";
$def[2] .= "GPRINT:peers_ipv4:MAX:\"%4.0lf %s max\\n\" ";

$def[2] .= "DEF:peers_ipv6=$RRDFILE[4]:$DS[4]:MAX " ;
$def[2] .= "CDEF:minus_ipv6=peers_ipv6,-1,* " ;
$def[2] .= "AREA:minus_ipv6#FFFF00:\"IPv6 \" " ;
$def[2] .= "GPRINT:peers_ipv6:LAST:\"%4.0lf %s last \" ";
$def[2] .= "GPRINT:peers_ipv6:AVERAGE:\"%4.0lf %s avg \" ";
$def[2] .= "GPRINT:peers_ipv6:MAX:\"%4.0lf %s max \\n\" ";


#
# Uptime Graph
#
$ds_name[3] = 'Fastd Uptime';
$opt[3]  = "--vertical-label 'Uptime (d)' -l0 --title \"Uptime (time since last daemon reboot)\" ";

$def[3]  = "DEF:uptime=$RRDFILE[5]:$DS[5]:MAX ";
$def[3] .= "CDEF:upt=uptime,86400000,/ ";
$def[3] .= "AREA:upt#80f000:\"Uptime (days)\" ";
$def[3] .= "LINE:upt#408000 ";
$def[3] .= "GPRINT:upt:LAST:\"%7.2lf %s LAST\" ";
$def[3] .= "GPRINT:upt:MAX:\"%7.2lf %s MAX\" ";

?>
