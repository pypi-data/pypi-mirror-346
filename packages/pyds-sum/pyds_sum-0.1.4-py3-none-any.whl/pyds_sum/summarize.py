from pathlib import Path
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List
import argparse

from transformers.utils import logging
logging.set_verbosity(40)

class summarizer:
    def __init__(self):
        model_checkpoint = "HuggingFaceTB/SmolLM-360M-Instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForCausalLM.from_pretrained(model_checkpoint)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def read_and_chunk_ipynb(
        self, path: Path, token_chunk_size: int = 2000
    ) -> List[str]:
        """
        Reads Jupyter Notebook (.ipynb) content, extracts code cells, and uses a Hugging Face tokenizer
        to split the code content into chunks of up to token_chunk_size tokens.
        Returns a list of code string chunks for a single file.
        """
        with open(path, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        full_code = ""

        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source_content = cell["source"]
                if isinstance(source_content, list):
                    cell_code = "".join(source_content)
                else:
                    cell_code = source_content

                if len(cell_code) >= 5:
                    full_code += cell_code + "\n"

        tokens = self.tokenizer.encode(full_code, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), round(0.9 * token_chunk_size)):
            chunk_tokens = tokens[i : i + round(0.9 * token_chunk_size)]
            chunk_string = self.tokenizer.decode(
                chunk_tokens, clean_up_tokenization_spaces=True
            )
            chunks.append(chunk_string)

        return chunks

    def summarize(self, path: Path) -> str:
        """Summarize a Python file or parses ipynb to python first then summarizes"""
        try:
            input_text = self.read_and_chunk_ipynb(path)
        except:
            raise ValueError("Invalid file type. Please provide a valid .ipynb file")
        preds = []
        for chunked_input_content in input_text:
            messages = [{"role": "user", "content": f"Summarize the following code in 2 sentences:\\n{chunked_input_content}"}]
            input_for_model = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            chunk_ids = self.tokenizer.encode(
                input_for_model,
                return_tensors="pt",
                truncation=True,
                max_length=2048,
            ).to(self.device)

            output_tokens = self.model.generate(
                chunk_ids,
                max_new_tokens=256,
                temperature=0.2,
                top_p=0.9,
                do_sample=True
            )
            output_text = self.tokenizer.decode(
                output_tokens[0][chunk_ids.shape[-1]:], skip_special_tokens=True
            )
            preds.append(output_text.strip())
        if len(preds) > 1:
            combined_preds_str = "\n".join(preds)
            
            if self.tokenizer.encode(combined_preds_str, return_tensors="pt").size()[1] <= 450:
                content_for_final_summary = combined_preds_str
            else:
                placeholder = " [...truncated...] "
                max_char_len_for_combined = 1500
                if len(combined_preds_str) > max_char_len_for_combined:
                    chars_each_side = (max_char_len_for_combined - len(placeholder)) // 2
                    content_for_final_summary = combined_preds_str[:chars_each_side] + placeholder + combined_preds_str[-chars_each_side:]
                else:
                    content_for_final_summary = combined_preds_str

            messages = [{"role": "user", "content": f"Summarize the following text:\\n{content_for_final_summary}"}]
            input_for_final_summary = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            chunk_ids = self.tokenizer.encode(
                input_for_final_summary,
                return_tensors="pt",
                truncation=True,
                max_length=2048,
            ).to(self.device)

            output_tokens = self.model.generate(
                chunk_ids,
                max_new_tokens=256,
                temperature=0.2,
                top_p=0.9,
                do_sample=True
            )
            output_text = self.tokenizer.decode(
                output_tokens[0][chunk_ids.shape[-1]:], skip_special_tokens=True
            )
            return output_text.strip()
        elif preds:
            return preds[0]
        else:
            return ""


def main(path: Path):
    s = summarizer()
    return s.summarize(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a ipynb ")
    parser.add_argument("path", type=Path, help="Path to the file to be summarized")
    args = parser.parse_args()
    print(main(args.path))
