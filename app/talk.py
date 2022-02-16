"""
Разговоры
"""
from dataclasses import dataclass
from datetime import datetime

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import config
from utils.logger import LogMixin


@dataclass()
class Line:
    """
    Один обмен фразами - реплика и ответ
    """
    id: int
    phrase: str
    response: str
    timestamp: datetime = datetime.now()

    def __init__(self, phrase, response):
        self.id = 0
        self.phrase = phrase
        self.response = response


class Talk(LogMixin):
    """
    Разговор
    """
    __instance: object = None

    def __init__(self):
        # Хотя у нас и синглтон, однако конструктор вызывается
        # при каждой попытке создания объекта
        if not hasattr(self, "history"):
            super().__init__()
            self.history = []
            self.__id = 0
            self.__tokenizer = AutoTokenizer.from_pretrained(config.DATA_GPT2)
            self.__model = \
                AutoModelForCausalLM.from_pretrained(config.DATA_GPT2)
            self.__chat_history_tensor = torch.clone(self.__make_init_tensor())

    def answer(self, phrase: str) -> str:
        """
        Ответ на заданный вопрос
        :param phrase:
        :return:
        """
        self.__id += 1
        text_phrase = phrase.strip()
        # self.info("Input phrase: {phrase}".format(phrase=text_phrase))
        self.log_info(f"Input phrase: {text_phrase}")
        phrase_tensor = self.__encode_phrase(text_phrase)

        self.log_debug("Add new user tokens to the chat history")
        bot_input_tensor = torch.cat(
            [self.__chat_history_tensor, phrase_tensor], dim=-1)

        self.log_debug("Generate a response")
        self.__chat_history_tensor = self.__model.generate(
            bot_input_tensor,
            num_return_sequences=1,
            max_length=512,
            # max_length=128,
            # early_stopping=True,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.6,
            mask_token_id=self.__tokenizer.mask_token_id,
            eos_token_id=self.__tokenizer.eos_token_id,
            unk_token_id=self.__tokenizer.unk_token_id,
            pad_token_id=self.__tokenizer.pad_token_id,
            device='cpu',
        )

        self.log_debug("Decode a response")
        text_response = self.__tokenizer.decode(
            self.__chat_history_tensor[:, bot_input_tensor.shape[-1]:][0],
            skip_special_tokens=True)

        self.history.insert(0, Line(text_phrase, text_response))
        self.log_info(f"Response: {text_response}")
        return text_response

    def log_info(self, msg: str):
        super().info(f"({self.__id}) {msg}")

    def log_debug(self, msg: str):
        super().debug(f"({self.__id}) {msg}")

    def __new__(cls, *args, **kwargs):
        """
        Реализуем синглтон
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __encode_phrase(self, text: str) -> torch.Tensor:
        """
        Закодировать фразу в виде тензора
        :param text:
        :return:
        """
        eos_token = self.__tokenizer.eos_token
        line = f"|0|{self.__get_length_param()}|{text}{eos_token}|1|1|"
        self.log_info(f"Parameters: {line}")
        return self.__tokenizer.encode(line, return_tensors="pt")

    def __encode_response(self, text: str) -> torch.Tensor:
        """
        Закодировать ответную фразу в виде тензора
        :param text:
        :return:
        """
        eos_token = self.__tokenizer.eos_token
        line = f"|1|{self.__get_length_param()}|{text}{eos_token}|1|1|"
        return self.__tokenizer.encode(line, return_tensors="pt")

    def __make_init_tensor(self) -> torch.Tensor:
        """
        Инициализируем диалог - чтобы Бендер знал свое имя.
        :return:
        """
        line = "Как тебя зовут?"
        phrase_tensor = self.__encode_phrase(line)
        line = "Меня зовут Bender"
        response_tensor = self.__encode_response(line)
        return torch.cat([phrase_tensor, response_tensor], dim=-1)

    @staticmethod
    def __get_length_param() -> str:
        """
        Определяем длину ответа.
        :return:
        1 - короткая фраза
        2 - средняя фраза
        3 - длинная фраза
        - - без ограничения
        """
        # return random.choice(['-', '1', '2', '3'])
        # Генерим только короткие ответы.
        # Иначе на слабом сервере долго работает
        return '1'
