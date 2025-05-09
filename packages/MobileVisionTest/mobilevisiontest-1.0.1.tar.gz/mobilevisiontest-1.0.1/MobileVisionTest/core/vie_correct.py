from transformers import pipeline
from unidecode import unidecode

class SpellingCorrector:
    def __init__(self, 
                 model1="Frankie202/vietnamese-correction-203", 
                 model2="bmd1905/vietnamese-correction-v2", 
                 max_length=512):
        self.corrector1 = pipeline("text2text-generation", model=model2)
        # self.corrector2 = pipeline("text2text-generation", model=model2) if model2 else None
        self.max_length = max_length
    
    def correct_texts(self, texts):
        """Sửa chính tả cho danh sách text bằng cả hai model."""
        if not texts:
            return []
        
        # Run first model
        predictions1 = self.corrector1(texts, max_length=self.max_length)
        results1 = [pred['generated_text'] for pred in predictions1]
        
        # Run second model (if available)
        # if self.corrector2:
        #     predictions2 = self.corrector2(texts, max_length=self.max_length)
        #     results2 = [pred['generated_text'] for pred in predictions2]
            
        #     # Combine results (e.g., choose the first model's output unless empty)
        #     return [r1 if r1.strip() else r2 for r1, r2 in zip(results1, results2)]
        
        return results1

    def no_accent(self, texts):
            return [unidecode(text) for text in texts]
        