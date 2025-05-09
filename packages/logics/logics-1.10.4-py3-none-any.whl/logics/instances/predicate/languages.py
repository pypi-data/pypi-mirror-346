from copy import deepcopy

from logics.classes.predicate.language import PredicateLanguage, InfinitePredicateLanguage, TruthPredicateLanguage

# Classical predicate logic
individual_constants = ['a', 'b', 'c', 'd', 'e']
variables = ['x', 'y', 'z']
individual_metavariables = ['α', 'β', 'γ', 'δ', 'ε']  # for rules, can be instantiated with either variables or ind constants
variable_metavariables = ['χ', 'ψ', 'ω']
quantifiers = ['∀', '∃']
metavariables = ['A', 'B', 'C', 'D', 'E']  # These are formula metavariables
constant_arity_dict = {'~': 1, '∧': 2, '∨': 2, '→': 2, '↔': 2}
predicate_letters = {"M": 1, "N": 1, 'P': 1, 'Q': 1, 'R': 2, 'S': 3, "T": 2}
predicate_variables = {'W': 1, 'X': 1, 'Y': 1, 'Z': 2}  # These can be quantified over in second order languages
sentential_constants = ['⊥', '⊤']

classical_predicate_language = PredicateLanguage(individual_constants=individual_constants,
                                                 variables=variables,
                                                 individual_metavariables=individual_metavariables,
                                                 variable_metavariables=variable_metavariables,
                                                 quantifiers=quantifiers,
                                                 metavariables=metavariables,
                                                 constant_arity_dict=constant_arity_dict,
                                                 predicate_letters=predicate_letters,
                                                 predicate_variables=predicate_variables,
                                                 sentential_constants=sentential_constants)

# Predicate language for natural deduction: no biconditional, no verum, no second order stuff
natural_deduction_predicate_language = deepcopy(classical_predicate_language)
del natural_deduction_predicate_language.constant_arity_dict['↔']
natural_deduction_predicate_language.sentential_constants = ['⊥']
natural_deduction_predicate_language.predicate_variables = {}

classical_infinite_predicate_language = InfinitePredicateLanguage(individual_constants=individual_constants,
                                                                  variables=variables,
                                                                  individual_metavariables=individual_metavariables,
                                                                  variable_metavariables=variable_metavariables,
                                                                  quantifiers=quantifiers,
                                                                  metavariables=metavariables,
                                                                  constant_arity_dict=constant_arity_dict,
                                                                  predicate_letters=predicate_letters,
                                                                  predicate_variables=predicate_variables,
                                                                  sentential_constants=sentential_constants)

function_symbols = {'f': 1, 'g': 2}
classical_function_language = InfinitePredicateLanguage(individual_constants=individual_constants,
                                                        variables=variables,
                                                        individual_metavariables=individual_metavariables,
                                                        variable_metavariables=variable_metavariables,
                                                        quantifiers=quantifiers,
                                                        metavariables=metavariables,
                                                        constant_arity_dict=constant_arity_dict,
                                                        predicate_letters=predicate_letters,
                                                        predicate_variables=predicate_variables,
                                                        sentential_constants=sentential_constants,
                                                        function_symbols=function_symbols)


# ----------------------------------------------------------------------------------------------------------------------
# Arithmetic languages (natural and real number)

arithmetic_language = PredicateLanguage(individual_constants=['0'],
                                        variables=['x', 'y', 'z'],
                                        individual_metavariables=individual_metavariables,
                                        variable_metavariables=variable_metavariables,
                                        quantifiers=quantifiers,
                                        metavariables=metavariables,
                                        constant_arity_dict=constant_arity_dict,
                                        predicate_letters={'=': 2, '>': 2, '<': 2},
                                        predicate_variables=predicate_variables,
                                        function_symbols={'s': 1, '+': 2, '*': 2, '**': 2})


def is_numeral(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
real_number_arithmetic_language = PredicateLanguage(individual_constants=is_numeral,
                                                    variables=['x', 'y', 'z'],
                                                    individual_metavariables=individual_metavariables,
                                                    variable_metavariables=variable_metavariables,
                                                    quantifiers=quantifiers, metavariables=metavariables,
                                                    constant_arity_dict=constant_arity_dict,
                                                    predicate_letters={'=': 2, '>': 2, '<': 2},
                                                    predicate_variables=predicate_variables,
                                                    function_symbols={'+': 2, '-': 2, '*': 2, '/': 2, '//': 2, '**': 2})


arithmetic_truth_language = TruthPredicateLanguage(individual_constants=['0'],
                                                   variables=['x', 'y', 'z'],
                                                   individual_metavariables=individual_metavariables,
                                                   variable_metavariables=variable_metavariables,
                                                   quantifiers=quantifiers, metavariables=metavariables,
                                                   constant_arity_dict=constant_arity_dict,
                                                   predicate_letters={'Tr': 1, '=': 2, '>': 2, '<': 2},
                                                   predicate_variables=predicate_variables,
                                                   sentential_constants=['λ'],
                                                   function_symbols={'s': 1, 'quote': 1, '+': 2, '*': 2, '**': 2})
