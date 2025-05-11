from transformers import T5EncoderModel


class T5EncoderModelWrapper(T5EncoderModel):
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        head_mask=None,
        inputs_embeds=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        encoder_outputs = super().forward(
            input_ids,
            attention_mask,
            head_mask,
            inputs_embeds,
            output_attentions,
            output_hidden_states,
            return_dict,
        )
        return encoder_outputs.last_hidden_state[:, 0]
