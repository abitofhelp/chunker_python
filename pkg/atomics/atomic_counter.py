import multiprocessing


class AtomicCounter:
    """
    A thread-safe atomic counter.

    This class provides a thread-safe counter implementation that supports
    increment and decrement operations. It ensures atomicity using a
    multiprocessing Lock, making it a suitable choice for scenarios requiring
    thread-safe counter updates, such as multi-threaded or multi-process
    environments.

    :ivar value: A shared multiprocessing value storing the counter's current
        value.
    :type value: multiprocessing.Value
    :ivar lock: A multiprocessing lock utilized to synchronize access and
        maintain thread-safety for the counter operations.
    :type lock: multiprocessing.Lock
    """

    def __init__(self, initial=0):
        self.value = multiprocessing.Value('i', initial)
        self.lock = multiprocessing.Lock()

    def increment(self, num=1):
        """
        Increments the shared value by the specified amount in a thread-safe
        manner using a lock.

        Locks ensure that the increment operation is performed atomically when
        accessing the shared value, preventing potential data corruption in
        multi-threaded scenarios. The method increments the shared integer
        value by the amount defined by the `num` parameter.

        :param num: The amount to add to the shared value. Defaults to 1.
        :type num: int
        :return: None
        """
        with self.lock:
            self.value.value += num

    def decrement(self, num=1):
        """
        Decrements the shared value by a specified amount in a thread-safe manner.

        This method uses a threading lock to ensure that the shared
        value is decremented safely across multiple threads. The decrement
        amount defaults to 1 if not provided explicitly by the user.

        :param num: The amount by which the shared value will be
            decreased. Defaults to 1.
        :return: None
        """
        with self.lock:
            self.value.value -= num

    def get(self):
        """
        Retrieves the current value stored in the `value` attribute, ensuring thread-safe
        access by using a lock.

        :return: The current value stored in the `value` attribute.
        :rtype: Any
        """
        with self.lock:
            return self.value.value
