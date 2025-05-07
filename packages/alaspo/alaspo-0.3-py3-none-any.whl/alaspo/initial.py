from .__init__ import logger


class AbstractInititalOperator:

    def construct(self, global_timeout):
        """construct the initial solution used for lns

        Returns either:
            (1) a pickleable object, with attributes:
             - sat
                True ... the logic program is proven to be satisfiable
                False ... the logic program is proven to be un-satisfiable
                None ... satisfiability was not proven
             - cost
                None ... the cost is undefined / unknown
                int ... this solution's cost
             - model
                None ... no answer set was found
                Model ... the found answer set

            (2) a set of clingo.Symbols
        """
        pass


class ClingoInitialOperator(AbstractInititalOperator):

    def __init__(self, internal_solver, configuration=None, pre_opt_time=0):
        self.__internal_solver = internal_solver
        self.__configuration = configuration
        self.__pre_opt_time = pre_opt_time

    def construct(self, global_timeout):
        logger.debug('initial operator executing')
        if self.__pre_opt_time > 0:
            if type(self.__pre_opt_time) == float:
                t = round(global_timeout * self.__pre_opt_time)
            else:
                t = self.__pre_opt_time
            res = self.__internal_solver.solve(timelimit=min(t, global_timeout), configuration=self.__configuration)
            if not res.sat:
                time_left = global_timeout - min(t, global_timeout)
                res = self.__internal_solver.solve(timelimit=time_left, configuration=self.__configuration, modellimit=1)
            return res
        else:
            return self.__internal_solver.solve(timelimit=global_timeout, configuration=self.__configuration, modellimit=1)


# InitialOperator Factory

def get_operator(args, internal_solver):
    """
    returns a new initial operator of the given type with given args
    """

    if 'timeout' in args:
        timeout = args['timeout']
    else:
        timeout = 0

    if 'configuration' in args:
        configuration = args['configuration']
    else:
        configuration = None

    return ClingoInitialOperator(internal_solver, configuration, timeout)
