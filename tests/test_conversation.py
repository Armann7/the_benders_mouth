import pytest

from app.conversation import Conversation


@pytest.mark.run(order=1)
@pytest.mark.parametrize("test_input",
                         [r"Привет! Как тебя зовут?",
                          r"Кто ты такой?",
                          r"Как твои дела?",
                          r"Чем занимаешься?",
                          r"Кто твой создатель?",
                          r"Снятся ли Андроидам электроовцы?"])
def test_conversation(test_input):
    conv = Conversation()
    answer = conv.answer(test_input)
    assert answer != ""


@pytest.mark.run(order=2)
def test_history():
    conv = Conversation()
    assert len(conv.history) > 2


if __name__ == '__main__':
    pytest.main()
