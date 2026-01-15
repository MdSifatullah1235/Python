from transformers import GPT2LMHeadModel, GPT2Tokenizer
import config

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model=GPT2LMHeadModel.from_pretrained('gpt2')

def get_response(prompt,max_length=50):
    inputs=tokenizer.encode(prompt,return_tensors='pt')
    outputs=model.generate(inputs,max_length=max_length,num_return_sequences=1)
    response=tokenizer.decode(outputs[0],skip_special_tokens=True)
    return response

question_prompt=input("Ask me a question: ")
print(f"Question prompt response:{get_response(question_prompt)}")
command_prompt=input("Tell me something to do: ")
print(f"Command prompt response:{get_response(command_prompt)}")