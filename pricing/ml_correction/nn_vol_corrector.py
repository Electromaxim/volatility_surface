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