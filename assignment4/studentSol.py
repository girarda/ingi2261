#!/usr/bin/env python3

import rpg		

def get_clauses(merchant, level):
		needed_abilities = [abi_name for abi_name in level.ability_names]

		eq_by_needed_ability = []

		for ability in needed_abilities:
			equipement_for_ability = []
			for eq in merchant.equipments:
				if merchant.abi_map[ability] in eq.provides:
					equipement_for_ability.append(eq)
			eq_by_needed_ability.append(tuple(equipement_for_ability))

		clauses = []

		for tuples_of_eq in eq_by_needed_ability:
			for equipment in tuples_of_eq:
				clauses.append(tuple([-equipment.index, -equipment.conflicts.index]))

		for clause in eq_by_needed_ability:
			clauses.append(tuple([eq.index for eq in clause]))

		return list(set(clauses))

def get_nb_vars(merchant, level):
		needed_abilities = set([merchant.abi_map[abi_name] for abi_name in level.ability_names])

		required_equipment = set()

		for eq in merchant.equipments:
			if eq.provides.issubset(needed_abilities):
				print("eq: {}".format(eq))
				required_equipment.add(eq)
				print("conflicts: {}".format(eq.conflicts))
				required_equipment.add(eq.conflicts)

		return len(required_equipment)