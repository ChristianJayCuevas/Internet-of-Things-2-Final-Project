import requests
import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils

finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4, 3)
index_Coord = (8, 6)
middle_Coord = (12, 10)
ring_Coord = (16, 14)
pinky_Coord = (20, 18)

# Set the IP address of your ESP8266
esp8266_ip = "192.168.4.1"  # Replace with the actual IP address

# Function to send a command to the robot
def send_command(command):
    url = f"http://{esp8266_ip}/?State={command}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Command '{command}' sent successfully.")
    else:
        print(f"Failed to send command '{command}'. Status code: {response.status_code}")

while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    binary_number = ""  # Reset binary_number for each frame

    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:  # Corrected variable name
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))

        upCount = 0
        if 0 <= thumb_Coord[0] < len(handList) and 0 <= thumb_Coord[1] < len(handList):
            if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                cv2.putText(image, "Thumb", (150, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 7)
                binary_number += "1"
            else:
                binary_number += "0"

        if 0 <= index_Coord[0] < len(handList) and 0 <= index_Coord[1] < len(handList):
            if handList[index_Coord[0]][1] < handList[index_Coord[1]][1]:
                cv2.putText(image, "Index", (150, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 7)
                binary_number += "1"
            else:
                binary_number += "0"

        if 0 <= middle_Coord[0] < len(handList) and 0 <= middle_Coord[1] < len(handList):
            if handList[middle_Coord[0]][1] < handList[middle_Coord[1]][1]:
                cv2.putText(image, "Middle", (150, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 7)
                binary_number += "1"
            else:
                binary_number += "0"

        if 0 <= ring_Coord[0] < len(handList) and 0 <= ring_Coord[1] < len(handList):
            if handList[ring_Coord[0]][1] < handList[ring_Coord[1]][1]:
                cv2.putText(image, "Ring", (150, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 7)
                binary_number += "1"
            else:
                binary_number += "0"

        if 0 <= pinky_Coord[0] < len(handList) and 0 <= pinky_Coord[1] < len(handList):
            if handList[pinky_Coord[0]][1] < handList[pinky_Coord[1]][1]:
                cv2.putText(image, "Pinky", (150, 350), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 7)
                binary_number += "1"
            else:
                binary_number += "0"

    if(binary_number=="00000"):
        send_command("S")
    elif(binary_number=="01000"):
        send_command("F")
    elif(binary_number=="01100"):
        send_command("B")
    elif(binary_number=="00001"):
        send_command("R")
    elif(binary_number=="10000"):
        send_command("L")
    elif(binary_number=="01111"):
        send_command("AD")
    elif(binary_number=="01001"):
        send_command("BU")

    # match binary_number:
    #     case "00000":
    #         send_command("S")
    #         #The bot will not move
    #     case "01000":
    #         send_command("F")
    #         #The bot will move but moderate speed
    #     case "01100":
    #         send_command("B")
    #         #The bot will move backward in moderate speed
    #     case "00100":
    #         send_command("FORWARD")
    #         #The bot will move forward in maximum speed
    #     case "00010":
    #         send_command("RETREAT")
    #         #The bot will move backward in maximum speed
    #     case "00001":
    #         send_command("ROTATE")
    #         #The bot will rotate
    #     case "11000":
    #         send_command("RIGHT")
    #         #The bot will move forward with a little bit of tilt to right
    #     case "10100":
    #         send_command("LEFT")
    #         #The bot will move forward with a little bit of tilt to left



    cv2.imshow("Live Feed", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Note: Adjust esp8266_ip to match the actual IP address of your ESP8266
