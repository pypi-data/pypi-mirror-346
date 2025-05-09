from collections.abc import Iterator, Sequence
from typing import Generic, TypeVar

from array_api_compat import array_namespace

TArray = TypeVar("TArray")


class AxisBatch(Generic[TArray]):
    """Batch the array along the given axis."""

    def __init__(self, a: TArray, /, *, axis: int | Sequence[int], size: int) -> None:
        """
        Batch the array along the given axis.

        Parameters
        ----------
        a : TArray
            The array to batch.
        axis : int | Sequence[int]
            The axis to batch.
        size : int
            The size of the batch.

        Yields
        ------
        TArray
            The batched arrays.

        Returns
        -------
        Callable[[Sequence[TArray]], TArray]
            The function that concats the batched arrays.

        Usage
        -----
        >>> a = ivy.arange(10)
        >>> b = AxisBatch(a, axis=0, size=3)
        >>> for x in b:
        >>>     b.send(x * 2)
        >>> print(b.value)

        """
        if isinstance(axis, int):
            axis = (axis,)
        self._axis = axis
        self._size = size
        self._axis_len = len(axis)
        xp = array_namespace(a)
        a = xp.moveaxis(a, axis, tuple(range(self._axis_len)))
        self._shape = a.shape  # type: ignore
        self._a = xp.reshape(a, (-1, *self._shape[self._axis_len :]))
        self._results: list[TArray] = []

    def __iter__(self) -> Iterator[TArray]:
        """
        Yield the batched array.

        Yields
        ------
        Iterator[TArray]
            The batched array.

        """
        for i in range(0, self._a.shape[0], self._size):
            yield self._a[i : i + self._size]

    def __len__(self) -> int:
        """
        Return the number of batches.

        Returns
        -------
        int
            The number of batches.

        """
        return len(self._a) // self._size

    def send(self, result: TArray, /) -> None:
        """
        Add the batched array to the results.

        Parameters
        ----------
        result : TArray
            The batched array.

        """
        self._results.append(result)

    @property
    def value(self) -> TArray:
        """
        Return the concentrated batched arrays.

        Returns
        -------
        TArray
            The concentrated batched arrays.

        """
        xp = array_namespace(self._results[0])
        result = xp.concat(self._results, axis=0)
        return xp.moveaxis(result, tuple(range(self._axis_len)), self._axis)
