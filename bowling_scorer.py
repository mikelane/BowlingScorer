from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Union

from log import get_logger

logger = get_logger(__name__)

# Define the GameCard type for convenience
Frame = Dict[int, Optional[Union[int, str]]]
GameCard = Dict[int, Frame]
Roll = Dict[int, Union[None, int, str]]


class InvalidRoll(Exception):
    pass


@dataclass()
class Game:
    rolls: str = ''
    running_totals: List[int, ...] = field(init=False, default_factory=list)
    __frame_results: GameCard = field(init=False, default_factory=dict)
    frame_scores: List[int, ...] = field(init=False, default_factory=list)
    game_over: bool = field(init=False, default=False)
    shot: int = field(init=False, default=1)
    frame: int = field(init=False, default=1)

    def __post_init__(self):
        """Basic validation of the rolls string followed by
        construction of the running_totals and frame_results lists
        based on that rolls str.
        """
        if not re.fullmatch(r'[0-9/X]{0,21}', self.rolls):
            logger.error(f'Roll string {self.rolls} does not appear to be valid')
            raise InvalidRoll(f'Roll string {self.rolls} does not appear to be valid')

        self.frame_results: Dict[int, Roll] = {
            1: {1: None, 2: None},
            2: {1: None, 2: None},
            3: {1: None, 2: None},
            4: {1: None, 2: None},
            5: {1: None, 2: None},
            6: {1: None, 2: None},
            7: {1: None, 2: None},
            8: {1: None, 2: None},
            9: {1: None, 2: None},
            10: {1: None, 2: None, 3: None}
        }
        self.__calculate_running_totals()

    def __calculate_running_totals(self) -> None:
        self.running_totals = [0]
        pass

    def add_roll(self, roll: str) -> None:
        """Add the incoming roll to the game card, validating as we go."""

        # Fail quickly if possible
        if self.shot == 1 and roll == '/':
            raise InvalidRoll('The first shot of a frame cannot be a spare')
        if self.frame == 10 and self.shot == 3 and roll == '/':
            raise InvalidRoll('The third shot of the 10th frame cannot be a spare.')
        if self.frame != 10 and self.shot == 2 and roll == 'X':
            raise InvalidRoll('The second shot of frames 1-9 cannot be a strike')
        if self.frame == 10 and self.shot == 2 and roll == 'X' and self.frame_results[10][1] != 'X':
            raise InvalidRoll('The second shot of frame 10 can only be a strike if the first shot was a strike.')

        if self.shot == 1:
            if roll == 'X':
                logger.debug(f'frame {self.frame}: Strike!')
                self.frame_results[self.frame][1] = 'X'
                if self.frame != 10:
                    self.frame += 1
                else:
                    self.shot += 1
            else:  # roll is 0-9
                logger.debug(f'frame {self.frame}, shot 1: {roll}')
                self.frame_results[self.frame][1] = int(roll)
                self.shot += 1
        elif self.shot == 2:
            if roll == 'X':
                logger.debug(f'frame {self.frame}, shot 2: Strike!')
                self.frame_results[self.frame][2] = 'X'
                self.shot += 1
            elif roll == '/':
                logger.debug(f'frame {self.frame}, shot 2: Spare!')
                self.frame_results[self.frame][2] = '/'
                if self.frame == 10:
                    logger.debug('Spare in frame 10, roll 2. Roll once more.')
                    self.shot += 1
                else:
                    logger.debug(f'Spare in frame {self.frame}. Moving to the next frame.')
                    self.frame += 1
                    self.shot = 1
            elif 0 <= int(roll) + self.frame_results[self.frame][1] <= 9:
                logger.debug(
                    f'frame {self.frame}, shot {self.shot}: {int(roll) + self.frame_results[self.frame][1]} pins. Nice try.')
                self.frame_results[self.frame][2] = int(roll)
                self.frame += 1
                self.shot = 1
            else:  # number of pins doesn't add up
                raise InvalidRoll(
                    f'Frame {self.frame} shot 1 was {self.frame_results[self.frame][1]} so shot 2 must be between 0 and {9 - self.frame_results[self.frame][1]} or /. Got {roll}')
        else:
            if self.shot != 3:
                raise ValueError(f'ERROR: Something went wrong. Shot is {self.shot} not 3')
            if self.frame != 10:  # shot == 3
                raise ValueError(f'ERROR: Something went wrong. Shot is 3 but frame is {self.frame}, not 10')
            # frame 10, shot 3 only happens when there is a strike or spare in frame 10, shot 2
            if self.frame_results[10][2] not in 'X/':
                raise InvalidRoll('You can only roll in frame 10, shot 3 if you rolled a spare or strike in shot 2')

            # frame 10, shot 3
            if roll == 'X':
                logger.debug(f'Finished strong with a strike.')
                self.frame_results[10][3] = 'X'
            else:  # We already know it can't be a spare
                logger.debug(f'Nice try. Last shot {roll}')
                self.frame_results[10][3] = int(roll)

        @property
        def score(self):
            return self.running_totals[-1]
