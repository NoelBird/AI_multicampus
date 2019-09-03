import struct
def to_csv(name, maxdata):
    lbl_f = open("mnist/" + name + "-labels-idx1-ubyte", "rb")
    img_f = open("mnist/" + name + "-images-idx3-ubyte", "rb")
    csv_f = open("mnist/" + name + ".csv", "w", encoding="utf-8")

    mag, lbl_count = struct.unpack(">II", lbl_f.read(8))
    mag, img_count = struct.unpack(">II", img_f.read(8))
    rows, cols = struct.unpack(">II", img_f.read(8))
    pixels = rows * cols

    res = []
    for idx in range(lbl_count):
        if idx > maxdata:
            break
        label = struct.unpack("B", lbl_f.read(1))[0]
        bdata = img_f.read(pixels)
        sdata = list(map(lambda n: str(n), bdata))
        csv_f.write(str(label)+",")
        csv_f.write(",".join(sdata)+"\r\n")

    csv_f.close()
    lbl_f.close()
    img_f.close()

# 시간 체크
import time
start = time.time()
to_csv("train", 5000) # 원하는 개수를 적는다. 최대 6만 이므로 6만보다 크면 모두 처리됨.
to_csv("t10k", 500)

end = (time.time()-start)
print( "{0:.2f}".format(end ), ' 초 소요됨.')