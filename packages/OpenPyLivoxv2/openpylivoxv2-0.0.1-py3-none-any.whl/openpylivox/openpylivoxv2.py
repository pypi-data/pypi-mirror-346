import binascii
import select
import socket
import struct
import threading
import time
import sys
import os
from pathlib import Path

# additional modules
import crcmod
import numpy as np
from tqdm import tqdm
import laspy
from deprecated import deprecated

class _heartbeatThread(object):
    
    def __init__(self, interval, transmit_socket, send_to_IP, send_to_port, send_command, showMessages, format_spaces):
        self.interval = interval
        self.IP = send_to_IP
        self.port = send_to_port  # [HAP] For Mid-360, this should be 56100 (control command port)
        self.t_socket = transmit_socket
        self.t_command = send_command
        self.started = True
        self.work_state = -1
        self.idle_state = 0
        self._showMessages = showMessages
        self._format_spaces = format_spaces

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            if self.started:
                self.t_socket.sendto(self.t_command, (self.IP, self.port))

                # check for proper response from heartbeat request
                if select.select([self.t_socket], [], [], 0.1)[0]:
                    binData, addr = self.t_socket.recvfrom(50)  # [HAP] Increased buffer size to accommodate Mid-360 protocol
                    tempObj = openpylivox()
                    _, ack, cmd_set, cmd_id, ret_code_bin = tempObj._parseResp(binData)

                    # [HAP] Updated command ID check for Mid-360 protocol 
                    # Mid-360 uses cmd_id 0x0101 for parameter information inquire
                    if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "257":  # 0x0101
                        ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                        if ret_code != 0:
                            if self._showMessages: print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     incorrect heartbeat response")
                        else:
                            # [HAP] Updated to handle Mid-360's different working status values
                            # Searching for work state information in the response (key 0x8006)
                            # Format: key(2) + length(2) + value(1)
                            key_found = False
                            for i in range(len(ret_code_bin) - 5):
                                if int.from_bytes(ret_code_bin[i:i+2], byteorder='little') == 0x8006:
                                    self.work_state = int.from_bytes(ret_code_bin[i+4:i+5], byteorder='little')
                                    key_found = True
                                    break
                            
                            if not key_found and self._showMessages:
                                print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     work state not found in response")

                            # [HAP] Updated state error checking for Mid-360
                            # ERROR state in Mid-360 is 0x04
                            if self.work_state == 0x04:
                                print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     *** ERROR: LIDAR IN ERROR STATE ***")
                                sys.exit(0)
                    
                    # [HAP] Updated to check for abnormal status message
                    # Mid-360 uses cmd_id 0x0102 for push messages
                    elif ack == "MSG (message)" and cmd_set == "General" and cmd_id == "258":  # 0x0102
                        # not given an option to hide this message!!
                        print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     *** ERROR: ABNORMAL STATUS MESSAGE RECEIVED ***")
                        sys.exit(1)
                    else:
                        if self._showMessages: print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     incorrect heartbeat response")

                for i in range(9, -1, -1):
                    self.idle_state = i
                    time.sleep(self.interval / 10.0)
            else:
                break

    def stop(self):
        self.started = False
        self.thread.join()
        self.idle_state = 9


class openpylivox(object):

    # Mid-360 Command Constants
    # Format: sof(1) + version(1) + length(2) + seq_num(4) + cmd_id(2) + cmd_type(1) + sender_type(1) + resv(6) + crc16(2) + crc32(4) + data

    # Device Discovery (0x0000)
    _CMD_QUERY =                  b'\xAA\x01\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4D\x3C\x00\x00\x00\x00'

    # Parameter Inquire (0x0101) - Used for heartbeat
    _CMD_HEARTBEAT =              b'\xAA\x01\x18\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF4\xA7\x00\x00\x00\x00'

    # Parameter Configuration (0x0100) - For disconnect
    _CMD_DISCONNECT =             b'\xAA\x01\x1C\x00\x02\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x65\x78\x00\x00\x00\x00\x01\x00\x1A\x00\x02'

    # Parameter Inquire (0x0101) - For reading extrinsic parameters
    _CMD_READ_EXTRINSIC =         b'\xAA\x01\x1C\x00\x03\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3B\xB0\x00\x00\x00\x00\x01\x00\x12\x00'

    # Parameter Inquire (0x0101) - For fan status
    _CMD_GET_FAN =                b'\xAA\x01\x1C\x00\x04\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8C\xC3\x00\x00\x00\x00\x01\x00\x19\x00'

    # Parameter Inquire (0x0101) - For IMU configuration
    _CMD_GET_IMU =                b'\xAA\x01\x1C\x00\x05\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFD\x0E\x00\x00\x00\x00\x01\x00\x1C\x00'

    # Parameter Configuration (0x0100) - Rain/Fog Mode On
    _CMD_RAIN_FOG_ON =            b'\xAA\x01\x1C\x00\x06\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8A\x37\x00\x00\x00\x00\x01\x00\x18\x00\x01'

    # Parameter Configuration (0x0100) - Rain/Fog Mode Off
    _CMD_RAIN_FOG_OFF =           b'\xAA\x01\x1C\x00\x07\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEB\xFA\x00\x00\x00\x00\x01\x00\x18\x00\x00'

    # Parameter Configuration (0x0100) - Start Lidar (Work Mode: Sampling)
    _CMD_LIDAR_START =            b'\xAA\x01\x1C\x00\x08\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1C\x41\x00\x00\x00\x00\x01\x00\x1A\x00\x01'

    # Parameter Configuration (0x0100) - Lidar Power Save Mode
    _CMD_LIDAR_POWERSAVE =        b'\xAA\x01\x1C\x00\x09\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7D\x8C\x00\x00\x00\x00\x01\x00\x1A\x00\x02'

    # Parameter Configuration (0x0100) - Lidar Standby Mode
    _CMD_LIDAR_STANDBY =          b'\xAA\x01\x1C\x00\x0A\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAA\xA7\x00\x00\x00\x00\x01\x00\x1A\x00\x09'

    # Parameter Configuration (0x0100) - Stop Point Cloud Data
    _CMD_DATA_STOP =              b'\xAA\x01\x1C\x00\x0B\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xCB\x6A\x00\x00\x00\x00\x01\x00\x00\x00\x00'

    # Parameter Configuration (0x0100) - Start Point Cloud Data
    _CMD_DATA_START =             b'\xAA\x01\x1C\x00\x0C\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3C\xD1\x00\x00\x00\x00\x01\x00\x00\x00\x01'

    # Parameter Configuration (0x0100) - Cartesian Coordinate System
    _CMD_CARTESIAN_CS =           b'\xAA\x01\x1C\x00\x0D\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x5D\x1C\x00\x00\x00\x00\x01\x00\x00\x00\x01'

    # Parameter Configuration (0x0100) - Spherical Coordinate System
    _CMD_SPHERICAL_CS =           b'\xAA\x01\x1C\x00\x0E\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8A\x37\x00\x00\x00\x00\x01\x00\x00\x00\x03'

    # Parameter Configuration (0x0100) - Fan On
    _CMD_FAN_ON =                 b'\xAA\x01\x1C\x00\x0F\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEB\xFA\x00\x00\x00\x00\x01\x00\x19\x00\x01'

    # Parameter Configuration (0x0100) - Fan Off
    _CMD_FAN_OFF =                b'\xAA\x01\x1C\x00\x10\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xBD\x83\x00\x00\x00\x00\x01\x00\x19\x00\x00'

    # Parameter Configuration (0x0100) - Single First Echo Mode
    _CMD_LIDAR_SINGLE_1ST =       b'\xAA\x01\x1C\x00\x11\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xDC\x4E\x00\x00\x00\x00\x01\x00\x00\x00\x01'

    # Parameter Configuration (0x0100) - Single Strongest Echo Mode
    _CMD_LIDAR_SINGLE_STRONGEST = b'\xAA\x01\x1C\x00\x12\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0B\x65\x00\x00\x00\x00\x01\x00\x00\x00\x01'

    # Parameter Configuration (0x0100) - Dual Return Mode
    _CMD_LIDAR_DUAL =             b'\xAA\x01\x1C\x00\x13\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6A\xA8\x00\x00\x00\x00\x01\x00\x00\x00\x02'

    # Parameter Configuration (0x0100) - IMU Data On
    _CMD_IMU_DATA_ON =            b'\xAA\x01\x1C\x00\x14\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9D\x13\x00\x00\x00\x00\x01\x00\x1C\x00\x01'

    # Parameter Configuration (0x0100) - IMU Data Off
    _CMD_IMU_DATA_OFF =           b'\xAA\x01\x1C\x00\x15\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFC\xDE\x00\x00\x00\x00\x01\x00\x1C\x00\x00'

    # Reboot Device (0x0200)
    _CMD_REBOOT =                 b'\xAA\x01\x1A\x00\x16\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC2\xC9\x00\x00\x00\x00\x00\x00'

    # Parameter Configuration (0x0100) - Dynamic IP configuration
    _CMD_DYNAMIC_IP =             b'\xAA\x01\x24\x00\x17\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA3\x04\x00\x00\x00\x00\x01\x00\x04\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    # Parameter Configuration (0x0100) - Write Zero Extrinsic Parameters
    _CMD_WRITE_ZERO_EO =          b'\xAA\x01\x34\x00\x18\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x54\xBF\x00\x00\x00\x00\x01\x00\x12\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    # Note: These CRC values are placeholders and should be properly calculated

    _SPECIAL_FIRMWARE_TYPE_DICT = {"03.03.0001": 2,
                                "03.03.0002": 3,
                                "03.03.0006": 2,
                                "03.03.0007": 3}

    def __init__(self, showMessages=False):

        self._isConnected = False
        self._isData = False
        self._isWriting = False
        self._dataSocket = ""
        self._cmdSocket = ""
        self._imuSocket = ""
        self._heartbeat = None
        self._firmware = "UNKNOWN"
        self._coordSystem = -1
        self._x = None
        self._y = None
        self._z = None
        self._roll = None
        self._pitch = None
        self._yaw = None
        self._captureStream = None
        self._serial = "UNKNOWN"
        self._ipRangeCode = 0
        self._computerIP = ""
        self._sensorIP = ""
        self._dataPort = -1
        self._cmdPort = -1
        self._imuPort = -1
        self._init_showMessages = showMessages
        self._showMessages = showMessages
        self._deviceType = "UNKNOWN"
        self._mid100_sensors = []
        self._format_spaces = ""

    def _reinit(self):

        self._dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._imuSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._cmdSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._imuSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        lidarSensorIPs, serialNums, ipRangeCodes, sensorTypes = self._searchForSensors(False)

        unique_serialNums = []
        unique_sensors = []
        IP_groups = []
        ID_groups = []

        for i in range(len(lidarSensorIPs)):
            if i == 0:
                unique_serialNums.append(serialNums[i])
            else:
                matched = False
                for j in range(len(unique_serialNums)):
                    if serialNums[i] == unique_serialNums[j]:
                        matched = True
                        break
                if not matched:
                    unique_serialNums.append(serialNums[i])

        for i in range(len(unique_serialNums)):
            count = 0
            IPs = ""
            IDs = ""
            for j in range(len(serialNums)):
                if serialNums[j] == unique_serialNums[i]:
                    count += 1
                    IPs += lidarSensorIPs[j] + ","
                    IDs += str(ipRangeCodes[j]) + ","
            if count == 1:
                unique_sensors.append(sensorTypes[i])
            elif count == 2:
                unique_sensors.append("NA")
            elif count == 3:
                unique_sensors.append("Mid-100")

            IP_groups.append(IPs[:-1])
            ID_groups.append(IDs[:-1])

        sensor_IPs = []
        for i in range(len(IP_groups)):
            current_device = unique_sensors[i]
            ind_IPs = IP_groups[i].split(',')
            for j in range(len(ind_IPs)):
                ip_and_type = [ind_IPs[j],current_device]
                sensor_IPs.append(ip_and_type)

        foundMatchIP = False
        for i in range(0, len(lidarSensorIPs)):
            if lidarSensorIPs[i] == self._sensorIP:
                foundMatchIP = True
                self._serial = serialNums[i]
                self._ipRangeCode = ipRangeCodes[i]
                break

        if foundMatchIP == False:
            print("\n* ERROR: specified sensor IP:Command Port cannot connect to a Livox sensor *")
            print("* common causes are a wrong IP or the command port is being used already   *\n")
            time.sleep(0.1)
            sys.exit(2)

        return unique_serialNums, unique_sensors, sensor_IPs

    def _checkIP(self, inputIP):

        IPclean = ""
        if inputIP:
            IPparts = inputIP.split(".")
            if len(IPparts) == 4:
                i = 0
                for i in range(0, 4):
                    try:
                        IPint = int(IPparts[i])
                        if IPint >= 0 and IPint <= 254:
                            IPclean += str(IPint)
                            if i < 3:
                                IPclean += "."
                        else:
                            IPclean = ""
                            break
                    except:
                        IPclean = ""
                        break

        return IPclean

    def _checkPort(self, inputPort):

        try:
            portNum = int(inputPort)
            if portNum >= 0 and portNum <= 65535:
                pass
            else:
                portNum = -1
        except:
            portNum = -1

        return portNum

    def _searchForSensors(self, opt=False):

        serverSock_INIT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock_INIT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSock_INIT.bind(("0.0.0.0", 55000))

        foundDevice = select.select([serverSock_INIT], [], [], 1)[0]

        IPs = []
        Serials = []
        ipRangeCodes = []
        sensorTypes = []

        if foundDevice:

            readData = True
            while readData:

                binData, addr = serverSock_INIT.recvfrom(34)

                if len(addr) == 2:
                    if addr[1] == 65000:
                        if len(IPs) == 0:
                            goodData, cmdMessage, dataMessage, device_serial, typeMessage, ipRangeCode = self._info(binData)
                            sensorTypes.append(typeMessage)
                            IPs.append(self._checkIP(addr[0]))
                            Serials.append(device_serial)
                            ipRangeCodes.append(ipRangeCode)

                        else:
                            existsAlready = False
                            for i in range(0, len(IPs)):
                                if addr[0] == IPs[i]:
                                    existsAlready = True
                            if existsAlready:
                                readData = False
                                break
                            else:
                                goodData, cmdMessage, dataMessage, device_serial, typeMessage, ipRangeCode = self._info(binData)
                                sensorTypes.append(typeMessage)
                                IPs.append(self._checkIP(addr[0]))
                                Serials.append(device_serial)
                                ipRangeCodes.append(ipRangeCode)

                else:
                    readData = False

        serverSock_INIT.close()
        time.sleep(0.2)

        if self._showMessages and opt:
            for i in range(0, len(IPs)):
                print("   Found Livox Sensor w. serial #" + Serials[i] + " at IP: " + IPs[i])
            print()

        return IPs, Serials, ipRangeCodes, sensorTypes

    def _auto_computerIP(self):

        try:
            hostname = socket.gethostname()
            self._computerIP = socket.gethostbyname(hostname)

        except:
            self.computerIP = ""

    def _bindPorts(self):

        try:
            self._dataSocket.bind((self._computerIP, self._dataPort))
            self._cmdSocket.bind((self._computerIP, self._cmdPort))
            self._imuSocket.bind((self._computerIP, self._imuPort))
            assignedDataPort = self._dataSocket.getsockname()[1]
            assignedCmdPort = self._cmdSocket.getsockname()[1]
            assignedIMUPort = self._imuSocket.getsockname()[1]

            time.sleep(0.1)

            return assignedDataPort, assignedCmdPort, assignedIMUPort

        except socket.error as err:
            print(" *** ERROR: cannot bind to specified IP:Port(s), " + err)
            sys.exit(3)


    def _waitForIdle(self):

        while self._heartbeat.idle_state != 9:
            time.sleep(0.1)

    def _disconnectSensor(self):

        self._waitForIdle()
        self._cmdSocket.sendto(self._CMD_DISCONNECT, (self._sensorIP, 56401))

        # check for proper response from disconnect request
        if select.select([self._cmdSocket], [], [], 0.1)[0]:
            binData, addr = self._cmdSocket.recvfrom(16)
            _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

            if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "6":
                ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                if ret_code == 1:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to disconnect")
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect disconnect response")

    def _rebootSensor(self):

        self._waitForIdle()
        self._cmdSocket.sendto(self._CMD_REBOOT, (self._sensorIP, 65000))

        # check for proper response from reboot request
        if select.select([self._cmdSocket], [], [], 0.1)[0]:
            binData, addr = self._cmdSocket.recvfrom(16)
            _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

            if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "10":
                ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                if ret_code == 1:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to reboot")
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect reboot response")

    def _query(self):

        self._waitForIdle()
        self._cmdSocket.sendto(self._CMD_QUERY, (self._sensorIP, 65000))

        # check for proper response from query request
        if select.select([self._cmdSocket], [], [], 0.1)[0]:

            binData, addr = self._cmdSocket.recvfrom(20)
            _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

            if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "2":
                ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                if ret_code == 1:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to receive query results")
                elif ret_code == 0:
                    AA = str(int.from_bytes(ret_code_bin[1], byteorder='little')).zfill(2)
                    BB = str(int.from_bytes(ret_code_bin[2], byteorder='little')).zfill(2)
                    CC = str(int.from_bytes(ret_code_bin[3], byteorder='little')).zfill(2)
                    DD = str(int.from_bytes(ret_code_bin[4], byteorder='little')).zfill(2)
                    self._firmware = AA + "." + BB + "." + CC + DD
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect query response")

    def _info(self, binData):

        goodData, cmdMessage, dataMessage, dataID, dataBytes = self._parseResp(binData)

        device_serial, typeMessage = "", ""

        if goodData:
            # received broadcast message
            if cmdMessage == "MSG (message)" and dataMessage == "General" and dataID == "0":
                device_broadcast_code = ""
                for i in range(0, 16):
                    device_broadcast_code += dataBytes[i].decode('ascii')

                ipRangeCode = int(device_broadcast_code[14:15])  # used to define L,M,R sensors in the Mid-100
                device_serial = device_broadcast_code[:-2]
                device_type = int.from_bytes(dataBytes[i + 1], byteorder='little')

                typeMessage = ""
                if device_type == 0:
                    typeMessage = "Hub    "
                elif device_type == 1:
                    typeMessage = "Mid-40 "
                elif device_type == 2:
                    typeMessage = "Tele-15"
                elif device_type == 3:
                    typeMessage = "Horizon"
                else:
                    typeMessage = "UNKNOWN"

        return goodData, cmdMessage, dataMessage, device_serial, typeMessage, ipRangeCode

    def _parseResp(self, binData):

        dataBytes = []
        dataString = ""
        dataLength = len(binData)
        for i in range(0, dataLength):
            dataBytes.append(binData[i:i + 1])
            dataString += (binascii.hexlify(binData[i:i + 1])).decode("utf-8")

        crc16Data = b''
        for i in range(0, 7):
            crc16Data += binascii.hexlify(dataBytes[i])

        crc16DataA = bytes.fromhex((crc16Data).decode('ascii'))
        checkSum16I = self._crc16(crc16DataA)

        frame_header_checksum_crc16 = int.from_bytes((dataBytes[7] + dataBytes[8]), byteorder='little')

        cmdMessage, dataMessage, dataID, = "", "", ""
        data = []

        goodData = True

        if frame_header_checksum_crc16 == checkSum16I:

            crc32Data = b''
            for i in range(0, dataLength - 4):
                crc32Data += binascii.hexlify(dataBytes[i])

            crc32DataA = bytes.fromhex((crc32Data).decode('ascii'))
            checkSum32I = self._crc32(crc32DataA)

            frame_header_checksum_crc32 = int.from_bytes((dataBytes[dataLength - 4] + dataBytes[dataLength - 3] +
                                                          dataBytes[dataLength - 2] + dataBytes[dataLength - 1]),
                                                         byteorder='little')

            if frame_header_checksum_crc32 == checkSum32I:

                frame_sof = int.from_bytes(dataBytes[0], byteorder='little')  # should be 170 = '\xAA'
                frame_version = int.from_bytes(dataBytes[1], byteorder='little')  # should be 1
                frame_length = int.from_bytes((dataBytes[2] + dataBytes[3]), byteorder='little')  # max value = 1400

                if frame_sof == 170:
                    if frame_version == 1:
                        if frame_length <= 1400:
                            frame_cmd_type = int.from_bytes(dataBytes[4], byteorder='little')

                            cmdMessage = ""
                            if frame_cmd_type == 0:
                                cmdMessage = "CMD (request)"
                            elif frame_cmd_type == 1:
                                cmdMessage = "ACK (response)"
                            elif frame_cmd_type == 2:
                                cmdMessage = "MSG (message)"
                            else:
                                goodData = False

                            frame_data_cmd_set = int.from_bytes(dataBytes[9], byteorder='little')

                            dataMessage = ""
                            if frame_data_cmd_set == 0:
                                dataMessage = "General"
                            elif frame_data_cmd_set == 1:
                                dataMessage = "Lidar"
                            elif frame_data_cmd_set == 2:
                                dataMessage = "Hub"
                            else:
                                goodData = False

                            dataID = str(int.from_bytes(dataBytes[10], byteorder='little'))
                            data = dataBytes[11:]

                        else:
                            goodData = False
                    else:
                        goodData = False
                else:
                    goodData = False
            else:
                goodData = False
                if self._showMessages: print("CRC32 Checksum Error")
        else:
            goodData = False
            if self._showMessages: print("CRC16 Checksum Error")

        return goodData, cmdMessage, dataMessage, dataID, data

    def _crc16(self, data):

        crc16 = crcmod.mkCrcFun(0x11021, rev=True, initCrc=0x4C49)
        checkSum = crc16(data)
        return checkSum

    def _crc16fromStr(self, binString):

        crcDataA = bytes.fromhex((binString).decode('ascii'))
        checkSum = self._crc16(crcDataA)
        strHexCheckSum = str(hex(checkSum))[2:]

        strLen = len(strHexCheckSum)
        for i in range(strLen, 4):
            strHexCheckSum = "0" + strHexCheckSum

        byte1 = strHexCheckSum[2:4]
        byte2 = strHexCheckSum[0:2]

        checkSumB = (byte1 + byte2)

        return checkSumB

    def _crc32(self, data):

        crc32 = crcmod.mkCrcFun(0x104C11DB7, rev=True, initCrc=0x564F580A, xorOut=0xFFFFFFFF)
        checkSum = crc32(data)
        return checkSum

    def _crc32fromStr(self, binString):

        crcDataA = bytes.fromhex((binString).decode('ascii'))
        checkSum = self._crc32(crcDataA)
        strHexCheckSum = str(hex(checkSum))[2:]

        strLen = len(strHexCheckSum)
        for i in range(strLen, 8):
            strHexCheckSum = "0" + strHexCheckSum

        byte1 = strHexCheckSum[6:8]
        byte2 = strHexCheckSum[4:6]
        byte3 = strHexCheckSum[2:4]
        byte4 = strHexCheckSum[0:2]

        checkSumB = (byte1 + byte2 + byte3 + byte4)

        return checkSumB

    def discover(self, manualComputerIP=""):

        if not manualComputerIP:
            self._auto_computerIP()
        else:
            self._computerIP = manualComputerIP

        if self._computerIP:
            print("\nUsing computer IP address: " + self._computerIP + "\n")

            lidarSensorIPs, serialNums, ipRangeCodes, sensorTypes = self._searchForSensors(False)

            unique_serialNums = []
            unique_sensors = []
            IP_groups = []
            ID_groups = []

            for i in range(len(lidarSensorIPs)):
                if i == 0:
                    unique_serialNums.append(serialNums[i])
                else:
                    matched = False
                    for j in range(len(unique_serialNums)):
                        if serialNums[i] == unique_serialNums[j]:
                            matched = True
                            break
                    if not matched:
                        unique_serialNums.append(serialNums[i])

            for i in range(len(unique_serialNums)):
                count = 0
                IPs = ""
                IDs = ""
                for j in range(len(serialNums)):
                    if serialNums[j] == unique_serialNums[i]:
                        count += 1
                        IPs += lidarSensorIPs[j] + ","
                        IDs += str(ipRangeCodes[j]) + ","
                if count == 1:
                    unique_sensors.append(sensorTypes[i])
                elif count == 3:
                    unique_sensors.append("Mid-100")
                IP_groups.append(IPs[:-1])
                ID_groups.append(IDs[:-1])

            if len(unique_serialNums) > 0:
                for i in range(len(unique_serialNums)):
                    IPs_list = IP_groups[i].split(',')
                    IDs_list = ID_groups[i].split(',')
                    IPs_mess = ""
                    last_IP_num = []
                    for j in range(len(IPs_list)):
                        last_IP_num.append(int(IPs_list[j].split('.')[3]))
                    last_IP_num.sort()
                    for j in range(len(last_IP_num)):
                        for k in range(len(IPs_list)):
                            if last_IP_num[j] == int(IPs_list[k].split('.')[3]):
                                numspaces = " "
                                if last_IP_num[j] < 100:
                                    numspaces += " "
                                if last_IP_num[j] < 10:
                                    numspaces += " "
                                IPs_mess += str(IPs_list[k]) + numspaces + "(ID: " + str(IDs_list[k]) + ")\n                 "
                                break
                    print("   *** Discovered a Livox sensor ***")
                    print("           Type: " + unique_sensors[i])
                    print("         Serial: " + unique_serialNums[i])
                    print("          IP(s): " + IPs_mess)

            else:
                print("Did not discover any Livox sensors, check communication and power cables and network settings")

        else:
            print("*** ERROR: Failed to auto determine computer IP address ***")
