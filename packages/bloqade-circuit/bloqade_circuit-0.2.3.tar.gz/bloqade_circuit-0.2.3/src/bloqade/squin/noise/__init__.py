# Put all the proper wrappers here

from kirin.lowering import wraps as _wraps

from bloqade.squin.op.types import Op

from . import stmts as stmts


@_wraps(stmts.PauliError)
def pauli_error(basis: Op, p: float) -> Op: ...


@_wraps(stmts.PPError)
def pp_error(op: Op, p: float) -> Op: ...


@_wraps(stmts.Depolarize)
def depolarize(n_qubits: int, p: float) -> Op: ...


@_wraps(stmts.PauliChannel)
def pauli_channel(n_qubits: int, params: tuple[float, ...]) -> Op: ...


@_wraps(stmts.QubitLoss)
def qubit_loss(p: float) -> Op: ...
