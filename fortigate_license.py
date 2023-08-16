"""
FortiGate license generator
Copyright (C) 2023  CataLpa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import struct
import base64
from Crypto.Cipher import AES

lic_key_array = {
    "SERIALNO":       (0x73, 0x0),
    "CERT":           (0x73, 0x8),
    "KEY":            (0X73, 0x10),
    "CERT2":          (0X73, 0x18),
    "KEY2":           (0X73, 0x20),
    "CREATEDATE":     (0x73, 0x28),
    "UUID":           (0x73, 0x30),
    "CONTRACT":       (0x73, 0x38),
    "USGFACTORY":     (0x6e, 0x40),
    "LENCFACTORY":    (0x6e, 0x44),
    "CARRIERFACTORY": (0x6e, 0x48),
    "EXPIRY":         (0x6e, 0x4c)
}

class License:
    aes_key_iv_length = 32            # 4 bytes
    aes_key = b"\x61" * 32            # 32 bytes, contains iv(16 bytes) and key(16 bytes)
    enc_data_length = None            # 4 bytes
    enc_data = None                   # length = enc_data_length
    license_data = None

    def __init__(self, licensedata):
        self.license_data = licensedata
    
    def encrypt_data(self):
        tmp_buf = b"\x00" * 4 + struct.pack("<I", 0x13A38693) + b"\x00" * 4 + self.license_data   # append magic number
        def encrypt(data, password, iv):
            bs = 16
            pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode()
            cipher = AES.new(password, AES.MODE_CBC, iv)
            data = cipher.encrypt(pad(data))
            return data
        
        self.enc_data = encrypt(tmp_buf, self.aes_key[16:], self.aes_key[:16])
        self.enc_data_length = len(self.enc_data)
    
    def obj_to_license(self):
        buf = b""
        buf += struct.pack("<I", self.aes_key_iv_length)
        buf += self.aes_key
        buf += struct.pack("<I", self.enc_data_length)
        buf += self.enc_data
        return base64.b64encode(buf)

class LicenseDataBlock:
    key_name_length = None    # 1 byte
    key_name = None
    key_flag = None           # 1 byte, 's' for str or 'n' for num
    key_value_length = None   # 2 bytes
    key_value = None

    def __init__(self, keyname, keyvalue):
        self.key_name_length = len(keyname)
        self.key_name = keyname
        self.key_value_length = len(keyvalue)
        self.key_value = keyvalue
        self.key_flag = lic_key_array.get(keyname)[0]
    
    def obj_to_bin(self):
        buf = b""
        buf += struct.pack("<B", self.key_name_length)
        buf += self.key_name.encode()
        buf += struct.pack("<B", self.key_flag)
        if self.key_flag == 0x73:
            buf += struct.pack("<H", self.key_value_length)
            buf += self.key_value.encode()
        elif self.key_flag == 0x6e:
            buf += struct.pack("<H", 4)
            buf += struct.pack("<I", int(self.key_value))
        return buf

if __name__ == "__main__":
    license_data_list = [
        LicenseDataBlock("SERIALNO", "FGVMPGLICENSEDTOGREETLIST"),
        LicenseDataBlock("CREATEDATE", "1692165607"),
        LicenseDataBlock("USGFACTORY", "0"),
        LicenseDataBlock("LENCFACTORY", "0"),
        LicenseDataBlock("CARRIERFACTORY", "0"),
        LicenseDataBlock("EXPIRY", "4294967295"),
    ]
    license_data = b""
    for obj in license_data_list:
        license_data += obj.obj_to_bin()

    license = License(license_data)
    license.encrypt_data()
    raw_license = license.obj_to_license().decode()
    n = 0
    lic = ""
    while True:
        if n >= len(raw_license):
            break
        lic += raw_license[n:n + 64]
        lic += "\r\n"
        n += 64
    f = open("./lic.txt", "w")
    f.write("-----BEGIN FGT VM LICENSE-----\r\n")
    f.write(lic)
    f.write("-----END FGT VM LICENSE-----\r\n")
    f.close()
    print("Saved to ./lic.txt")
