import cv2
from pyzbar.pyzbar import decode


class QR:
    def __init__(self):
        self.qr_str = ''
        self.qr_frame = None
        self.captured = False

    def qr_scanner(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            for d in decode(frame):
                self.qr_str = d.data.decode()

                cv2.rectangle(frame, (d.rect.left, d.rect.top),
                              (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (255, 0, 0), 2)

                self.qr_frame = frame[d.rect.top: d.rect.top + d.rect.height, d.rect.left: d.rect.left + d.rect.width]

                self.captured = True
                break

            # Streaming normal frames until it captures a QR
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if self.captured:
                break

        cap.release()

        _, buffer = cv2.imencode('.jpg', self.qr_frame)
        self.qr_frame = buffer.tobytes()
        if self.qr_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
