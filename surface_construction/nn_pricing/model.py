import torch
import torch.nn as nn

class VolatilityNN(nn.Module):
    """3-layer LSTM for volatility surface correction"""
    def __init__(self, input_dim=5):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, 32, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        
    def forward(self, x):
        # x: [batch, seq_len, features]
        _, (h_n, _) = self.lstm(x)
        return self.fc(h_n[-1])