import pytest

from app.talk import Talk


@pytest.mark.run(order=1)
@pytest.mark.parametrize("test_input",
                         [r"Привет! Как тебя зовут?",
                          r"Кто ты такой?",
                          r"Как твои дела?",
                          r"Чем занимаешься?",
                          r"Кто твой создатель?",
                          r"Снятся ли Андроидам электроовцы?"])
def test_conversation(test_input):
    talk = Talk()
    answer = talk.answer(test_input)
    assert answer != ""


@pytest.mark.run(order=5)
def test_history():
    talk = Talk()
    assert len(talk.history) > 2


if __name__ == '__main__':
    pytest.main()
