from __future__ import annotations
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field

from time import sleep

import datetime
from typing import Dict, Optional

import rich.progress


class CompletionTimeColumn(rich.progress.ProgressColumn):
    """Renders completion time."""
    def __init__(self) -> None:
        super().__init__()
        self.previous_percentage = 0.0
        self.end_time = datetime.datetime.now()

    def render(self, task: rich.progress.Task) -> rich.progress.Text:
        """Show completion time."""
        if task.start_time is None or task.elapsed is None or task.percentage is None:
            return rich.progress.Text("-:--:--", style="progress.elapsed")

        if task.percentage == 0.0 or task.elapsed == 0.0:
            return rich.progress.Text("-:--:--", style="progress.elapsed")

        if task.percentage != self.previous_percentage:
            total_duration = 100.0 / task.percentage * task.elapsed
            start_time = datetime.datetime.fromtimestamp(task.start_time)
            duration = datetime.timedelta(seconds=int(total_duration))
            self.end_time = start_time + duration
            self.previous_percentage = task.percentage

        return rich.progress.Text(self.end_time.strftime("%a %H:%M:%S"), style="progress.elapsed")


class RemainingTimeColumn(rich.progress.ProgressColumn):
    """Renders remaining time."""
    @dataclass
    class Data:
        previous_percentage: float = 0.0
        remaining_time: float = 0.0
        progress_times: Dict[float, float] = field(default_factory=dict)

    def __init__(self) -> None:
        super().__init__()
        self.data: defaultdict[int, RemainingTimeColumn.Data] = defaultdict(RemainingTimeColumn.Data)

    def _get_median_iteration_time(self, task_id: int) -> float:
        percentages = sorted(self.data[task_id].progress_times.keys())

        if len(percentages) <= 1:
            return float(0.0)

        duration = []
        for index in range(1, len(percentages)):
            percentage_diff = percentages[index] - percentages[index - 1]
            time_diff = (self.data[task_id].progress_times[percentages[index]] -
                         self.data[task_id].progress_times[percentages[index - 1]])
            duration.append(time_diff / percentage_diff)

        return statistics.median(duration)

    def total_time(self, task_id: int) -> float:
        return self._get_median_iteration_time(task_id) * 100.0

    def render(self, task: rich.progress.Task) -> rich.progress.Text:
        """Show remaining time."""
        if task.start_time is None or task.elapsed is None or task.percentage is None:
            return rich.progress.Text("-:--:--", style="progress.remaining")

        if task.percentage == 0.0 or task.elapsed == 0.0:
            return rich.progress.Text("-:--:--", style="progress.remaining")

        if task.percentage != self.data[task.id].previous_percentage:
            self.data[task.id].progress_times[task.percentage] = task.elapsed
            self.data[task.id].remaining_time = max(0.0, self.total_time(task.id) - task.elapsed)
            self.data[task.id].previous_percentage = task.percentage

        # Based on https://github.com/tqdm/tqdm/blob/master/tqdm/std.py
        minutes, seconds = divmod(int(self.data[task.id].remaining_time), 60)
        hours, minutes = divmod(minutes, 60)

        return rich.progress.Text(f'{hours:d}:{minutes:02d}:{seconds:02d}', style="progress.remaining")


COLUMNS = (rich.progress.SpinnerColumn(),
           rich.progress.TextColumn("[progress.description]{task.description}"),
           rich.progress.BarColumn(bar_width=None),
           rich.progress.MofNCompleteColumn(),
           'Elapsed:',
           rich.progress.TimeElapsedColumn(),
           'Remaining:',
           RemainingTimeColumn(),
           'Completion:',
           CompletionTimeColumn())


class RichProgressObject(rich.progress.Progress):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*COLUMNS, *args, **kwargs, get_time=get_time, expand=True)
        self.task_id = self.new_task()

    def _get_tid(self, task_id: Optional[rich.progress.TaskID] = None) -> rich.progress.TaskID:
        return task_id if task_id is not None else self.task_id

    def new_task(self) -> rich.progress.TaskID:
        return self.add_task('Processing...', start=False)

    def start(self, task_id: Optional[rich.progress.TaskID] = None) -> None:
        super().start()
        self.reset(self._get_tid(task_id))

    def stop(self, task_id: Optional[rich.progress.TaskID] = None) -> None:
        self.stop_task(self._get_tid(task_id))
        self.remove_task(self._get_tid(task_id))

    def set_progress_text(self, _txt: str, task_id: Optional[rich.progress.TaskID] = None) -> None:
        self.update(self._get_tid(task_id), description=_txt)
        self.refresh()

    def set_progress_count(self, _progress: int, _total: int, task_id: Optional[rich.progress.TaskID] = None) -> None:
        self.update(self._get_tid(task_id), total=_total, completed=_progress)
        self.refresh()

    def __enter__(self) -> RichProgressObject:
        self.start()
        return self


def get_time() -> float:
    return datetime.datetime.timestamp(datetime.datetime.now())


def simulate() -> None:
    num_iterations = 50
    with RichProgressObject() as progress:
        progress.set_progress_count(0, num_iterations)
        progress.start()
        for _ in range(num_iterations):
            progress.advance(progress.task_id)
            sleep(random.uniform(0.05, 0.35))


if __name__ == "__main__":
    simulate()
