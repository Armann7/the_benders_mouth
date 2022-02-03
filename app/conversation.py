from dataclasses import dataclass
import random
import logging
from datetime import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import config


@dataclass
class Line:
    phrase: str
    answer: str
    timestamp = datetime.now()


class Conversation:
    """
    Разговор
    """
    __instance = None

    # history = list()
    # __tokenizer = AutoTokenizer.from_pretrained(config.DATA_GPT2)
    # __model = AutoModelForCausalLM.from_pretrained(config.DATA_GPT2)
    # __chat_history_tensor = Optional[torch.Tensor]
    # __log = logging.getLogger("Conversation")

    def __init__(self):
        # Хотя у нас и синглтон, однако конструктор вызывается при каждой попытке создания объекта
        if "history" not in self.__dict__:
            self.history = list()
            self.__log = logging.getLogger("Conversation")
            self.__tokenizer = AutoTokenizer.from_pretrained(config.DATA_GPT2)
            self.__model = AutoModelForCausalLM.from_pretrained(config.DATA_GPT2)
            self.__chat_history_tensor = torch.clone(self.__make_init_tensor())

    def answer(self, phrase: str) -> str:
        """
        Ответ на заданный вопрос
        :param phrase:
        :return:
        """
        text_phrase = phrase.strip()
        self.__log.info("Input phrase: {phrase}".format(phrase=text_phrase))
        # encode the new phrase, add parameters and return a tensor in Pytorch
        phrase_tensor = self.__encode_phrase(text_phrase)

        # append the new user input tokens to the chat history
        self.__log.debug("Add new user tokens to the chat history")
        bot_input_tensor = torch.cat([self.__chat_history_tensor, phrase_tensor], dim=-1)

        # generated a response
        self.__log.debug("Generate a response")
        self.__chat_history_tensor = self.__model.generate(
            bot_input_tensor,
            num_return_sequences=1,
            max_length=512,
            # max_length=128,
            early_stopping=True,
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

        # Decode response
        self.__log.debug("Decode a response")
        text_answer = self.__tokenizer.decode(self.__chat_history_tensor[:, bot_input_tensor.shape[-1]:][0],
                                              skip_special_tokens=True)
        self.history.insert(0, Line(text_phrase, text_answer))
        self.__log.info("Answer: {text}".format(text=text_answer))
        return text_answer

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
        line = f"|0|{self.__get_length_param()}|{text}{self.__tokenizer.eos_token}|1|1|"
        self.__log.info("Parameters: {line}".format(line=line))
        return self.__tokenizer.encode(line, return_tensors="pt")

    def __encode_answer(self, text: str) -> torch.Tensor:
        """
        Закодировать ответную фразу в виде тензора
        :param text:
        :return:
        """
        line = f"|1|{self.__get_length_param()}|{text}{self.__tokenizer.eos_token}|1|1|"
        return self.__tokenizer.encode(line, return_tensors="pt")

    def __make_init_tensor(self) -> torch.Tensor:
        """
        Инициализируем диалог - чтобы Бендер знал свое имя.
        :return:
        """
        line = "Как тебя зовут?"
        phrase_tensor = self.__encode_phrase(line)
        line = "Меня зовут Bender"
        answer_tensor = self.__encode_answer(line)
        return torch.cat([phrase_tensor, answer_tensor], dim=-1)

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
        return random.choice(['1', '2', '3'])
