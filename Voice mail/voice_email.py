import smtplib
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

def get_audio(prompt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=10)
            text = r.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not understand. Please try again.")
            return get_audio(prompt)
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return ""
        except sr.WaitTimeoutError:
            speak("No response detected. Try again.")
            return get_audio(prompt)

def send_email(to_email, subject, message):
    from_email = "yourname@gmail.com"
    password = "12345"  # From Gmail App Passwords

    email_body = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, email_body)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        print("Error:", e)
        speak("Failed to send email.")

def clean_email(raw_email):
    cleaned = raw_email.lower().replace(" ", "").replace("at", "@").replace("dot", ".")
    return cleaned

def main():
    speak("Welcome to the voice-based email system.")

    raw_email = get_audio("Please say the recipient's email address.")
    receiver = clean_email(raw_email)

    subject = get_audio("Please say the subject.")
    message = get_audio("Please speak your message.")

    send_email(receiver, subject, message)

if __name__ == "__main__":
    main()
