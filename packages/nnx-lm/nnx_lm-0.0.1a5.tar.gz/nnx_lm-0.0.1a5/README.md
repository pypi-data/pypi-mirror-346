# nnx-lm: A portable, pip-installable CLI for running LLMs via JAX on any hardware backend.

```
pip install nnx-lm==0.0.1a5
import nnxlm
new_str, new_ids = nnxlm.generate(model_id='Qwen/Qwen3-0.6B', model_cls=nnxlm.Qwen3ForCausalLM, enable_thinking=False, use_chat_template=False)
```
