import os

import segno
from aiogram.types import InputFile


# qrcode = segno.make_qr("Hello METANIT.COM")
# qrcode2 = segno.make("Hello METANIT.COM", micro=False)
#
# qrcode.save("metanit_qr.png")
# qrcode2.save("metanit_qr2.png")
# qrcode.show()
# qrcode2.show()
if not os.path.exists('qrs'):
    os.mkdir('qrs')

def get_qr_code(text: str):
    qr = segno.make(text, micro=False)
    qr.save(f'qrs/{text}.png', scale=10)
    return InputFile(f'qrs/{text}.png')
