import shap
import torch


# pricing/ml_correction/shap_explainer.py
class SHAPExplainer:

    def generate_report(self) -> dict:
        """Model explainability for front office"""
        # Add to existing class
    def generate_report(self) -> Path:
    
    plt = shap.summary_plot(self.shap_values, self.features)
    plt.savefig("reports/shap_summary.pdf")
    return Path("reports/shap_summary.pdf")
        return {
            "R²": self.calculate_r_squared(),
            "Feature Contributions": self.get_feature_importances(),
            "FINMA_Compliance": "VAL_303"
        }

class SwissSHAPExplainer:
    """FINMA-compliant model explainability for NN corrections"""
    
    def __init__(self, model, background_data):
        self.explainer = shap.DeepExplainer(
            model, 
            torch.Tensor(background_data)
        )
    
    def generate_report(self, sample: torch.Tensor) -> dict:
        """Produces auditable feature attribution"""
        shap_values = self.explainer.shap_values(sample)
        return {
            "feature_names": ["moneyness", "T", "volume", "vix", "base_iv"],
            "shap_values": shap_values[0].tolist(),
            "base_value": self.explainer.expected_value[0].item()
        }
    
    def save_plot(self, sample: torch.Tensor, filepath: str):
        """PDF output for compliance"""
        shap_values = self.explainer.shap_values(sample)
        shap.save_html(filepath, shap.force_plot(
            self.explainer.expected_value[0], 
            shap_values[0], 
            sample
        ))