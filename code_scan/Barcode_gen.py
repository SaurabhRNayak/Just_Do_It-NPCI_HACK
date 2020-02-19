import hashlib
import barcode
from barcode.writer import ImageWriter
import cv2
from pyzbar import pyzbar
import time

file=r"E:\Hackerearth\NPCI\code_scan\static\abc"
scanned_file=r"E:\Hackerearth\NPCI\code_scan\scanned.jpg"
read_hash=r"E:\Hackerearth\NPCI\code_scan\hash.txt"
def encrypt(ar):
    str=''.join(i for i in ar)
    # print(hashlib.sha3_256(str.encode('utf-8')).hexdigest())
    # print(hashlib.sha1(str.encode('utf-8')).hexdigest())
    # print(hashlib.sha224(str.encode('utf-8')).hexdigest())
    # print(hashlib.shake_128(str.encode('utf-8')).hexdigest())
    # print(hashlib.blake2b(str.encode('utf-8')).hexdigest())
    encoded=(hashlib.md5(str.encode('utf-8')).hexdigest())[0:14]
    return encoded

def generate_barcode(data):
    c = barcode.get_barcode_class('code128')
    bc=c(data, writer=ImageWriter())
    bc.save(file)
    time.sleep(1)

def decrypt(image):
    # image = cv2.imread(f)
    barcodes = pyzbar.decode(image)
    if len(barcodes)>0:
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x - 10, y - 5), (x + w + 10, y + h + 5), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        cv2.imshow("Image", image)
        cv2.waitKey(0)

def read_feed(flg):
    """Video streaming generator function."""
    if flg == False:
        img = cv2.imread(scanned_file)
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    else:
        cap = cv2.VideoCapture(0)
        # Read until video is completed
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, img = cap.read()
            # print(type(img))
            if ret == True:
                global barcodeData
                # print("flg_bc",flg)
                img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
                barcodes = pyzbar.decode(img)
                if (len(barcodes) > 0):
                    print(barcodes)
                    for barcode in barcodes:
                        (x, y, w, h) = barcode.rect
                        cv2.rectangle(img, (x - 10, y - 5), (x + w + 10, y + h + 5), (0, 0, 255), 2)
                        barcodeData = barcode.data.decode("utf-8")
                        barcodeType = barcode.type
                        with open(read_hash, 'w') as f:
                            f.write(str(barcodeData))
                            print('read', barcodeData)
                        text = "{} ({})".format(barcodeData, barcodeType)
                        cv2.putText(img, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 0, 255), 2)
                        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
                        cv2.imwrite(scanned_file, img)
                    frame = cv2.imencode('.jpg', img)[1].tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    cv2.destroyAllWindows()
                    break

                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.1)

            else:
                break

if __name__=='__main__':
    en=encrypt(['a','asdadsdddddddd','122'])
    generate_barcode(en)
    feed=cv2.VideoCapture(0)
    while (True):
        _, image = feed.read()
        print(type(image))
        barcodes = pyzbar.decode(image)
        print(barcodes)
        if(len(barcodes)>0):
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x - 10, y - 5), (x + w + 10, y + h + 5), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(image, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)
                print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        cv2.imshow("Image", image)
        cv2.waitKey(1)

    # decrypt(cv2.imread(r"E:\Hackerearth\NPCI\code_scan\abc.png"))


