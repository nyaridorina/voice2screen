import pygame
import speech_recognition as sr

# Initialize pygame
pygame.init()

# Set up the display dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up font and colors
font = pygame.font.Font(None, 74)  # You can change the font size or use a custom font file
white = (255, 255, 255)
green = (0, 255, 0)

# Function to display text on the screen
def display_text(text):
    screen.fill(green)  # Fill the background with green
    text_surface = font.render(text, True, white)  # Render the text in white
    text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2))  # Center the text
    screen.blit(text_surface, text_rect)  # Display the text
    pygame.display.flip()  # Update the display

# Function to handle speech recognition and display
def recognize_and_display():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Reduce the noise interference

        print("Listening for voice input...")
        audio = recognizer.listen(source)  # Listen to the microphone input

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)  # Using Google's API for recognition
        print(f"Recognized Text: {text}")
        display_text(text)  # Display the recognized text
    except sr.UnknownValueError:
        print("Could not understand the audio")
        display_text("Sorry, I could not understand.")
    except sr.RequestError:
        print("API request failed")
        display_text("Sorry, there was a request error.")

# Main loop for the pygame application
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Allow the user to close the window
                running = False

        recognize_and_display()  # Recognize and display text continuously
        pygame.time.wait(5000)  # Wait for 5 seconds before listening again

    pygame.quit()

# Entry point of the script
if __name__ == "__main__":
    main()
