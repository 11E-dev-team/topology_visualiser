import operations as op

pxp = op.start_telnet("172.23.201.115", "32792")
data = op.get_neig_data(pxp)
print(data)
print(op.match_neighbors(data))
