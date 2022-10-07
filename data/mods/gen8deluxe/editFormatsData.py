# go through every pokemon in ./formats-data.ts and if the pokemon looks like this:
# raticate: {
	# 	isNonstandard: "Past",
	# 	tier: "Illegal",
	# },
# then replace it with the correct data from ../gen7/formats-data.ts
# this is the start of the formats-data.ts gen7 file:
# export const FormatsData: {[k: string]: ModdedSpeciesFormatsData} = {
# start of gen8 file:
# export const FormatsData: {[k: string]: SpeciesFormatsData} = {


import re
import os 
import json, _jsonnet



# get the data from the gen7 formats-data.ts file
with open(os.path.join(os.path.dirname(__file__), '../gen7/formats-data.ts'), 'r') as f:
	gen7data = f.read()
gen7data = gen7data.split('export const FormatsData: {[k: string]: ModdedSpeciesFormatsData} = ')[1]
gen7data = gen7data.split(';')[0]
with open ('gen7.txt', 'w') as w:
	w.write(gen7data)

gen7data = json.loads(_jsonnet.evaluate_file('gen7.txt'))

# get the data from the gen8 formats-data.ts file
with open(os.path.join(os.path.dirname(__file__), 'formats-data.ts'), 'r') as f:
	gen8data = f.read()
gen8data = gen8data.split('export const FormatsData: {[k: string]: SpeciesFormatsData} = ')[1]
gen8data = gen8data.split(';')[0]
with open ('gen8.txt', 'w') as w:
	w.write(gen8data)

gen8data = json.loads(_jsonnet.evaluate_file('gen8.txt'))

# go through every pokemon in gen8data and if the pokemon looks like this:
# raticate: {
	# 	isNonstandard: "Past",
	# 	tier: "Illegal",
	# },
# then replace it with the correct data from gen7data

mons = []

for pokemon in gen8data:
	mons.append(pokemon)
	if pokemon in gen7data:
		if 'isNonstandard' in gen8data[pokemon] and gen8data[pokemon]['isNonstandard'] == 'Past' and 'tier' in gen8data[pokemon] and gen8data[pokemon]['tier'] == 'Illegal':
			# check if the key exists in gen7data
				gen8data[pokemon] = gen7data[pokemon]

# write the new data to the gen8 formats-data.ts file
with open(os.path.join(os.path.dirname(__file__), 'formats-data.ts'), 'r') as f:
	gen8datafile = f.read()

newGen8 = json.dumps(gen8data, indent=1)
for mon in mons:
	newGen8 = newGen8.replace(f'"{mon}"', mon)

gen8datafile = gen8datafile.split('export const FormatsData: {[k: string]: SpeciesFormatsData} = ')[0] + 'export const FormatsData: {[k: string]: SpeciesFormatsData} = ' + newGen8 + ';'
with open(os.path.join(os.path.dirname(__file__), 'formats-data.ts'), 'w') as f:
	f.write(gen8datafile)

# delete the temp files
os.remove('gen7.txt')
os.remove('gen8.txt')

with open(os.path.join(os.path.dirname(__file__), 'formats-data.ts'), 'r') as f:
	gen8datafile = f.read()

with open(os.path.join(os.path.dirname(__file__), 'formats-data.ts'), 'w') as f:
	gen8datafile.replace('"randomBattleMoves"', 'randomBattleMoves')
	gen8datafile.replace('"randomBattleLevel"', 'randomBattleLevel')
	gen8datafile.replace('"randomDoubleBattleMoves"', 'randomDoubleBattleMoves')
	gen8datafile.replace('"randomDoubleBattleLevel"', 'randomDoubleBattleLevel')
	gen8datafile.replace('"tier"', 'tier')
	gen8datafile.replace('"doublesTier"', 'doublesTier')
	gen8datafile.replace('"isNonstandard"', 'isNonstandard')
	f.write(gen8datafile)