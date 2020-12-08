

SET =['a4i_HV.0', 'a4i_HV.1', 'a4i_CAV.0', 'a4i_HV.2', 'a4i_HV.3', 'a4i_CAV.1', 'a4i_CAV.2', 'a4i_CAV.3', 'a4i_CAV.4', 'a4i_CAV.5']
def find_sequence(lane_result):
	CAV_set = []; HV = [0]; CAV_total = []; HV_total = [];
	count1 = -1; count2 = -1;
	for member in lane_result:
		if member.find('CAV') != -1:
			count2 = 0
			CAV_set.append(member)
			if count1 == 0:
				HV_total.append(HV)
				count1 = 1
		else:
			count1 = 0
			if count2 == 0:
				CAV_total.append(CAV_set)
				CAV_set = []
				count2 = 1
			HV = [member]

	if CAV_set != []:
		CAV_total.append(CAV_set)
	topology = []	
	length = len(HV_total)
	print(CAV_total)
	print(length)
	for x,y in zip(HV_total,CAV_total[-length:]):
		if x == [0]:
			z = y
		else:
			z = x + y
		topology.append(z)

	return topology
## if the first member is CAV, CAV_total[0] == []
## if the first member is HV, H_total[]

if __name__ == '__main__':
	topology = find_sequence(SET)
	print(topology)