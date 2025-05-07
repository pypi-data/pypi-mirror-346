from kirin import ir as _ir
from kirin.prelude import structural_no_opt as _structural_no_opt
from kirin.lowering import wraps as _wraps

from . import stmts as stmts, types as types, rewrite as rewrite
from .traits import Unitary as Unitary, MaybeUnitary as MaybeUnitary
from ._dialect import dialect as dialect


@_wraps(stmts.Kron)
def kron(lhs: types.Op, rhs: types.Op) -> types.Op: ...


@_wraps(stmts.Mult)
def mult(lhs: types.Op, rhs: types.Op) -> types.Op: ...


@_wraps(stmts.Scale)
def scale(op: types.Op, factor: complex) -> types.Op: ...


@_wraps(stmts.Adjoint)
def adjoint(op: types.Op) -> types.Op: ...


@_wraps(stmts.Control)
def control(op: types.Op, *, n_controls: int) -> types.Op:
    """
    Create a controlled operator.

    Note, that when considering atom loss, the operator will not be applied if
    any of the controls has been lost.

    Args:
        operator: The operator to apply under the control.
        n_controls: The number qubits to be used as control.

    Returns:
        Operator
    """
    ...


@_wraps(stmts.Identity)
def identity(*, sites: int) -> types.Op: ...


@_wraps(stmts.Rot)
def rot(axis: types.Op, angle: float) -> types.Op: ...


@_wraps(stmts.ShiftOp)
def shift(theta: float) -> types.Op: ...


@_wraps(stmts.PhaseOp)
def phase(theta: float) -> types.Op: ...


@_wraps(stmts.X)
def x() -> types.Op: ...


@_wraps(stmts.Y)
def y() -> types.Op: ...


@_wraps(stmts.Z)
def z() -> types.Op: ...


@_wraps(stmts.H)
def h() -> types.Op: ...


@_wraps(stmts.S)
def s() -> types.Op: ...


@_wraps(stmts.T)
def t() -> types.Op: ...


@_wraps(stmts.P0)
def p0() -> types.Op: ...


@_wraps(stmts.P1)
def p1() -> types.Op: ...


@_wraps(stmts.Sn)
def spin_n() -> types.Op: ...


@_wraps(stmts.Sp)
def spin_p() -> types.Op: ...


@_wraps(stmts.U3)
def u(theta: float, phi: float, lam: float) -> types.Op: ...


@_wraps(stmts.PauliString)
def pauli_string(*, string: str) -> types.Op: ...


# stdlibs
@_ir.dialect_group(_structural_no_opt.add(dialect))
def op(self):
    def run_pass(method):
        pass

    return run_pass


@op
def rx(theta: float) -> types.Op:
    """Rotation X gate."""
    return rot(x(), theta)


@op
def ry(theta: float) -> types.Op:
    """Rotation Y gate."""
    return rot(y(), theta)


@op
def rz(theta: float) -> types.Op:
    """Rotation Z gate."""
    return rot(z(), theta)


@op
def cx() -> types.Op:
    """Controlled X gate."""
    return control(x(), n_controls=1)


@op
def cy() -> types.Op:
    """Controlled Y gate."""
    return control(y(), n_controls=1)


@op
def cz() -> types.Op:
    """Control Z gate."""
    return control(z(), n_controls=1)


@op
def ch() -> types.Op:
    """Control H gate."""
    return control(h(), n_controls=1)


@op
def cphase(theta: float) -> types.Op:
    """Control Phase gate."""
    return control(phase(theta), n_controls=1)
