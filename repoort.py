
def report(S):
	avg_death = 0
	avg_infection = 0
	avg_maximum_infection = 0
	avg_maximum_infection_time = 0
	avg_stop_periods = 0

	f = open('total_death_' + str(S) + '.txt', 'r')
	lines = f.readlines()
	for line in lines:
		avg_death += int(line)
	avg_death = avg_death / len(lines)
	f.close()

	f = open('total_infection_' + str(S) + '.txt', 'r')
	lines = f.readlines()
	for line in lines:
		avg_infection += int(line)
	avg_infection = avg_infection / len(lines)
	f.close()

	f = open('maximum_infection_' + str(S) + '.txt', 'r')
	lines = f.readlines()
	for line in lines:
		tmp = line.split(",")
		avg_maximum_infection += int(tmp[0])
		avg_maximum_infection_time += int(tmp[1])
	avg_maximum_infection = avg_maximum_infection / len(lines)
	avg_maximum_infection_time = avg_maximum_infection_time / len(lines)
	f.close()

	f = open('stop_periods_' + str(S) + '.txt', 'r')
	lines = f.readlines()
	for line in lines:
		avg_stop_periods += int(line)
	avg_stop_periods = avg_stop_periods / len(lines)
	f.close()

	f = open('report_' + str(S) + '.txt', 'a')
	f.write("avg_infection")
	f.write("\n")
	f.write(str(avg_infection))
	f.write("\n")

	f.write("avg_death")
	f.write("\n")
	f.write(str(avg_death))
	f.write("\n")

	f.write("avg_stop_periods")
	f.write("\n")
	f.write(str(avg_stop_periods))
	f.write("\n")	

	f.write("avg_maximum_infection")
	f.write("\n")
	f.write(str(avg_maximum_infection))
	f.write("\n")

	f.write("maximum_infection_periods")
	f.write("\n")
	f.write(str(avg_maximum_infection_time))
	f.write("\n")
	f.close()

report(0)