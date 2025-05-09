import asyncio

import aiofiles
import humanize

from pkg.atomics import atomic_counter


class AsyncFileChunker:
    """
    Provides asynchronous file chunking and processing.

    This class is designed to read files in chunks asynchronously, perform processing
    on each chunk, and maintain metrics related to the number of chunks processed
    and total bytes read. It is suitable for handling large files that might not
    fit into memory by processing them in smaller, consistent chunks.

    :ivar chunk_counter: Counter to track the number of processed chunks.
    :type chunk_counter: atomic_counter.AtomicCounter
    :ivar total_bytes: Counter to track the total number of processed bytes.
    :type total_bytes: atomic_counter.AtomicCounter
    """
    DEFAULT_CHUNK_SIZE = 8192
    PROCESS_DELAY_SECONDS = 0.1

    def __init__(self):
        self.chunk_counter = atomic_counter.AtomicCounter()
        self.total_bytes = atomic_counter.AtomicCounter()

    async def process_file(self, file_path, chunk_size=DEFAULT_CHUNK_SIZE):
        """
        Asynchronously processes a file by reading its content in chunks and performing
        custom operations on each chunk. Updates internal metrics based on the size
        of the chunks processed.

        :param file_path: Full path to the file to be processed.
        :type file_path: str
        :param chunk_size: Size of each chunk to read from the file in bytes. Defaults
            to DEFAULT_CHUNK_SIZE.
        :type chunk_size: int
        :return: None
        :rtype: None
        :raises FileNotFoundError: If the specified file does not exist.
        :raises PermissionError: If the file cannot be accessed due to permission issues.
        :raises Exception: For any other errors encountered during file processing.
        """
        try:
            async with aiofiles.open(file_path, 'rb') as file:
                while chunk := await file.read(chunk_size):
                    await self._process_single_chunk(chunk)
                    self._update_metrics(len(chunk))
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except PermissionError:
            print(f"Permission denied accessing file: {file_path}")
        except Exception as e:
            print(f"Error processing file: {str(e)}")

    async def _process_single_chunk(self, chunk):
        """
        Processes a single chunk with a specified delay.

        This asynchronous method processes a single given chunk and introduces a
        delay determined by the `PROCESS_DELAY_SECONDS` attribute before continuing.

        :param chunk: The chunk to be processed.
        :type chunk: Any
        :return: None
        :rtype: None
        """
        await asyncio.sleep(self.PROCESS_DELAY_SECONDS)

    def _update_metrics(self, chunk_length):
        """
        Updates the internal metrics for tracking data processing. This method increments
        the total byte count, updates the chunk counter, and displays processing progress
        based on the current chunk length.

        :param chunk_length: Length of the data chunk that has been processed
        :type chunk_length: int
        :return: None
        """
        self.total_bytes.increment(chunk_length)
        self.chunk_counter.increment()
        self._display_progress(chunk_length)

    def _display_progress(self, chunk_length):
        """
        Displays the progress of data processing in a formatted output. This method
        prints the processed chunks and total bytes processed using a human-readable
        format for better visibility.

        :param chunk_length: The length of the current chunk being processed.
        :type chunk_length: int
        :return: None
        """
        print(
            f"Processed[{humanize.intcomma(self.chunk_counter.get()):>4}]:"
            f"{humanize.intcomma(chunk_length):>6}B / "
            f"{humanize.intcomma(self.total_bytes.get()):>10}B"
        )
