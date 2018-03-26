import smbus
import time
import struct

def u2s(n):
	'''
		Converte numero sem sinal para numero com sinal
	'''
	return struct.unpack("<h", struct.pack("<H", n))[0]

endereco_barometro = 0x77

bus = smbus.SMBus(1)
x = bus.read_byte_data(endereco_barometro,0xD0)

if x == 0x55:
	print("Barometro esta online.")

else:
	print("Barometro nao encontrado.")
	exit(1)

AC6_MSB = bus.read_byte_data(0x77,0xB4)
AC6_LSB = bus.read_byte_data(0x77,0xB5)
AC6 = float((AC6_MSB << 8) + AC6_LSB)

AC5_MSB = bus.read_byte_data(0x77,0xB2)
AC5_LSB = bus.read_byte_data(0x77,0xB3)
AC5 = float((AC5_MSB << 8) + AC5_LSB)

MC_MSB = bus.read_byte_data(0x77,0xBC)
MC_LSB = bus.read_byte_data(0x77,0xBD)
MC = float(u2s((MC_MSB << 8) + MC_LSB))

MD_MSB = bus.read_byte_data(0x77,0xBE)
MD_LSB = bus.read_byte_data(0x77,0xBF)
MD = float(u2s((MD_MSB << 8) + MD_LSB))

#Acionando a leitura da temperatura
bus.write_byte_data(0x77,0xF4,0x2E)

time.sleep(0.005)

MSB = bus.read_byte_data(0x77,0xF6)
LSB = bus.read_byte_data(0x77,0xF7)

UT = float((MSB<<8) + LSB)

#Calculo da temperatura
X1 = (UT - AC6) * (AC5 / (2**15))
X2 = (MC * (2**11)) / (X1+MD)
B5 = X1 + X2
T = ((B5+8)/(2**4))/10

print("A temperatura eh %s (UT = %s)" %(T, UT))
