"""
生成随机车
"""
import random

def generate_platoon(VehicleRate,penetration,SimuTime):

	### make the generation is repeatable
	total = VehicleRate*4 / 3600
	CAVprob =  total * penetration  / 4
	HVprob = total * (1 - penetration) / 4
	print(HVprob)
	with open("cfg/freeway.rou.xml", "w") as routes:
		print("""<flows>
		<vType id="CAV" accel="2.5" tau = '0.6' decel="10" sigma="0.5" length="4.5"
		   minGap="10" maxSpeed="15" lcKeepRight="0" color="0,1,0" probability="1"
		   carFollowModel="CC" tauEngine="0.5" omegaN="0.2" xi="1" c1="0.5"
		   lanesCount="4" ccAccel="5" ccDecel="5" ploegKp="0.2" ploegKd="0.7" ploegH="0.5" />

		<vType id="HV" accel="2.5" tau = '1' decel="10" sigma="0.5" length="4.5"
		   minGap="10" maxSpeed="15" lcKeepRight="0" color="1,0,0" probability="1"
		   carFollowModel="CC" tauEngine="0.5" omegaN="0.2" xi="1" c1="0.5"
		   lanesCount="4" ccAccel="5" ccDecel="5" ploegKp="0.2" ploegKd="0.7" ploegH="0.5" />

		<vType id="HV1" accel="2.5" tau = '1' decel="10" lcKeepRight="0.2" sigma="0.5" length="4.5"
		   minGap="10" maxSpeed="15" color="1,0,0"  carFollowModel="IDM" />
		<route id="route1" edges="bi a1i_1 ci "/> """, file=routes)

		#print('<flow id="a1i_CAV" type="CAV" route="route1" departSpeed ="10" departLane ="3" begin="0" end="%i" probability="%s"/>' % (SimuTime,CAVprob), file=routes)    
		#print('<flow id="a1i_HV" type="HV" route="route1" departSpeed ="10" departLane ="3" begin="0" end="%i" probability="%s"/>' % (SimuTime,HVprob), file=routes)
		#print('<flow id="a2i_CAV" type="CAV" route="route1" departSpeed ="10" departLane ="2" begin="0" end="%i" probability="%s"/>' % (SimuTime,CAVprob), file=routes)    
		#print('<flow id="a2i_HV" type="HV" route="route1" departSpeed ="10" departLane ="2" begin="0" end="%i" probability="%s"/>' % (SimuTime,HVprob), file=routes) 
		#print('<flow id="a3i_CAV" type="CAV" route="route1" departSpeed ="10" departLane ="1" begin="0" end="%i" probability="%s"/>' % (SimuTime,CAVprob), file=routes)    
		#print('<flow id="a3i_HV" type="HV" route="route1" departSpeed ="10" departLane ="1" begin="0" end="%i" probability="%s"/>' % (SimuTime,HVprob), file=routes) 
		print('<flow id="a4i_CAV" type="CAV" route="route1" departSpeed ="10" departLane ="0" begin="0" end="%i" probability="%s"/>' % (SimuTime,CAVprob), file=routes)    
		print('<flow id="a4i_HV" type="HV" route="route1" departSpeed ="10" departLane ="0" begin="0" end="%i" probability="%s"/>' % (SimuTime,HVprob), file=routes)                
		print("</flows>", file=routes)     


if __name__ == '__main__':
	VehicleRate = 1800
	SimuTime = 3600
	penetration = 0.5
	SizeDict = generate_platoon(VehicleRate, penetration,SimuTime)
			
			
			
			
			
			
			
			
			
			
	