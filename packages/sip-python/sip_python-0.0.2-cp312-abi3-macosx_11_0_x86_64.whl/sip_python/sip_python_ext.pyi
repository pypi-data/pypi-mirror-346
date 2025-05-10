from collections.abc import Callable
import enum
from typing import Annotated

from numpy.typing import ArrayLike
import scipy.sparse


FAILED_CHECK: Status = Status.FAILED_CHECK

ITERATION_LIMIT: Status = Status.ITERATION_LIMIT

LINE_SEARCH_FAILURE: Status = Status.LINE_SEARCH_FAILURE

LINE_SEARCH_ITERATION_LIMIT: Status = Status.LINE_SEARCH_ITERATION_LIMIT

LOCALLY_INFEASIBLE: Status = Status.LOCALLY_INFEASIBLE

class ModelCallbackInput:
    def __init__(self, problem_dimensions: ProblemDimensions) -> None: ...

    @property
    def x(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @property
    def y(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @property
    def z(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

class ModelCallbackOutput:
    def __init__(self) -> None: ...

    @property
    def f(self) -> float: ...

    @f.setter
    def f(self, arg: float, /) -> None: ...

    @property
    def gradient_f(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @gradient_f.setter
    def gradient_f(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def upper_hessian_lagrangian(self) -> scipy.sparse.csc_matrix[float]: ...

    @upper_hessian_lagrangian.setter
    def upper_hessian_lagrangian(self, arg: scipy.sparse.csc_matrix[float], /) -> None: ...

    @property
    def c(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @c.setter
    def c(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def jacobian_c(self) -> scipy.sparse.csr_matrix[float]: ...

    @jacobian_c.setter
    def jacobian_c(self, arg: scipy.sparse.csr_matrix[float], /) -> None: ...

    @property
    def g(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @g.setter
    def g(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def jacobian_g(self) -> scipy.sparse.csr_matrix[float]: ...

    @jacobian_g.setter
    def jacobian_g(self, arg: scipy.sparse.csr_matrix[float], /) -> None: ...

class OutputStatus:
    def __init__(self) -> None: ...

    @property
    def exit_status(self) -> Status: ...

    @property
    def num_iterations(self) -> int: ...

    @property
    def max_primal_violation(self) -> float: ...

    @property
    def max_dual_violation(self) -> float: ...

class ProblemDimensions:
    def __init__(self) -> None: ...

    @property
    def x_dim(self) -> int: ...

    @x_dim.setter
    def x_dim(self, arg: int, /) -> None: ...

    @property
    def s_dim(self) -> int: ...

    @s_dim.setter
    def s_dim(self, arg: int, /) -> None: ...

    @property
    def y_dim(self) -> int: ...

    @y_dim.setter
    def y_dim(self, arg: int, /) -> None: ...

    @property
    def upper_hessian_lagrangian_nnz(self) -> int: ...

    @upper_hessian_lagrangian_nnz.setter
    def upper_hessian_lagrangian_nnz(self, arg: int, /) -> None: ...

    @property
    def jacobian_c_nnz(self) -> int: ...

    @jacobian_c_nnz.setter
    def jacobian_c_nnz(self, arg: int, /) -> None: ...

    @property
    def jacobian_g_nnz(self) -> int: ...

    @jacobian_g_nnz.setter
    def jacobian_g_nnz(self, arg: int, /) -> None: ...

    @property
    def kkt_nnz(self) -> int: ...

    @kkt_nnz.setter
    def kkt_nnz(self, arg: int, /) -> None: ...

    @property
    def kkt_L_nnz(self) -> int: ...

    @kkt_L_nnz.setter
    def kkt_L_nnz(self, arg: int, /) -> None: ...

    @property
    def is_jacobian_c_transposed(self) -> bool: ...

    @is_jacobian_c_transposed.setter
    def is_jacobian_c_transposed(self, arg: bool, /) -> None: ...

    @property
    def is_jacobian_g_transposed(self) -> bool: ...

    @is_jacobian_g_transposed.setter
    def is_jacobian_g_transposed(self, arg: bool, /) -> None: ...

class QDLDLSettings:
    def __init__(self) -> None: ...

    @property
    def permute_kkt_system(self) -> bool: ...

    @permute_kkt_system.setter
    def permute_kkt_system(self, arg: bool, /) -> None: ...

    @property
    def kkt_pinv(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None))]: ...

    @kkt_pinv.setter
    def kkt_pinv(self, arg: Annotated[ArrayLike, dict(dtype='int32', shape=(None))], /) -> None: ...

SOLVED: Status = Status.SOLVED

SUBOPTIMAL: Status = Status.SUBOPTIMAL

class Settings:
    def __init__(self) -> None: ...

    @property
    def max_iterations(self) -> int: ...

    @max_iterations.setter
    def max_iterations(self, arg: int, /) -> None: ...

    @property
    def max_ls_iterations(self) -> int: ...

    @max_ls_iterations.setter
    def max_ls_iterations(self, arg: int, /) -> None: ...

    @property
    def num_iterative_refinement_steps(self) -> int: ...

    @num_iterative_refinement_steps.setter
    def num_iterative_refinement_steps(self, arg: int, /) -> None: ...

    @property
    def max_kkt_violation(self) -> float: ...

    @max_kkt_violation.setter
    def max_kkt_violation(self, arg: float, /) -> None: ...

    @property
    def max_suboptimal_constraint_violation(self) -> float: ...

    @max_suboptimal_constraint_violation.setter
    def max_suboptimal_constraint_violation(self, arg: float, /) -> None: ...

    @property
    def max_merit_slope(self) -> float: ...

    @max_merit_slope.setter
    def max_merit_slope(self, arg: float, /) -> None: ...

    @property
    def initial_regularization(self) -> float: ...

    @initial_regularization.setter
    def initial_regularization(self, arg: float, /) -> None: ...

    @property
    def regularization_decay_factor(self) -> float: ...

    @regularization_decay_factor.setter
    def regularization_decay_factor(self, arg: float, /) -> None: ...

    @property
    def tau(self) -> float: ...

    @tau.setter
    def tau(self, arg: float, /) -> None: ...

    @property
    def start_ls_with_alpha_s_max(self) -> bool: ...

    @start_ls_with_alpha_s_max.setter
    def start_ls_with_alpha_s_max(self, arg: bool, /) -> None: ...

    @property
    def initial_mu(self) -> float: ...

    @initial_mu.setter
    def initial_mu(self, arg: float, /) -> None: ...

    @property
    def mu_update_factor(self) -> float: ...

    @mu_update_factor.setter
    def mu_update_factor(self, arg: float, /) -> None: ...

    @property
    def mu_min(self) -> float: ...

    @mu_min.setter
    def mu_min(self, arg: float, /) -> None: ...

    @property
    def initial_penalty_parameter(self) -> float: ...

    @initial_penalty_parameter.setter
    def initial_penalty_parameter(self, arg: float, /) -> None: ...

    @property
    def min_acceptable_constraint_violation_ratio(self) -> float: ...

    @min_acceptable_constraint_violation_ratio.setter
    def min_acceptable_constraint_violation_ratio(self, arg: float, /) -> None: ...

    @property
    def penalty_parameter_increase_factor(self) -> float: ...

    @penalty_parameter_increase_factor.setter
    def penalty_parameter_increase_factor(self, arg: float, /) -> None: ...

    @property
    def penalty_parameter_decrease_factor(self) -> float: ...

    @penalty_parameter_decrease_factor.setter
    def penalty_parameter_decrease_factor(self, arg: float, /) -> None: ...

    @property
    def max_penalty_parameter(self) -> float: ...

    @max_penalty_parameter.setter
    def max_penalty_parameter(self, arg: float, /) -> None: ...

    @property
    def armijo_factor(self) -> float: ...

    @armijo_factor.setter
    def armijo_factor(self, arg: float, /) -> None: ...

    @property
    def line_search_factor(self) -> float: ...

    @line_search_factor.setter
    def line_search_factor(self, arg: float, /) -> None: ...

    @property
    def line_search_min_step_size(self) -> float: ...

    @line_search_min_step_size.setter
    def line_search_min_step_size(self, arg: float, /) -> None: ...

    @property
    def min_merit_slope_to_skip_line_search(self) -> float: ...

    @min_merit_slope_to_skip_line_search.setter
    def min_merit_slope_to_skip_line_search(self, arg: float, /) -> None: ...

    @property
    def enable_elastics(self) -> bool: ...

    @enable_elastics.setter
    def enable_elastics(self, arg: bool, /) -> None: ...

    @property
    def elastic_var_cost_coeff(self) -> float: ...

    @elastic_var_cost_coeff.setter
    def elastic_var_cost_coeff(self, arg: float, /) -> None: ...

    @property
    def enable_line_search_failures(self) -> bool: ...

    @enable_line_search_failures.setter
    def enable_line_search_failures(self, arg: bool, /) -> None: ...

    @property
    def print_logs(self) -> bool: ...

    @print_logs.setter
    def print_logs(self, arg: bool, /) -> None: ...

    @property
    def print_line_search_logs(self) -> bool: ...

    @print_line_search_logs.setter
    def print_line_search_logs(self, arg: bool, /) -> None: ...

    @property
    def print_search_direction_logs(self) -> bool: ...

    @print_search_direction_logs.setter
    def print_search_direction_logs(self, arg: bool, /) -> None: ...

    @property
    def print_derivative_check_logs(self) -> bool: ...

    @print_derivative_check_logs.setter
    def print_derivative_check_logs(self, arg: bool, /) -> None: ...

    @property
    def only_check_search_direction_slope(self) -> bool: ...

    @only_check_search_direction_slope.setter
    def only_check_search_direction_slope(self, arg: bool, /) -> None: ...

    @property
    def assert_checks_pass(self) -> bool: ...

    @assert_checks_pass.setter
    def assert_checks_pass(self, arg: bool, /) -> None: ...

class Solver:
    def __init__(self, sip_settings: Settings, qdldl_settings: QDLDLSettings, problem_dimension: ProblemDimensions, model_callback: Callable[[ModelCallbackInput], ModelCallbackOutput]) -> None: ...

    def solve(self, arg: Variables, /) -> OutputStatus: ...

class Status(enum.Enum):
    SOLVED = 0

    SUBOPTIMAL = 1

    LOCALLY_INFEASIBLE = 2

    ITERATION_LIMIT = 3

    LINE_SEARCH_ITERATION_LIMIT = 4

    LINE_SEARCH_FAILURE = 5

    TIMEOUT = 6

    FAILED_CHECK = 7

TIMEOUT: Status = Status.TIMEOUT

class Variables:
    def __init__(self, problem_dimensions: ProblemDimensions) -> None: ...

    @property
    def x(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @x.setter
    def x(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def s(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @s.setter
    def s(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def e(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @e.setter
    def e(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def y(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @y.setter
    def y(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

    @property
    def z(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None))]: ...

    @z.setter
    def z(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None))], /) -> None: ...

def getLnnz(arg: scipy.sparse.csc_matrix[float], /) -> int:
    """Computes L's nnz for an L D L^T decomposition."""
