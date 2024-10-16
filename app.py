import pygame
import speech_recognition as sr

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up font and colors
font = pygame.font.Font(None, 74)
white = (255, 255, 255)
green = (0, 255, 0)

def display_text(text):
    screen.fill(green)  # Fill background with green
    text_surface = font.render(text, True, white)  # Render the text in white
    screen.blit(text_surface, (50, 300))  # Display text in the center of the screen
    pygame.display.flip()  # Update the screen

def recognize_and_display():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        text = r.recognize_google(audio)
        display_text(text)
    except sr.UnknownValueError:
        display_text("Sorry, I could not understand the audio.")
    except sr.RequestError:
        display_text("Sorry, there was a request error.")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    recognize_and_display()  # Run the voice recognition and display
    pygame.time.wait(5000)  # Wait 5 seconds before listening again

pygame.quit()
