#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from .embedding_model import *
from .chat_model import *

EmbeddingModel = {
    "Ollama": OllamaEmbed,
    "LocalAI": LocalAIEmbed,
    "OpenAI": OpenAIEmbed,
    "Azure-OpenAI": AzureEmbed,
    "Xinference": XinferenceEmbed,
    "Tongyi-Qianwen": QWenEmbed,
    "ZHIPU-AI": ZhipuEmbed,
    "BaiChuan": BaiChuanEmbed,
    "Jina": JinaEmbed,
    "Bedrock": BedrockEmbed,
    "NVIDIA": NvidiaEmbed,
    "LM-Studio": LmStudioEmbed,
    "TogetherAI": TogetherAIEmbed,
    "PerfXCloud": PerfXCloudEmbed,
    "Upstage": UpstageEmbed,
    "SILICONFLOW": SILICONFLOWEmbed,
    "HuggingFace": HuggingFaceEmbed,
}

ChatModel = {
    "OpenAI": GptTurbo,
    "Azure-OpenAI": AzureChat,
    "ZHIPU-AI": ZhipuChat,
    "Tongyi-Qianwen": QWenChat,
    "Ollama": OllamaChat,
    "LocalAI": LocalAIChat,
    "Xinference": XinferenceChat,
    "Moonshot": MoonshotChat,
    "DeepSeek": DeepSeekChat,
    "VolcEngine": VolcEngineChat,
    "BaiChuan": BaiChuanChat,
    "MiniMax": MiniMaxChat,
    "Bedrock": BedrockChat,
    "OpenRouter": OpenRouterChat,
    "StepFun": StepFunChat,
    "NVIDIA": NvidiaChat,
    "LM-Studio": LmStudioChat,
    "OpenAI-API-Compatible": OpenAI_APIChat,
    "LeptonAI": LeptonAIChat,
    "TogetherAI": TogetherAIChat,
    "PerfXCloud": PerfXCloudChat,
    "Upstage": UpstageChat,
    "novita.ai": NovitaAIChat,
    "SILICONFLOW": SILICONFLOWChat,
    "01.AI": YiChat,
    "HuggingFace": HuggingFaceChat,
}
