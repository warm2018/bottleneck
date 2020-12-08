from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import optparse
import subprocess
import random
import traci
import math
import xlsxwriter
from write_excel import write_excel

from copy import deepcopy

from plexe import Plexe, DRIVER, ACC, CACC, FAKED_CACC, RPM, GEAR, ACCELERATION, SPEED  
#generator(1)
#we need to import python modules from the $SUMO_HOME/tools directory

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
     from sumolib import checkBinary
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")

## Write data to Excel 
workbook = xlsxwriter.Workbook('result/trajectory1.xlsx') 
worksheet = workbook.add_worksheet('test1')
RouteList_left = ('bi', 'a1i_1', 'ci')
RouteList_straight = ("to_a4","a4i","a2o","go_a2")
RouteList = RouteList_left
vehicle_store = []

begin_step = 10
WRITE_EXCEL = True
## Write data to Excel
CACC_space = 10

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


def run(): 
    STEP = 0
    plexe = Plexe()
    traci.addStepListener(plexe)
    StepLength = 0.01
    topology = {}
    while STEP < 400: 
        traci.simulationStep()  
        STEP += StepLength
        if int(STEP*100) % 500 == 0:
            Vehicles_0 = traci.lane.getLastStepVehicleIDs("a1i_1_0")
            #Vehicles_1 = traci.lane.getLastStepVehicleIDs("a1i_1_1")
            #Vehicles_2 = traci.lane.getLastStepVehicleIDs("a1i_1_2")
            #Vehicles_3 = traci.lane.getLastStepVehicleIDs("a1i_1_3")
            #for lane in [Vehicles_0,Vehicles_1,Vehicles_2,Vehicles_3]:
            for lane in [Vehicles_0]:   
                position_result,lane_result = sort_lane(lane)
                platooning_members = find_sequence(lane_result)
                print("&&&&&&&",platooning_members)
                platoon_forming(plexe,platooning_members,topology)
                print("topology",topology)
                print("&&&&&&&",platooning_members)

        if int(STEP*100) % 500 == 0:
            platoon_die(plexe, topology)
            #print("######")
        if STEP >= 20 and WRITE_EXCEL and int(STEP*100) % 10 == 0:
            currentIDList = traci.vehicle.getIDList()
            print('999')
            write_excel(STEP, worksheet, begin_step,RouteList,vehicle_store,currentIDList)
    workbook.close()
    traci.close()
    sys.stdout.flush()


def sort_lane(lane_vehicles):
    position_lane = []
    for Vehicle_ID in lane_vehicles:
        vehicle_position = traci.vehicle.getLanePosition(Vehicle_ID)
        position_lane.append(vehicle_position)
    position_result,lane_result = Sort_two(position_lane, lane_vehicles)
    return position_result,lane_result



def Sort_two(List_a,List_b):##此函数表示将List_b按照List_a顺序排序
    if List_a !=[] and List_b != []:
        Index_number = []
        Listb_sort = []
        # 定义一个中间索引列表以及初始化结果的列表
        A_sort = sorted(List_a,reverse = True)
        ##将A排序
        for index_a in range(len(A_sort)):
            Index_number.append(List_a.index(A_sort[index_a]))
        ##将A排序后的列表对应原列表的索引找出来
        for index_b in Index_number:
            Listb_sort.append(List_b[index_b])
        #按照索引值从需要排序的列表中取出元素，行成一个与a排序后对应的列表
        return A_sort,Listb_sort
    ### 实现两个列表元素对的同步排序
    else: 
        return List_a,List_b

def platoon_forming(plexe,opt_vehicles,topology):
    for i,lane_members in enumerate(opt_vehicles):
        FOllOWERS = []
        position = 1
        if lane_members != []:
            for j,vid in enumerate(lane_members):
                if j == 0: # leaders
                    leader_id = vid
                    cacc_spacing = CACC_space
                    traci.vehicle.setSpeedMode(leader_id, 0)
                    plexe.set_path_cacc_parameters(leader_id, cacc_spacing)
                    '''
                    Sets the parameters for the PATH CACC. If a parameter is set to None,
                    it won't be set and it will keep its current value
                    :param vid: vehicle id
                    :param distance: constant spacing in meters
                    :param xi: damping ratio
                    :param omega_n: bandwidth
                    :param c1: leader data weighting parameter 
                    '''       
                    plexe.set_active_controller(leader_id,ACC)
                    plexe.set_cc_desired_speed(vid,15)
                    plexe.use_controller_acceleration(vid, True)
                else: # following members
                    member = vid
                    traci.vehicle.setSpeedMode(member, 0)
                    plexe.use_controller_acceleration(member, True)
                    #topology[member] = {"front": last_follower,
                    #"leader": leader_id}
                    plexe.set_active_controller(member, CACC)
                    plexe.set_cc_desired_speed(vid,15)
                    plexe.enable_auto_feed(member, True, leader_id,last_follower)
                    plexe.add_member(leader_id, member, position)
                    position += 1
                    FOllOWERS.append(member)
                last_follower = vid
                ## reset followers' parameters
                ## init platoons topology
            platoon_size = len(FOllOWERS) + 1   
            topology[leader_id]  = {"followers": FOllOWERS}



def platoon_die(plexe,topology):
    '''
    because of the bug in plexe ( SUMO can't let vehicle
    die peacefully,and make SUMO gui show a crash
    to let SUMO destroy platoon one by one peacefully,
    we should let the platoon member die one by one to 
    avoid SUMO errors.
    :pram followers: a dictionary which describ the platoon followers exist anywhere
    :pram failure_add: a list which load 
    :pram plexe: plexe API instance
    '''
    topology_temp = deepcopy(topology)

    for leader,inf in topology_temp.items(): 
        #print(topology)
        ##to avoid bug, we should judge this vehicle whether has add to sumo or not
        followers = inf['followers']
        last_follower = 0
        if followers != []:
            last_follower = followers[-1]
        else:
            route = traci.vehicle.getRoute(leader)
            #obtain current edge which the vehicle running nowS
            current_edge = traci.vehicle.getRoadID(leader)
            if current_edge == route[-1]:
                del topology[leader]
            continue

        if last_follower != 0:
            #obtain the platoons' route(consists of edges)
            route = traci.vehicle.getRoute(last_follower)
            #obtain current edge which the vehicle running nowS
            current_edge = traci.vehicle.getRoadID(last_follower)
            if current_edge == route[-1]:
                for followerID in followers:
                    plexe.set_active_controller(followerID,ACC) 
                ## update the topology at the same time
                del topology[leader]


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
     default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options
    # this is the main entry point of this script


if __name__ == "__main__":


    options = get_options()
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    #"--collision.action", "none",
    #"--collision.mingap-factor", "0",
    traci.start([sumoBinary, "-c", "cfg/freeway.sumocfg",
                             "--tripinfo-output", "result/tripinfo.xml",
                             "--step-length","0.01",
                             "--device.emissions.probability", "1.0",])


    run()

