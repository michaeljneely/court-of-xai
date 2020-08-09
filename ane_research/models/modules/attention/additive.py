"""
Bahdanau et al. 2015 (arXiv 1409.0473) additive attention modules
"""

# pylint: disable=E1101
# pylint incorrectly identifies some types as tuples

import torch
import torch.nn as nn

from ane_research.models.modules.attention.attention import Attention
from ane_research.models.modules.attention.activations import AttentionActivationFunction


@Attention.register('additive_basic')
class AdditiveAttentionBasic(Attention):
    """
    Query-less additive attention module variant as described by Bahdanau et al. 2015 (arXiv 1409.0473)
    Calculates a weight distribution with a feedforward alignment model operating exclusively on a key vector

    Parameters:
        hidden_size (int):
            Input dimensionality of the alignment model
        activation_function (AttentionActivationFunction):
            Attention activation function module
    """
    def __init__(self, hidden_size: int, activation_function: AttentionActivationFunction):
        super().__init__()
        self.activation = activation_function
        self.num_intermediate_features = hidden_size // 2
        self.alignment_layer1 = nn.Linear(hidden_size, self.num_intermediate_features)
        self.alignment_layer2 = nn.Linear(self.num_intermediate_features, 1, bias=False)

    def forward(self, key: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """Compute a weight distribution on the input sequence, (hopefully) assigning higher values to more relevant elements.

        Args:
            key (torch.Tensor): (Batch x Sequence Length x Hidden Dimension)
                The encoded data features. In a BiLSTM, this corresponds to the encoder annotation, h
            mask (torch.Tensor): (Batch x Sequence Length)
                Mask to apply to padded key elements

        Returns:
            torch.Tensor: (Batch x Sequence Length)
                Attention scores
        """
        layer1 = nn.Tanh()(self.alignment_layer1(key))
        layer2 = self.alignment_layer2(layer1).squeeze(-1)
        scores = self.activation(layer2, mask)

        return scores

@Attention.register('additive_query')
class AdditiveAttentionQuery(Attention):
    """
    Full additive attention module variant as described by Bahdanau et al. 2015 (arXiv 1409.0473)
    Calculates a weight distribution with a feedforward alignment model operating on key and query vectors

    Parameters:
        hidden_size (int):
            Input dimensionality of the alignment model
        activation_function (AttentionActivationFunction):
            Attention activation function module
    """
    def __init__(self, hidden_size: int, activation_function: AttentionActivationFunction):
        super().__init__()
        self.activation = activation_function
        self.num_intermediate_features = hidden_size // 2
        self.alignment_layer1_k = nn.Linear(hidden_size, self.num_intermediate_features)
        self.alignment_layer1_q = nn.Linear(hidden_size, self.num_intermediate_features)
        self.alignment_layer2 = nn.Linear(self.num_intermediate_features, 1, bias=False)

    def forward(self, key: torch.Tensor, query: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """Compute a weight distribution on the input sequence, (hopefully) assigning higher values to more relevant elements.

        Args:
            key (torch.Tensor): (Batch x Sequence Length x Hidden Dimension)
                The encoded data features. In a BiLSTM, this corresponds to the encoder annotation, h
            query (torch.Tensor): (Batch x Sequence Length)
                The reference when computing the attention distribution. In a BiLSTM, this corresponds to the decoder hidden state, s
            mask (torch.Tensor): (Batch x Sequence Length)
                Mask to apply to padded key elements

        Returns:
            torch.Tensor: (Batch x Sequence Length)
                Attention scores
        """
        layer1 = nn.Tanh()(self.alignment_layer1_k(key) + self.alignment_layer1_q(query).unsqueeze(1))
        layer2 = self.alignment_layer2(layer1).squeeze(-1)
        scores = self.activation(layer2, mask)

        return scores
