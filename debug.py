event_name = "QUARTERFINAL_NEWCOMER__EASTCOAST_SWING"
num_adv = None

if "SEMI" in event_name: num_adv = 6
print(num_adv)
if "QUARTER" in event_name: num_adv = 10
print(num_adv)
if "3" in event_name: num_adv = 16
print(num_adv)
if "2" in event_name: num_adv = 20
print(num_adv)
if "1" in event_name: num_adv = 24
else: num_adv = 1
print(num_adv)