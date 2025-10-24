import minimalmodbus
import serial

class Sensor:
    def __init__(self, port: str, address: int) -> None:
        self.sensor = minimalmodbus.Instrument(port, address)
        self.sensor.serial.baudrate = 9600 #type:ignore
        self.sensor.serial.bytesize = 8 #type:ignore
        self.sensor.serial.parity   = serial.PARITY_NONE #type:ignore
        self.sensor.serial.stopbits = 1 #type:ignore
        self.sensor.serial.timeout  = 1 #type:ignore
        self.sensor.mode = minimalmodbus.MODE_RTU

    def __read_register_value(self, register_value: int) -> int | float:
        raw_value = self.sensor.read_register(register_value, 2, functioncode=3, signed=False)
        return raw_value
    
    def get_intent_flow_rate(self) -> int | float:
        raw_value_a = self.__read_register_value(0x003A)
        raw_value_b = self.__read_register_value(0x003B)
        air_flow = (raw_value_a * 65536 + raw_value_b)/10
        air_flow_m3 = air_flow * 0.06
        
        return air_flow_m3

    def get_accumulated_flow(self) -> int | float:
        raw_value_c = self.__read_register_value(0x003C)
        raw_value_d = self.__read_register_value(0x003D)
        raw_value_e = self.__read_register_value(0x003E)
        accumulated_flow = (raw_value_c * 65536) + (raw_value_d * 100) + (raw_value_e/10)

        return accumulated_flow
    
    def __disable_write_protection(self) -> bool:
        try:
            self.sensor.write_register(registeraddress=0x00FF, value=0xAA55, functioncode=6)
            return True
        except:
            return False
        
    def reset_accumulated_flow_rate(self) -> bool:
        try:
            self.__disable_write_protection()
            self.sensor.write_register(registeraddress=0x00F2, value=0x0001, functioncode= 6)
            return True
        except:
            return False
        
