
import traci 

def write_excel(step,worksheet,begin_step,RouteList,vehicle_store,VehicleSet):
	if step >= begin_step:
		# get all Vehicle's ID
		#get vehicle's  ID which we want
		temp_vehicle = []
		Row_count = int((step - begin_step)*10)
		for VehicleID in VehicleSet:
			JudgeValue = judge_needed(VehicleID,RouteList)
			# 选取从A交叉口西行驶至E交叉口东直行的车辆
			if JudgeValue:    
				temp_vehicle.append(VehicleID)

		for temp_vehicleID in temp_vehicle:
			if temp_vehicleID not in vehicle_store:
				vehicle_store.append(temp_vehicleID)
		#用Vehicle_store 来装路径为特定路径的车辆
		for VehicleID in temp_vehicle:
			travel_distance = traci.vehicle.getDistance(VehicleID)
			worksheet.write(Row_count,vehicle_store.index(VehicleID),travel_distance)


def judge_needed(VehicleID,RouteID):
	specific_route = traci.vehicle.getRoute(VehicleID)  
	print("wwww",specific_route)  
	###得到该车辆的routID和所在车道ID
	if specific_route  ==  RouteID:
		return  True
	else:
		return False
	'''
	#如果车辆的车道ID和RouteID都在我们要求的范围内
	#，可判断此车辆就是我们要跟踪的车辆
	'''