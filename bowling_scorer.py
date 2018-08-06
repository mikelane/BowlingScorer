from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

from log import get_logger

logger = get_logger(__name__)


class InvalidRoll(Exception):
    pass


@dataclass()
class Game:
    rolls: str = ''
    running_totals: List[int, ...] = field(init=False, default_factory=list)
    frame_results: List[int, ...] = field(init=False, default_factory=list)

    def __post_init__(self):
        """Basic validation of the rolls string followed by
        construction of the running_totals and frame_results lists
        based on that rolls str.
        """
        if not re.fullmatch(r'[0-9/X]{0,21}', self.rolls):
            logger.error(f'Roll string {self.rolls} does not appear to be valid')
            raise InvalidRoll(f'Roll string {self.rolls} does not appear to be valid')

        self.__set_frame_results()
        self.__calculate_running_totals()

    def __set_frame_results(self) -> None:
        pass

    def __calculate_running_totals(self) -> None:
        self.running_totals.append(0)
        pass

    def __game_over(self) -> bool:
        pass

    @property
    def score(self):
        return self.running_totals[-1]
