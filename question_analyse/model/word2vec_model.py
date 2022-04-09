import pandas as pd
import numpy as np
import jieba as jb
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import  pad_sequences
from keras .models import  Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers.convolutional import  Conv1D
from keras.layers.convolutional import  MaxPooling1D
import keras
from keras .models import load_model

excel_file = "../../crwal/data/question_answer.xlsx"

# 读取数据
data = pd.read_excel(excel_file)
# print(read_file)
# questions = read_file['问题'].values



