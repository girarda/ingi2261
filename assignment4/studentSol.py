#!/usr/bin/env python3

import rpg


def getPossibilities(merchant, possibility, allPossibilities, eq_by_needed_ability):
	_getPossibilities(merchant, possibility, allPossibilities, eq_by_needed_ability, 0)
	# pass

def _getPossibilities(merchant, possibility, allPossibilities, eq_by_needed_ability, currentAbility):
	if currentAbility == len(eq_by_needed_ability):
		allPossibilities.add(tuple(possibility))
	else:
		for i in range(len(eq_by_needed_ability[currentAbility])):
			if all([eq.index is not eq_by_needed_ability[currentAbility][i].conflicts.index or eq_by_needed_ability[currentAbility][i].index == eq.conflicts.index for eq in possibility]):
					possibility[currentAbility] = eq_by_needed_ability[currentAbility][i]
					_getPossibilities(merchant, possibility, allPossibilities, eq_by_needed_ability, currentAbility+1)				

def get_clauses(merchant, level):
		# print(level.ability_names)
		# print(merchant.equ_map)

		# for ability in level.ability_names:
		# 	for eq in merchant.equipments:
		# 		if merchant.abi_map[ability] in eq.provides:
		# 			print(eq)
		# exit()


		needed_abilities = [abi_name for abi_name in level.ability_names]

		eq_by_needed_ability = []

		for ability in needed_abilities:
			equipement_for_ability = []
			for eq in merchant.equipments:
				if merchant.abi_map[ability] in eq.provides:
					equipement_for_ability.append(eq)
			eq_by_needed_ability.append(tuple(equipement_for_ability))


		# for ability in needed_abilities:
		# 	possible_eq = []
		# 	for eq in merchant.equipments:
		# 		if merchant.abi_map[ability] in eq.provides:
		# 			possible_eq.append(eq)
		# 	eq_by_needed_ability.append(possible_eq)


		# all_possibilities = set()
		# possible_set = [possibility[0] for possibility in eq_by_needed_ability]

		# all_possibilities.add(tuple(possible_set))
		# getPossibilities(merchant, possible_set, all_possibilities, eq_by_needed_ability)

		# Append all clauses needed to find the correct equipment in the 'clauses' list.
		#
		# Minisat variables are represented with integers. As such you should use
		# the index attribute of classes Ability and Equipment from the rpg.py module
		# 
		# The equipments and abilities they provide read from the merchant file you passed
		# as argument are contained in the variable 'merchant'.
		# The enemies and abilities they require to be defeated read from the level file you
		# passed as argument are contained in the variable 'level'
		# 
		# For example if you want to add the clauses equ1 or equ2 or ... or equN (i.e. a
		# disjunction of all the equipment pieces the merchant proposes), you should write:
		# 
		# clauses.append(tuple(equ.index for equ in merchant.equipments))
		clauses = []

		for tuples_of_eq in eq_by_needed_ability:
			for equipment in tuples_of_eq:
				clauses.append(tuple([-equipment.index, -equipment.conflicts.index]))

		for clause in eq_by_needed_ability:
			clauses.append(tuple([eq.index for eq in clause]))

		# for possibility in all_possibilities:
		# 	clauses.append(tuple([eq.index for eq in possibility]))

		for eq in merchant.equipments:
			print("{}: {}".format(eq, eq.index))

		# print(list(set(clauses)))
		# exit()

		return list(set(clauses))

def get_nb_vars(merchant, level):
		# nb_vars should be the number of different variables present in your list 'clauses'
		# 
		# For example, if your clauses contain all the equipments proposed by merchant and
		# all the abilities provided by these equipment, you would have:
		# nb_vars = len(merchant.abilities) + len(merchant.equipments)
		needed_abilities = set([merchant.abi_map[abi_name] for abi_name in level.ability_names])

		required_equipment = set()

		for eq in merchant.equipments:
			if eq.provides.issubset(needed_abilities):
				print("eq: {}".format(eq))
				# print("provides: {}".format(eq.provides))
				required_equipment.add(eq)
				print("conflicts: {}".format(eq.conflicts))
				required_equipment.add(eq.conflicts)

		return len(required_equipment)