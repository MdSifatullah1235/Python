from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')


def get_response(prompt,max_length=50):
    inputs = tokenizer(prompt, return_tensors='pt')
    output = model.generate(**inputs, max_length=max_length,num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

question_prompt = input("Enter a question: ")
print(f"Question Prompt: {get_response(question_prompt)}")

command_prompt = input("Enter a command: ")

print(f"Command Prompt: {get_response(command_prompt)}")