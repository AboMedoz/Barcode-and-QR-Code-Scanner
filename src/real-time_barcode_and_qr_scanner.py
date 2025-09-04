import cv2
import numpy as np
from pyzbar.pyzbar import decode

qr_str = ''
img = None
captured = False

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)

    for d in decode(frame):
        qr_str = d.data.decode()

        cv2.rectangle(frame, (d.rect.left, d.rect.top), (d.rect.left + d.rect.width, d.rect.top + d.rect.height),
                      (0, 255, 0), 2)
        cv2.polylines(frame, [np.array(d.polygon)], True, (0, 255, 0), 2)
        cv2.putText(frame, qr_str, (d.rect.left, d.rect.top + d.rect.height), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 1)

        img = frame[d.rect.top:d.rect.top + d.rect.height, d.rect.left:d.rect.left + d.rect.width]
        captured = True
        break
    if captured:
        break

    cv2.imshow('Barcode and QR Reader', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

cv2.imshow('Output', img)
print(qr_str)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


