from django.shortcuts import render,get_object_or_404, redirect
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
from .models import ChatMessage

# Create your views here.

def chatBot(request):
    return render(request, 'chatBot/chatBot.html')


# Path to the fine-tuned model
save_directory = r"C:\Users\HP\Desktop\PregnancyModelChatBot\fine_tuned_T5PregnancyChatbot"

# ChatBot class for handling user input and generating responses
class ChatBot:
    def __init__(self):
        try:
            print("Loading model...")
            self.model = TFT5ForConditionalGeneration.from_pretrained(save_directory)
            print("Model loaded successfully.")
            print("Loading tokenizer...")
            self.tokenizer = T5Tokenizer.from_pretrained(save_directory)
            print("Tokenizer loaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Error loading model or tokenizer: {e}")

    def get_response(self, input_text):
        if not input_text.strip():
            return "Please enter a valid message."
        try:
            input_text = f"question: {input_text} </s>"
            input_ids = self.tokenizer(input_text, return_tensors="tf").input_ids
            outputs = self.model.generate(
                input_ids,
                max_length=150,
                min_length=50,
                num_beams=5,
                do_sample=True,
                temperature=0.5,
                top_p=0.9,
            )
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer
        except Exception as e:
            return f"An error occurred while generating a response: {e}"

# Instantiate the chatbot
chatbot = ChatBot()

# View to handle chat page requests
def chatPage(request):
    if not request.user.is_authenticated:
        return redirect("connexion")

    if request.method == "POST":
        # Retrieve the user's input
        user_message = request.POST.get("message", "").strip()

        if user_message:
            # Get the bot's response
            bot_response = chatbot.get_response(user_message)

            # Save the chat message to the database
            ChatMessage.objects.create(
                user=request.user, message=user_message, response=bot_response
            )

    # Fetch chat history for the user
    chat_history = ChatMessage.objects.filter(user=request.user).order_by("timestamp")

    context = {
        "chat_history": chat_history,  # Pass chat history to the template
    }

    return render(request, "chatBot/chatBot.html", context)


def delete_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect("connexion")

    # Get the message or return 404 if not found
    chat_message = get_object_or_404(ChatMessage, id=message_id, user=request.user)

    # Delete the message
    chat_message.delete()

    # Redirect back to the chat page after deleting
    return redirect('chatBot')
