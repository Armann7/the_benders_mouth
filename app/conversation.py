from dataclasses import dataclass
import random
import logging
from typing import Optional
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
    history = list()

    __instance = None
    __tokenizer = AutoTokenizer.from_pretrained(config.DATA_GPT2)
    __model = AutoModelForCausalLM.from_pretrained(config.DATA_GPT2)
    __chat_history_tensor = Optional[torch.Tensor]
    __log = logging.getLogger("Conversation")

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
        bot_input_tensor = torch.cat([self.__chat_history_tensor, phrase_tensor], dim=-1)

        # generated a response
        self.__chat_history_tensor = self.__model.generate(
            bot_input_tensor,
            num_return_sequences=1,
            max_length=512,
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
        text_answer = self.__tokenizer.decode(self.__chat_history_tensor[:, bot_input_tensor.shape[-1]:][0],
                                              skip_special_tokens=True)
        self.history.insert(0, Line(text_phrase, text_answer))
        self.__log.info("Answer: {text}".format(text=text_answer))
        return text_answer

    @classmethod
    def init(cls):
        cls.__chat_history_tensor = torch.clone(cls.__make_init_tensor())

    def __new__(cls, *args, **kwargs):
        """
        Реализуем синглтон
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
            cls.init()
        return cls.__instance

    @classmethod
    def __encode_phrase(cls, text: str) -> torch.Tensor:
        """
        Закодировать фразу в виде тензора
        :param text:
        :return:
        """
        line = f"|0|{cls.__get_length_param()}|{text}{cls.__tokenizer.eos_token}|1|1|"
        cls.__log.info("Parameters: {line}".format(line=line))
        return cls.__tokenizer.encode(line, return_tensors="pt")

    @classmethod
    def __encode_answer(cls, text: str) -> torch.Tensor:
        """
        Закодировать ответную фразу в виде тензора
        :param text:
        :return:
        """
        line = f"|1|{cls.__get_length_param()}|{text}{cls.__tokenizer.eos_token}|1|1|"
        return cls.__tokenizer.encode(line, return_tensors="pt")

    @classmethod
    def __make_init_tensor(cls) -> torch.Tensor:
        """
        Инициализируем диалог - чтобы Бендер знал свое имя.
        :return:
        """
        line = "Как тебя зовут?"
        phrase_tensor = cls.__encode_phrase(line)
        line = "Меня зовут Bender"
        answer_tensor = cls.__encode_answer(line)
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
