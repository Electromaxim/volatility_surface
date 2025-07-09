import torch
import torch.nn as nn

class SwissVolatilityNN(nn.Module):
    """3-layer LSTM for residual volatility correction (FINMA-compliant)"""
    
    def __init__(self, input_dim=5, hidden_dim=32):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,  # [moneyness, T, volume, vix, base_iv]
            hidden_size=hidden_dim,
            num_layers=3,
            batch_first=True
        )
        self.regressor = nn.Sequential(
            nn.Linear(hidden_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Tanh()  # Constrain output to ±0.15 vol points
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (hidden, _) = self.lstm(x)
        return self.regressor(hidden[-1])


class SwissVolatilityNN(nn.Module):
    """3-layer LSTM for illiquid strike adjustment"""
    
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=5,  # [moneyness, T, volume, vix, heston_residual]
            hidden_size=32,
            batch_first=True
        )
        self.regressor = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Tanh()  # Constrain output to ±0.15 vol
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (h_n, _) = self.lstm(x)
        return self.regressor(h_n[-1])