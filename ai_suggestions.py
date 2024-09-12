"""
Importing necessary libraries
"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the model and tokenizer
MODEL_NAME = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)


def generate_rap_lyrics(prompt, current_lyrics=None, max_lines=10):
    """
    Generates rap lyrics using the GPT-2 model.
    """
    try:
        print(f"Generating rap lyrics with prompt: {prompt}")
        print(f"Current lyrics: {current_lyrics}")
        print(f"Max lines: {max_lines}")

        # Combine the current lyrics and the new prompt for context if provided
        combined_input = f"{current_lyrics}\n{prompt}" if current_lyrics else prompt

        # Tokenize the input text
        input_ids = tokenizer.encode(combined_input, return_tensors="pt", truncation=True, max_length=512)

        # Generate new tokens
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=input_ids.shape[1] + 100,  # Generate up to 100 new tokens
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id,
                attention_mask=input_ids.new_ones(input_ids.shape)
            )

        # Decode the generated tokens to text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        print(f"Raw generated text: {generated_text}")

        # Extract only the newly generated part
        new_text = generated_text[len(combined_input):].strip()

        if not new_text:
            return "No new lyrics generated. Please try again."

        # Format the generated text into rap lyrics
        formatted_lyrics = format_rap_lyrics(new_text, max_lines)
        print(f"Formatted lyrics: {formatted_lyrics}")
        return formatted_lyrics
    except Exception as e:
        print(f"Error in generate_rap_lyrics: {e}")
        import traceback
        traceback.print_exc()
        return f"Error generating lyrics: {str(e)}"


def format_rap_lyrics(generated_text, max_lines):
    """
    Formats the generated text into rap lyrics.
    """
    try:
        lines = generated_text.split('\n')
        formatted_lines = [line.strip() for line in lines if line.strip()][:max_lines]
        return '\n'.join(formatted_lines)
    except Exception as e:
        print(f"Error in format_rap_lyrics: {e}")
        import traceback
        traceback.print_exc()
        return f"Error formatting lyrics: {str(e)}"
