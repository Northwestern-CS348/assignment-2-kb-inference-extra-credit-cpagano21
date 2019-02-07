import read, copy
from util import *
from logical_classes import *

verbose = 0




class KnowledgeBase(object):

    _string = ""

    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Implementation goes here
        # Not required for the extra credit assignment

    def spacing(self, count):
        s = ""
        for i in range(count):
            s += " "
        return s

    def kb_help(self, fact_or_rule, count):
        if len(fact_or_rule.supported_by) > 0 and len(fact_or_rule.supported_by[0]) > 0:

            for i in range(len(fact_or_rule.supported_by)):
                #count += 2
                spaces = self.spacing(count+2)

                self._string += spaces
                self._string += "SUPPORTED BY" + "\n"
                for x in fact_or_rule.supported_by[i]:
                    self._string += "  "
                    if isinstance(x, Fact):
                        n_f_r = self._get_fact(x)
                        spaces_fact = self.spacing(count+2)
                        self._string += spaces_fact
                        self._string += "fact: "
                        self._string += str(n_f_r.statement)
                        if len(n_f_r.supported_by) == 0:
                            self._string += " ASSERTED"
                        self._string += "\n"

                    elif isinstance(x, Rule):
                        n_f_r = self._get_rule(x)
                        spaces_rule = self.spacing(count+2)
                        self._string += spaces_rule
                        self._string += "rule: ("
                        for i in range(len(n_f_r.lhs)):
                            if i == len(n_f_r.lhs) - 1:
                                self._string += str(n_f_r.lhs[i])
                                break
                            self._string += str(n_f_r.lhs[i]) + ", "
                        self._string += ") -> "
                        self._string += str(n_f_r.rhs)
                        if len(n_f_r.supported_by) == 0:
                            self._string += " ASSERTED"
                        self._string += "\n"
                    else:
                        return
                    count += 2

                    self.kb_help(n_f_r, count+2)
                    count -= 2


        return self._string

    def kb_explain(self, fact_or_rule):
        """
        Explain where the fact or rule comes from

        Args:
            fact_or_rule (Fact or Rule) - Fact or rule to be explained

        Returns:
            string explaining hierarchical support from other Facts and rules
        """

        ####################################################
        # Student code goes here


        if isinstance(fact_or_rule, Fact):
            if fact_or_rule in self.facts:


                self._string += "fact: "
                self._string += (str(fact_or_rule.statement))
                self._string += "\n"
                actual_f_r = self._get_fact(fact_or_rule)

            else:
                return "Fact is not in the KB"
        if isinstance(fact_or_rule, Rule):
            if fact_or_rule in self.rules:
                self._string += "rule: ("
                for x in fact_or_rule.lhs:
                    self._string += str(x) + ", "

                actual_f_r = self._get_rule(fact_or_rule)
            else:
                return "Rule is not in the KB"

        count = 0

        self.kb_help(actual_f_r, count)
        """
        for x in actual_f_r.supported_by[0]:

            if isinstance(x, Fact):
                new_fact = self._get_fact(x)

                self.kb_help(new_fact, _string)
            if isinstance(x, Rule):
                new_rule = self._get_rule(x)

                self.kb_help(new_rule, _string)
        """
        return self._string




    """
            if len(fact_or_rule.supported_by) > 0:
                my_string += "SUPPORTED BY: " + "\n"
                for each in fact_or_rule.supported_by:
                    self.syntax_helper(fact_or_rule)
            
            elif isinstance(fact_or_rule, Rule):
                _string = "rule:  ("
                for each in fact_or_rule.supports_rules.lhs:
                    _string += " , " + str(fact_or_rule)
                    _string += ")"
                    _string
            else:
    """
    """
    def kb_lookup(self, fact_or_rule):
        if isinstance(fact_or_rule, Fact) or isinstance(fact_or_rule, Rule):
            if fact_or_rule in self.facts:
                _base = self.facts.index(fact_or_rule)
                _facts = self.facts[_base]
                return self.facts[_base]
        elif fact_or_rule in self.rules:
            _base = self.rules.index(fact_or_rule)
            _facts = self.rules[_base]
            return self.rules[_base]
        else:
            return False

        _facts = self.kb_lookup(fact_or_rule)
        if _facts != True:
            if isinstance(fact_or_rule, Fact):
                return "Fact is not in the KB"
            elif isinstance(fact_or_rule, Fact):
                    return "Rule is not in the KB"
            else:
                return False

        _string = ""
        if len(_facts.supported_by) == 0:
            if isinstance(fact_or_rule, Fact):
                _string += "fact: "
                _string += str(_facts.statement)
                _string += " ASSERTED"
            if isinstance(fact_or_rule, Rule):
                _string += "rule: ("
            if len(_facts.lhs) > 1:
                space = 0
                for x in _facts.lhs:
                    _string += str(x)
                    _string += ", "
                    space += 1
            else:
                _string += str(_facts.lhs[0])
            _string += ") -> "
            _string += str(_facts.rhs)
            _string += " ASSERTED" + "\n" 
            
    """



class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
               [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Implementation goes here
        # Not required for the extra credit assignment
