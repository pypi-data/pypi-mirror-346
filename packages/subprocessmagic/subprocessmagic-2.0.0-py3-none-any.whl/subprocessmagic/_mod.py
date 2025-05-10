import logging
import os
import subprocess
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import IO, Any, Callable, Generator, Iterable, TypeAlias

from errorhandling import ErrorCode

LOG_LEVEL_TYPE: TypeAlias = int
OUTPUT_TYPE: TypeAlias = str


class _Output:
	def __init__(self, log_level: LOG_LEVEL_TYPE, line: OUTPUT_TYPE) -> None:
		"""
		ioi: IO-interface
		"""
		self._log_level: LOG_LEVEL_TYPE = log_level
		self._line: OUTPUT_TYPE = line

	@property
	def log_level(self) -> LOG_LEVEL_TYPE:
		return self._log_level

	@property
	def line(self) -> OUTPUT_TYPE:
		return self._line


_QUEUE_ENDING_FLAG_TYPE: TypeAlias = None
_QUEUE_ENDING_FLAG: _QUEUE_ENDING_FLAG_TYPE = None


class _Pipe:
	def __init__(self, log_level: LOG_LEVEL_TYPE, ioi: IO[OUTPUT_TYPE]) -> None:
		"""
		ioi: IO-interface
		"""
		self._log_level: LOG_LEVEL_TYPE = log_level
		self._ioi: IO[OUTPUT_TYPE] = ioi

	@property
	def log_level(self) -> LOG_LEVEL_TYPE:
		return self._log_level

	@property
	def ioi(self) -> IO[OUTPUT_TYPE]:
		return self._ioi


def _blocking_pipe_reading(queue: Queue[_Output | _QUEUE_ENDING_FLAG_TYPE], pipe: _Pipe):
	try:
		with pipe.ioi:
			# Blocking operation: pipe empty -> block program execution until pipe is not empty
			for line in pipe.ioi:
				queue.put(_Output(log_level=pipe.log_level, line=line))
	finally:
		# Signal for end of queue when looping over it.
		queue.put(_QUEUE_ENDING_FLAG)


def _io_generator(pipes: Iterable[_Pipe]) -> Generator[_Output, None, _QUEUE_ENDING_FLAG_TYPE]:
	out_queue: Queue[_Output | _QUEUE_ENDING_FLAG_TYPE] = Queue()
	thread_list: list[Thread] = [
		Thread(
			target=_blocking_pipe_reading,
			kwargs={
				"queue": out_queue,
				"pipe": _Pipe(log_level=pipe.log_level, ioi=pipe.ioi),
			},
		)
		for pipe in pipes
	]

	# Both operations, the for-loop of the lines in the pipe, and the queue.get, are blocking by default.
	# Hence wait until each thread provides None in the queue.
	for thread in thread_list:
		thread.start()
	try:
		for _ in range(len(thread_list)):
			for output in iter(out_queue.get, _QUEUE_ENDING_FLAG):
				yield output
	# try-finally block is triggered e.g. when user stops execution via CTRL+C
	finally:
		return _QUEUE_ENDING_FLAG


def process(
	command: list[str],
	logger: Callable[[int, str], None] | None = None,
	cwd: Path | None = None,
	env: dict[str, str] | None = None,
) -> ErrorCode:
	process = subprocess.Popen(
		command,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		encoding="utf-8",
		cwd=cwd,
		env=env if env else os.environ,
	)

	pipe_list: list[_Pipe] = []
	if process.stderr is not None:
		pipe_list.append(_Pipe(log_level=logging.ERROR, ioi=process.stderr))
	if process.stdout is not None:
		pipe_list.append(_Pipe(log_level=logging.INFO, ioi=process.stdout))
	generator: Generator[_Output, None, _QUEUE_ENDING_FLAG_TYPE] = _io_generator(pipe_list)

	if logger is None:

		def _log(log_level: LOG_LEVEL_TYPE, msg: OUTPUT_TYPE):
			assert log_level is not None
			print(msg, end="")

		logger = _log
	try:
		while True:
			output = next(generator)
			logger(output.log_level, output.line)
	except StopIteration as _:
		# TODO 2024.11.16 dominicparga check .communicate() vs .wait() https://stackoverflow.com/a/30984882
		# The .communicate() doesn't work, probably because the yield-routine consumes the output.
		return_code = process.wait(timeout=None)
		return ErrorCode(return_code)


def _run(
	command: list[str] | str, cwd: Path | None, env: dict[str, str] | None, is_shell: bool
) -> tuple[str, ErrorCode, str]:
	result: subprocess.CompletedProcess[str] = subprocess.run(
		command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", cwd=cwd, env=env, shell=is_shell
	)
	_input_args: Any = result.args
	return result.stdout, ErrorCode(result.returncode), result.stderr


def run(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> tuple[str, ErrorCode, str]:
	return _run(command=command, cwd=cwd, env=env, is_shell=False)


def shell(command: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> tuple[str, ErrorCode, str]:
	return _run(command=command, cwd=cwd, env=env, is_shell=True)
