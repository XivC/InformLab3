import yaml
import json
import time


def convert_yaml_to_json_my(yml_file):
	yaml_file = open(yml_file).readlines()
	def count_level(s):
		l = 0
		for i in s:
			if i == " ":
				l += 1
			else:
				return l

	def tree(lines, level):
		n = 0
		subtree = {}
		for line in lines:
			n += 1
			key = line.split(":")[0].replace("\n","")
			arg = "".join(line.split(": ")[1:]).replace("\n", "")
			lv = count_level(key)
			if lv < level:
				return subtree
			if lv - level == 1:
				if len(arg) > 0:
					subtree[key.strip()] = arg.strip()
				else:
					subtree[key.strip()] = tree(lines[n:], lv + 1)
			else:
				continue
		return subtree

	for l in yaml_file:
		if l.count(":") == 0:
			yaml_file.remove(l)

	print(str(tree(yaml_file, -1)).replace("'", '"').replace('""', '"'), file = open("schedule_my.json", 'w'))


def convert_yaml_to_json_libs(yaml_file):
	data = yaml.load(open(yaml_file), Loader = yaml.FullLoader)
	data_json = json.dumps(data)
	open("schedule_libs.json", "w").write(data_json)


def time_experiment(iterations):
	print("My time" + " " * 2 + "Libs_time" + " " + "My - Libs")
	for i in range(iterations):
		s_time = time.time()
		convert_yaml_to_json_my("schedule.yaml")
		delta_t_my = time.time()-s_time
		s_time = time.time()
		convert_yaml_to_json_libs("schedule.yaml")
		delta_t_libs = time.time()-s_time
		delta = delta_t_my - delta_t_libs
		print("%6f %6f %6f" % (delta_t_my, delta_t_libs, delta))


convert_yaml_to_json_my("schedule.yaml")   #Задание 1
convert_yaml_to_json_libs("schedule.yaml") #Задание 2
time_experiment(10)                        #Задание 3  
