import time
from . import initial
import clingo
from .__init__ import logger


class ClingoLNS:

    def __init__(self, internal_solver, program, initial_operator, relax_operators, search_operators, strategy):
        """
        instantiated the VLNS solver with required relax operators and the optional move timeout in seconds (default 5)
        """
        self.__internal_solver = internal_solver
        self.__program = program
        self._unsat_count = 0
        self._timeout_count = 0

        if initial_operator is None:
            raise ValueError('no initial operator provided')

        self.__initial_operator = initial_operator

        self.__strategy = strategy

        # keep references current operators
        self.relax_operator = None
        self.search_operator = None

        self.__strategy.prepare(relax_operators, search_operators)

        self.best_solution = None
        self.search_complete = False

    def get_portfolio(self):
        """
        returns a tuple containing the used relax and search operators
        """

        return self.__strategy.get_portfolio()

    def solve(self, timeout, on_solution=None):
        """
        runs the VLNS algorithm on the given ASP instance for the given timelimit
        """

        self._unsat_count = 0
        self._timeout_count = 0

        start_time = time.time()
        def time_left(): return timeout - (time.time() - start_time)

        # get internal solver
        internal_solver = self.__internal_solver

        # load clear and program
        internal_solver.load_string(self.__program)

        # ground base
        internal_solver.ground()

        incumbent = None

        # obtain initial solution
        solution = self.__initial_operator.construct(time_left())

        if solution is None or solution == []:
            logger.info('NO INTITIAL SOLUTION FOUND')
            print('Could not obtain initial solution!')
            return None

        if isinstance(solution, list) and all(isinstance(x, clingo.symbol.Symbol) for x in solution):
            # non default init operator provided a set of symbols which need to be feed to the solver
            solution = internal_solver.solve(
                assumptions=solution, modellimit=1, timelimit=time_left())
        elif not isinstance(self.__initial_operator, initial.ClingoInitialOperator):
            # non default init operator was used, hence we seed the solver with the greedy solution
            internal_solver.solve(
                assumptions=solution.model.symbols, modellimit=1, timelimit=time_left())

        logger.info(f'initial cost: {solution.cost}')
        incumbent = solution
        if on_solution != None and solution != None:
            on_solution(incumbent, time.time() - start_time)
        self.best_solution = incumbent

        if solution.exhausted:
            logger.info('OPTIMAL SOLUTION FOUND')
            self.search_complete = True
            return incumbent

        # LNS loop
        assumptions = None
        while time_left() > 0:
            move_start_time = time.time()

            # get assumptions
            if assumptions is None or not self.__strategy.supports_intensification():
                self.relax_operator, self.search_operator = self.__strategy.select_operators()
                logger.debug('selected relax operator %s and search operator %s' % (
                    self.relax_operator.name(), self.search_operator.name()))
                assumptions = self.relax_operator.get_move_assumptions(
                    incumbent)
            # perform move
            max_move_time = time_left()
            if max_move_time <= 0:
                break
            solution = self.search_operator.execute(assumptions, max_move_time)

            prev_cost = incumbent.cost
            if solution.sat:
                # solution found, update incumbent
                incumbent = solution
                logger.info(f'found solution with cost: {incumbent.cost}')
                if solution.exhausted:
                    logger.debug('move optimal')
                if on_solution != None:
                    on_solution(incumbent, time.time() - start_time)
                self.best_solution = incumbent
                if prev_cost == solution.cost:
                    assumptions = None
                self._unsat_count = 0
                self._timeout_count = 0
            else:
                # unsat or timeout, do not change incumbent and reset assumptions
                if solution.sat is False or solution.exhausted:
                    self._timeout_count = 0
                    if len(assumptions) == 0:
                        logger.info('OPTIMAL SOLUTION FOUND')
                        self.search_complete = True
                        return incumbent
                    else:
                        logger.debug('unsat/optimal under current assumptions')
                        self._unsat_count += 1
                else:
                    logger.debug('move timed out')
                    self._unsat_count = 0
                    self._timeout_count += 1
                assumptions = None

            move_end_time = time.time()
            operators = (self.relax_operator, self.search_operator)
            self.__strategy.on_move_finished(
                operators, prev_cost, solution, move_end_time - move_start_time)

        return incumbent
