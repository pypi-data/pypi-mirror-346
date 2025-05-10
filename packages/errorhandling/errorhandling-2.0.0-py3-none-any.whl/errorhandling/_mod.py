from typing import Generic, TypeVar

_T = TypeVar("_T")
_E = TypeVar("_E")


class ErrorCode:
	def __init__(self, intvalue: int):
		self._intvalue = intvalue

	@property
	def intvalue(self) -> int:
		return self._intvalue

	@classmethod
	def ok(cls) -> "ErrorCode":
		return ErrorCode(intvalue=0)

	@classmethod
	def err(cls) -> "ErrorCode":
		return ErrorCode(intvalue=1)

	def is_ok(self) -> bool:
		return self._intvalue == 0

	def is_err(self) -> bool:
		return self._intvalue != 0

	def consider(self, other: "ErrorCode | int") -> None:
		if isinstance(other, ErrorCode):
			other = other.intvalue
		self._intvalue += other


class Result:
	class Ok(Generic[_T]):
		# private
		def __init__(
			self,
			obj: _T,
			is_constructor_called_privately: bool = False,
		):
			assert is_constructor_called_privately
			self._obj = obj

		@property
		def obj(self) -> _T:
			return self._obj

		@property
		def is_ok(self) -> bool:
			return True

		@property
		def is_err(self) -> bool:
			return False

	class Err(Generic[_E]):
		# private
		def __init__(
			self,
			obj: _E,
			is_constructor_called_privately: bool = False,
		):
			assert is_constructor_called_privately
			self._obj = obj

		@property
		def obj(self) -> _E:
			return self._obj

		@property
		def is_ok(self) -> bool:
			return False

		@property
		def is_err(self) -> bool:
			return True

	@staticmethod
	def ok(obj: _T) -> "Result.Ok[_T]":
		return Result.Ok(obj=obj, is_constructor_called_privately=True)

	@staticmethod
	def err(obj: _E) -> "Result.Err[_E]":
		return Result.Err(obj=obj, is_constructor_called_privately=True)

	@staticmethod
	def is_ok(result: "Result.Ok[_T]|Result.Err[_E]") -> bool:
		return result.is_ok

	@staticmethod
	def is_err(result: "Result.Ok[_T]|Result.Err[_E]") -> bool:
		return result.is_err
