from typing import *
from .cursor import Cursor
from datetime import datetime
from .scalar import Scalar
import sys


class LogWriter:
    """
    This class makes an object that is bound to a run row in the result table. This means that everything that is
    logged through this object is added into the result table and this object can be used to interact with a specific
    run. This object is single use. This means that once the final results are written, the object becomes read-only.

    You should not instantiate this class directly, but use the ResultTable class to create it instead.

    """
    def __init__(self, db_path, run_id: int, start: datetime, flush_each: int = 10, keep_each: int = 1):
        """
        :param db_path: The path to the database file
        :param run_id: The run id of this run
        :param start: The start time of this run
        :param flush_each: Every how many logs should we write them to the database. (increase it to reduce io)
        :param keep_each: Every how many logs datapoint should we store. The others will be discarted. If 2, only one
        datapoint every two times the add_scalar method is called will be stored.
        """
        if keep_each <= 0:
            raise ValueError("Parameter keep_each must be grater than 0: {1, 2, 3, ...}")
        if flush_each <= 0:
            raise ValueError("Parameter keep_each must be grater than 0: {1, 2, 3, ...}")
        self.db_path = db_path
        self.run_id = run_id
        self.start = start
        self.flush_each = flush_each
        self.keep_each = keep_each
        self.global_step = {}
        self.buffer = {}
        self.log_count = {}
        self.enabled = True
        self.run_rep = 0

        # Set the exception handler to set the status to failed and disable the logger if the program crashes
        self._exception_handler()

    def new_repetition(self):
        """
        Create a new repetition of the current run. This is useful if you want to log multiple repetitions of the same
        run. This is a mutating method, meaning that you can call it at the end of the training loop before the next
        full training loop is run again.
        :return: None
        """
        # Start by flushing the buffer
        for tag in self.buffer.keys():
            self._flush(tag)

        self.run_rep += 1

        # Reset the writer
        self.log_count = {}
        self.global_step = {}
        self.start = datetime.now()

    def add_scalar(self, tag: str, scalar_value: Union[float, int],
                   step: Optional[int] = None, epoch: Optional[int] = None,
                   walltime: Optional[float] = None, flush: bool = False):
        """
        Add a scalar to the resultTable
        :param tag: The tag, formatted as: 'split/name' or simply 'split'
        :param scalar_value: The value
        :param step: The global step. If none, the one calculated is used
        :param epoch: The epoch. If None, none is saved
        :param walltime: Override the wall time with this
        :param flush: Force flush all the scalars in memory
        :return: None
        """
        if not self.enabled:
            raise RuntimeError("The LogWriter is read only! This might be due to the fact that you loaded an already"
                               "existing one or you reported final metrics.")
        # Early return if we are not supposed to keep this run.
        if not self._keep(tag):
            return

        # We split the tag as a split and a name for readability
        splitted_tag = tag.split("/")
        if len(splitted_tag) == 2:
            split, name = splitted_tag[0], splitted_tag[1]
        else:
            split, name = "", splitted_tag[0]

        scalar_value = float(scalar_value)  # Cast it as float

        step = self._get_global_step(tag) if step is None else step

        walltime = (datetime.now() - self.start).total_seconds() if walltime is None else walltime

        epoch = 0 if epoch is None else epoch

        # Added a row to table logs
        self._log(tag, epoch, step, split, name, scalar_value, walltime, self.run_rep)

        # Flush all if requested to force flush
        self._flush_all()

    def read_scalar(self, tag) -> List[Scalar]:
        """
        Read a scalar from the resultTable with the given tag
        :param tag: The tag to read formatted as: 'split/name' or simply 'split'.
        :return: A list of Scalars items
        """
        splitted_tag = tag.split("/")
        if len(splitted_tag) == 2:
            split, name = splitted_tag[0], splitted_tag[1]
        else:
            split, name = "", splitted_tag[0]

        with self._cursor as cursor:
            cursor.execute("SELECT * FROM Logs WHERE run_id=? AND split=? AND label=?", (self.run_id, split, name))
            # cursor.execute("SELECT * FROM Logs", (self.run_id, split, name))
            rows = cursor.fetchall()
            return [Scalar(*row[1:]) for row in rows]

    def add_hparams(self, **kwargs):
        """
        Add hyperparameters to the result table
        :param kwargs: The hyperparameters to save
        :return: None
        """

        # Prepare the data to save
        query = "INSERT INTO Results (run_id, metric, value, is_hparam) VALUES (?, ?, ?, ?)"
        data = [(self.run_id, key, value, True) for key, value in kwargs.items()]
        with self._cursor as cursor:
            cursor.executemany(query, data)

    def get_hparams(self) -> Dict[str, Any]:
        """
        Get the hyperparameters of the current run
        :return: A dict of hyperparameters
        """
        with self._cursor as cursor:
            cursor.execute("SELECT metric, value FROM Results WHERE run_id=? AND is_hparam=1", (self.run_id,))
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows}

    def get_repetitions(self) -> List[int]:
        """
        Get the all the repetitions ids of the current run
        :return: A list of repetitions ids
        """
        with self._cursor as cursor:
            cursor.execute("SELECT DISTINCT run_rep FROM Logs WHERE run_id=?", (self.run_id,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]

    def write_result(self, **kwargs):
        """
        Log the results of the run to the table, then disable the logger. This means that the logger will be read-only
        after this operation. If you run multiple iterations, consider writing the results only once all the runs are
        finished. You can aggregate the different metrics before passing them.
        :param kwargs: The metrics to save
        :return: None
        """
        # Start by flushing the buffer
        self._flush_all()

        # Then, prepare the data to save
        query = "INSERT INTO Results (run_id, metric, value, is_hparam) VALUES (?, ?, ?, ?)"
        data = [(self.run_id, key, value, False) for key, value in kwargs.items()]
        with self._cursor as cursor:
            cursor.executemany(query, data)

        # Set the status to finished
        self.set_status("finished")

        # Disable the logger
        self.enabled = False

    def set_status(self, status: Literal["running", "finished", "failed"]):
        """
        Manually set the status of the run
        :param status: The status to set
        :return: None
        """
        if status not in ["running", "finished", "failed"]:
            raise ValueError("Status must be one of: running, finished, failed")
        with self._cursor as cursor:
            cursor.execute("UPDATE Experiments SET status=? WHERE run_id=?", (status, self.run_id))

    @property
    def status(self) -> str:
        """
        Get the status of the run
        :return: The status of the run
        """
        with self._cursor as cursor:
            cursor.execute("SELECT status FROM Experiments WHERE run_id=?", (self.run_id,))
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError(f"Run {self.run_id} does not exist.")
            return row[0]

    @property
    def scalars(self) -> List[str]:
        """
        Return the tags of all scalars logged in the run
        """
        # We need to format the tags as Split/Label
        # If split is empty, we just return the label
        rows = [(row[0] + "/" + row[1]) if row[0] != "" else row[1] for row in self.formatted_scalars]
        return rows

    @property
    def formatted_scalars(self) -> List[Tuple[str, str]]:
        """
        Return the scalars values as split and label
        """
        with self._cursor as cursor:
            cursor.execute("SELECT DISTINCT split, label FROM Logs WHERE run_id=?", (self.run_id,))
            rows = cursor.fetchall()
            # We need to format the tags as Split/Label
            # If split is empty, we just return the label
            return [(row[0], row[1]) for row in rows]

    def __getitem__(self, tag):
        """
        Get the scalar values for a given tag.
        """
        return self.read_scalar(tag)

    def _get_global_step(self, tag):
        """
        Keep track of the global step for each tag.
        :param tag: The tag to get the step
        :return: The current global step
        """
        if tag not in self.global_step:
            self.global_step[tag] = 0

        out = self.global_step[tag]
        self.global_step[tag] += 1
        return out

    def _log(self, tag: str, epoch: int, step: int, split: str, name: str, scalar_value: float, walltime: float,
             run_rep: int):
        """
        Store the scalar log into the buffer, and flush the buffer if it is full.
        :param tag: The tag
        :param epoch: The epoch
        :param step: The step
        :param split: The split
        :param name: The name
        :param scalar_value: The value
        :param walltime: The wall time
        :param run_rep: The run repetition
        :return: None
        """
        if tag not in self.buffer:
            self.buffer[tag] = []
        self.buffer[tag].append((self.run_id, epoch, step, split, name, scalar_value, walltime, run_rep))

        if len(self.buffer[tag]) >= self.flush_each:
            self._flush(tag)

    def _flush_all(self):
        """
        Flush all buffers.
        :return: None
        """
        for tag in self.buffer.keys():
            self._flush(tag)

    def _flush(self, tag: str):
        """
        Flush the scalar values into the db and reset the buffer.
        :param tag: The tag to flush
        :return: None
        """
        query = """
                INSERT INTO Logs (run_id, epoch, step, split, label, value, wall_time, run_rep)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
        with self._cursor as cursor:
            cursor.executemany(query, self.buffer[tag])

        # Reset the buffer
        self.buffer[tag] = []

    def _keep(self, tag: str) -> bool:
        """
        Assert if we need to record this log or drop it. Depends on the kep_each attribute
        :param tag: The tag
        :return: True if we need to keep it and False if we drop it
        """
        if tag not in self.log_count:
            self.log_count[tag] = 0
        self.log_count[tag] += 1
        if self.log_count[tag] >= self.keep_each:
            self.log_count[tag] = 0
            return True
        else:
            return False

    def _exception_handler(self):
        """
        Set the exception handler to set the status to failed and disable the logger if the program crashes
        """
        previous_hooks = sys.excepthook
        def handler(exc_type, exc_value, traceback):
            # Set the status to failed
            self.set_status("failed")
            # Disable the logger
            self.enabled = False

            # Call the previous exception handler
            previous_hooks(exc_type, exc_value, traceback)

        # Set the new exception handler
        sys.excepthook = handler

    @property
    def _cursor(self):
        return Cursor(self.db_path)