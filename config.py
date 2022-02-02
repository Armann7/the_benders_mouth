import pathlib
import logging

PROJECT_ROOT = pathlib.Path(__file__).parent
DATA_GPT2 = pathlib.Path(PROJECT_ROOT, 'data_local', 'gpt2')

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
