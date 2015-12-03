def perfometer_check_mk_fastd_peers(row, check_command, perf_data):
    peers_all = float(perf_data[0][1])
    peers_online = float(perf_data[1][1])
    perc_connected = 100.0 * peers_online / peers_all
    return "%.0f%%" % perc_connected, perfometer_linear(perc_connected, "#30ff80")

perfometers["check_mk-fastd.stats"] = perfometer_check_mk_fastd_peers
