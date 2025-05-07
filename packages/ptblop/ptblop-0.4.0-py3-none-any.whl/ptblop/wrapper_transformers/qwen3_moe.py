import sys
from typing import Any, Optional

import torch
import transformers  # type: ignore
from transformers.modeling_flash_attention_utils import (  # type: ignore
    FlashAttentionKwargs,
)

from .. import prunable_block
from . import common

# from transformers.processing_utils import Unpack  # type: ignore


if sys.version_info >= (3, 11):
    from typing import Unpack
else:
    from typing_extensions import Unpack


class PrunableQwen3MoeBlock(torch.nn.Module, prunable_block.PrunableBlock):

    def get_unused_layer_names(self) -> set[str]:
        unused_layer_names = set()
        if not self.use_attention:
            unused_layer_names.add("input_layernorm")
            unused_layer_names.add("self_attn")
        if not self.use_mlp:
            unused_layer_names.add("mlp")
            unused_layer_names.add("post_attention_layernorm")
        return unused_layer_names

    @classmethod
    def fix_root_model(cls, root_model: torch.nn.Module) -> None:
        common.fix_root_model_attention_indices(root_model)

    def __init__(
        self,
        original_module: transformers.models.qwen3.modeling_qwen3.Qwen3DecoderLayer,
        use_attention: bool = True,
        use_mlp: bool = True,
        set_unused_layers_to_none: bool = True,
    ):
        torch.nn.Module.__init__(self)

        self.hidden_size = original_module.hidden_size
        self.self_attn = original_module.self_attn
        self.mlp = original_module.mlp
        self.input_layernorm = original_module.input_layernorm
        self.post_attention_layernorm = original_module.post_attention_layernorm
        # Called at the end sice it sets the unused layers to None automatically
        prunable_block.PrunableBlock.__init__(
            self,
            original_module=original_module,
            use_attention=use_attention,
            use_mlp=use_mlp,
            set_unused_layers_to_none=set_unused_layers_to_none,
        )

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[tuple[torch.Tensor]] = None,
        output_attentions: Optional[bool] = False,
        output_router_logits: Optional[bool] = False,
        use_cache: Optional[bool] = False,
        cache_position: Optional[torch.LongTensor] = None,
        position_embeddings: Optional[
            tuple[torch.Tensor, torch.Tensor]
        ] = None,  # necessary, but kept here for BC
        **kwargs: Unpack[FlashAttentionKwargs],
    ) -> tuple[torch.Tensor] | tuple[torch.Tensor, Any] | tuple[torch.Tensor, Any, Any]:

        if self.use_attention:
            out = self.input_layernorm(hidden_states)

            out, self_attn_weights = self.self_attn(
                hidden_states=out,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_value=past_key_value,
                output_attentions=output_attentions,
                use_cache=use_cache,
                cache_position=cache_position,
                position_embeddings=position_embeddings,
            )
            hidden_states = hidden_states + out
        else:
            self_attn_weights = None

        if self.use_mlp:
            out = self.post_attention_layernorm(hidden_states)
            out = self.mlp(out)
            if isinstance(out, tuple):
                out, router_logits = out
            else:
                router_logits = None

            hidden_states = hidden_states + out
        else:
            router_logits = None
        outputs: (
            tuple[torch.Tensor]
            | tuple[torch.Tensor, Any]
            | tuple[torch.Tensor, Any, Any]
        ) = (hidden_states,)

        if output_attentions:
            outputs = (
                *outputs,
                self_attn_weights,
            )

        if output_router_logits:
            outputs = (
                *outputs,
                router_logits,
            )

        return outputs
