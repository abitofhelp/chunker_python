import argparse
import asyncio
import pathlib
import sys
import timeit

import humanize

from pkg.fileio.async_file_chunker import AsyncFileChunker


async def validate_file_path(file_path):
    """
    Validates whether the provided file path exists and is indeed a file. This
    function checks that the given path corresponds to an existing file. If the
    path does not exist or is not associated with a file, the appropriate
    exception is raised.

    :param file_path: The path to the file that needs validation
    :type file_path: pathlib.Path
    :raises FileNotFoundError: If the file does not exist
    :raises ValueError: If the path is not a file
    :return: None
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist")
    if not file_path.is_file():
        raise ValueError(f"'{file_path}' is not a file")


################################################################################
#                             M  A  I  N  L  I  N  E                           #
################################################################################
async def main():
    """
    Main entry point for processing a file in byte chunks asynchronously.

    This function sets up argument parsing for file path input and initializes the
    chunking process using the AsyncFileChunker class. It also measures the time
    taken for processing and outputs the elapsed time in microseconds. In case of
    errors, it gracefully handles expected exceptions such as `FileNotFoundError`
    and `ValueError`.

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the file path is invalid or cannot be processed.
    :return: None.
    """
    parser = argparse.ArgumentParser(description="CHUNKER: File processing in BYTES!")
    parser.add_argument("file_path", type=pathlib.Path, help="The file to process")
    args = parser.parse_args()

    try:
        await validate_file_path(args.file_path)
        processor = AsyncFileChunker()

        start_time = timeit.default_timer()
        await processor.process_file(args.file_path)
        end_time = timeit.default_timer()

        print(f"Elapsed: {humanize.scientific(round((end_time - start_time) * 1e6, 3))} µs")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
