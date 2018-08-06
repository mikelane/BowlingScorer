import pytest

import bowling_scorer
import log

logger = log.get_logger(__name__)

test_data = [
    ('', 0),
    ('XXXXXXXXXXXX', 300),
    ('90909090909090909090', 90),
    ('5/5/5/5/5/5/5/5/5/5/5', 150),
    ('X7/729/XXX236/7/3', 168),
    ('00000000000000000000', 0),
    ('01273/X5/7/345400X70', 113),
    ('X7/90X088/06XXX81', 167),
]

test_invalid_data = [
    ('asdf'),
    ('01234567890123456789012')
]

valid_frame_results_data = [
    ('XXXXXXXXXXXX',
     {
         1: {1: 'X', 2: None},
         2: {1: 'X', 2: None},
         3: {1: 'X', 2: None},
         4: {1: 'X', 2: None},
         5: {1: 'X', 2: None},
         6: {1: 'X', 2: None},
         7: {1: 'X', 2: None},
         8: {1: 'X', 2: None},
         9: {1: 'X', 2: None},
         10: {1: 'X', 2: 'X', 3: 'X'}
     }),
    ('X7/729/XXX236/7/3',
     {
         1: {1: 'X', 2: None},
         2: {1: 7, 2: '/'},
         3: {1: 7, 2: 2},
         4: {1: 9, 2: '/'},
         5: {1: 'X', 2: None},
         6: {1: 'X', 2: None},
         7: {1: 'X', 2: None},
         8: {1: 2, 2: 3},
         9: {1: 6, 2: '/'},
         10: {1: 7, 2: '/', 3: 3}
     })
]

invalid_frame_results_data = [
    'X/',
    '/',
    '35/',
    '54545454545454545452/',
    '9X',
    '3434343434343434343X4'
]


class TestGame():
    @pytest.mark.parametrize('rolls,result', test_data)
    def test_game(self, rolls: str, result: int) -> None:
        logger.debug(f'Game({rolls}) result: {bowling_scorer.Game(rolls).score}, expected: {result}')
        assert bowling_scorer.Game(rolls).score == result

    @pytest.mark.parametrize('rolls', test_invalid_data)
    def test_invalid_roll_string(self, rolls: str) -> None:
        with pytest.raises(bowling_scorer.InvalidRoll):
            bowling_scorer.Game(rolls)

    @pytest.mark.parametrize('rolls,frame_result', valid_frame_results_data)
    def test_valid_frame_results(self, rolls: str, frame_result: dict) -> None:
        game = bowling_scorer.Game('')
        for roll in rolls:
            game.add_roll(roll)
        assert game.frame_results == frame_result

    @pytest.mark.parametrize('rolls', invalid_frame_results_data)
    def test_invalid_frame_results(self, rolls: str) -> None:
        game = bowling_scorer.Game('')
        with pytest.raises(bowling_scorer.InvalidRoll):
            for roll in rolls:
                game.add_roll(roll)

    def test_set_frames(self):
        game = bowling_scorer.Game('')
        game.frames('X')
        assert game.frames == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
