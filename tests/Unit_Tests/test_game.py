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


class TestGame():
    @pytest.mark.parametrize('scores,result', test_data)
    def test_game(self, scores: str, result: int) -> None:
        logger.debug(f'Game({scores}) result: {bowling_scorer.Game(scores).score}, expected: {result}')
        assert bowling_scorer.Game(scores).score == result

    @pytest.mark.parametrize('scores', test_invalid_data)
    def test_invalid(self, scores:str) -> None:
        with pytest.raises(bowling_scorer.InvalidRoll):
            bowling_scorer.Game(scores)

    def test_set_frames(self):
        game = bowling_scorer.Game('')
        game.frames('X')
        assert game.frames == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
