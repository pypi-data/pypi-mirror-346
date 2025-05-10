import binascii
import select
import socket
import struct
import threading
import time
import sys
import os
from pathlib import Path

import crcmod
import numpy as np


class _heartbeatThread(object):

    def __init__(self, interval, transmit_socket, send_to_IP, send_to_port, send_command, showMessages, format_spaces):
        self.interval = interval
        self.IP = send_to_IP
        self.port = send_to_port
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

                if select.select([self.t_socket], [], [], 0.1)[0]:
                    binData, addr = self.t_socket.recvfrom(22)
                    tempObj = openpylivoxv2()
                    _, ack, cmd_set, cmd_id, ret_code_bin = tempObj._parseResp(binData)

                    if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "3":
                        ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                        if ret_code != 0:
                            if self._showMessages: print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     incorrect heartbeat response")
                        else:
                            self.work_state = int.from_bytes(ret_code_bin[1], byteorder='little')

                            # TODO: read and store the lidar status codes from heartbeat response (right now only being read from data stream)

                            if self.work_state == 4:
                                print("   " + self.IP + self._format_spaces + self._format_spaces + "   -->     *** ERROR: HEARTBEAT ERROR MESSAGE RECEIVED ***")
                                sys.exit(0)
                    elif ack == "MSG (message)" and cmd_set == "General" and cmd_id == "7":
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


class _dataCaptureThread(object):

    def __init__(self, sensorIP, data_socket, imu_socket, filePathAndName, fileType, secsToWait, duration, firmwareType, showMessages, format_spaces, deviceType):

        self.startTime = -1
        self.sensorIP = sensorIP
        self.d_socket = data_socket
        self.i_socket = imu_socket
        self.filePathAndName = filePathAndName
        # fileType 0 = Stored ASCII, 1 = Real-time ASCII, 2 = Real-time BINARY
        self.fileType = fileType
        self.secsToWait = secsToWait
        self.duration = duration
        self.firmwareType = firmwareType
        self.started = True
        self.isCapturing = False
        self.dataType = -1
        self.numPts = 0
        self.nullPts = 0
        self.imu_records = 0
        self._showMessages = showMessages
        self._format_spaces = format_spaces
        self._deviceType = deviceType
        self.system_status = -1
        self.temp_status = -1
        self.volt_status = -1
        self.motor_status = -1
        self.dirty_status = -1
        self.firmware_status = -1
        self.pps_status = -1
        self.device_status = -1
        self.fan_status = -1
        self.self_heating_status = -1
        self.ptp_status = -1
        self.time_sync_status = -1

        if duration == 0:
            self.duration = 126230400  # 4 years of time (so technically not indefinite)

        self.thread = None

        if self.fileType == 1:
            self.thread = threading.Thread(target=self.run_realtime_csv, args=())
        elif self.fileType == 2:
            self.thread = threading.Thread(target=self.run_realtime_bin, args=())
        else:
            self.thread = threading.Thread(target=self.run, args=())

        self.thread.daemon = True
        self.thread.start()

    def run(self):

        # read point cloud data packet to get packet version and datatype
        # keep looping to 'consume' data that we don't want included in the captured point cloud data

        breakByCapture = False
        while True:

            if self.started:
                selectTest = select.select([self.d_socket], [], [], 0)
                if selectTest[0]:
                    data_pc, addr = self.d_socket.recvfrom(1500)
                    version = int.from_bytes(data_pc[0:1], byteorder='little')
                    self.dataType = int.from_bytes(data_pc[9:10], byteorder='little')
                    timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                    timestamp1 = self.getTimestamp(data_pc[10:18], timestamp_type)
                    self.updateStatus(data_pc[4:8])
                    if self.isCapturing:
                        self.startTime = timestamp1
                        breakByCapture = True
                        break
            else:
                break

        if breakByCapture:

            # check data packet is as expected (first byte anyways)
            if version == 5:

                # lists to capture point cloud data stream info
                # TODO: should use an object, I know, I know!
                timestamps = []
                timestamp_types = []
                slot_ids = []
                lidar_ids = []
                coord1s = []
                coord2s = []
                coord3s = []
                intensities = []
                returnNums = []

                # delayed start to capturing data check (secsToWait parameter)
                timestamp2 = self.startTime
                while True:
                    if self.started:
                        timeSinceStart = timestamp2 - self.startTime
                        if timeSinceStart <= self.secsToWait:
                            # read data from receive buffer and keep 'consuming' it
                            if select.select([self.d_socket], [], [], 0)[0]:
                                data_pc, addr = self.d_socket.recvfrom(1500)
                                timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                                timestamp2 = self.getTimestamp(data_pc[10:18], timestamp_type)
                                self.updateStatus(data_pc[4:8])
                        else:
                            self.startTime = timestamp2
                            break
                    else:
                        break

                if self._showMessages: print("   " + self.sensorIP + self._format_spaces + self._format_spaces + "   -->     CAPTURING DATA...")

                # duration adjustment (trying to get exactly 100,000 points / sec)
                if self.duration != 126230400:
                    if self.firmwareType == 1:
                        self.duration += (0.001 * (self.duration / 2.0))
                    elif self.firmwareType == 2:
                        self.duration += (0.0005 * (self.duration / 2.0))
                    elif self.firmwareType == 3:
                        self.duration += (0.00055 * (self.duration / 2.0))

                timestamp_sec = self.startTime
                # main loop that captures the desired point cloud data
                while True:
                    if self.started:
                        timeSinceStart = timestamp_sec - self.startTime

                        if timeSinceStart <= self.duration:

                            # read data from receive buffer
                            if select.select([self.d_socket], [], [], 0)[0]:
                                data_pc, addr = self.d_socket.recvfrom(1500)

                                version = int.from_bytes(data_pc[0:1], byteorder='little')
                                slot_id = int.from_bytes(data_pc[1:2], byteorder='little')
                                lidar_id = int.from_bytes(data_pc[2:3], byteorder='little')

                                # byte 3 is reserved

                                # update lidar status information
                                self.updateStatus(data_pc[4:8])

                                timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                                timestamp_sec = self.getTimestamp(data_pc[10:18], timestamp_type)

                                bytePos = 18

                                # single return firmware (most common)
                                if self.firmwareType == 1:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.00001

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            # X coordinate
                                            coord1 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # Y coordinate
                                            coord2 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # Z coordinate
                                            coord3 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # intensity
                                            intensity = data_pc[bytePos:bytePos + 1]
                                            bytePos += 1

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            timestamps.append(timestamp_sec)
                                            timestamp_types.append(timestamp_type)
                                            slot_ids.append(slot_id)
                                            lidar_ids.append(lidar_id)
                                            coord1s.append(coord1)
                                            coord2s.append(coord2)
                                            coord3s.append(coord3)
                                            intensities.append(intensity)

                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            # distance
                                            coord1 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # zenith
                                            coord2 = data_pc[bytePos:bytePos + 2]
                                            bytePos += 2

                                            # azimuth
                                            coord3 = data_pc[bytePos:bytePos + 2]
                                            bytePos += 2

                                            # intensity
                                            intensity = data_pc[bytePos:bytePos + 1]
                                            bytePos += 1

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            timestamps.append(timestamp_sec)
                                            timestamp_types.append(timestamp_type)
                                            slot_ids.append(slot_id)
                                            lidar_ids.append(lidar_id)
                                            coord1s.append(coord1)
                                            coord2s.append(coord2)
                                            coord3s.append(coord3)
                                            intensities.append(intensity)

                                # double return firmware
                                elif self.firmwareType == 2:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.00001

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # X coordinate
                                            coord1 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # Y coordinate
                                            coord2 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # Z coordinate
                                            coord3 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # intensity
                                            intensity = data_pc[bytePos:bytePos + 1]
                                            bytePos += 1

                                            zeroORtwo = i % 2

                                            # timestamp
                                            timestamp_sec += float(not (zeroORtwo)) * 0.00001

                                            # return number
                                            returnNum += zeroORtwo * 1

                                            timestamps.append(timestamp_sec)
                                            timestamp_types.append(timestamp_type)
                                            slot_ids.append(slot_id)
                                            lidar_ids.append(lidar_id)
                                            coord1s.append(coord1)
                                            coord2s.append(coord2)
                                            coord3s.append(coord3)
                                            intensities.append(intensity)
                                            returnNums.append(returnNum)

                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # distance
                                            coord1 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # zenith
                                            coord2 = data_pc[bytePos:bytePos + 2]
                                            bytePos += 2

                                            # azimuth
                                            coord3 = data_pc[bytePos:bytePos + 2]
                                            bytePos += 2

                                            # intensity
                                            intensity = data_pc[bytePos:bytePos + 1]
                                            bytePos += 1

                                            zeroORtwo = i % 2

                                            # timestamp
                                            timestamp_sec += float(not (zeroORtwo)) * 0.00001

                                            # return number
                                            returnNum += zeroORtwo * 1

                                            timestamps.append(timestamp_sec)
                                            timestamp_types.append(timestamp_type)
                                            slot_ids.append(slot_id)
                                            lidar_ids.append(lidar_id)
                                            coord1s.append(coord1)
                                            coord2s.append(coord2)
                                            coord3s.append(coord3)
                                            intensities.append(intensity)
                                            returnNums.append(returnNum)

                                # triple return firmware
                                elif self.firmwareType == 3:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.000016666

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # X coordinate
                                            coord1 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # Y coordinate
                                            coord2 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # Z coordinate
                                            coord3 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # intensity
                                            intensity = data_pc[bytePos:bytePos + 1]
                                            bytePos += 1

                                            zeroORoneORtwo = i % 3

                                            # timestamp
                                            timestamp_sec += float(not (zeroORoneORtwo)) * 0.000016666

                                            # return number
                                            returnNum += zeroORoneORtwo * 1

                                            timestamps.append(timestamp_sec)
                                            timestamp_types.append(timestamp_type)
                                            slot_ids.append(slot_id)
                                            lidar_ids.append(lidar_id)
                                            coord1s.append(coord1)
                                            coord2s.append(coord2)
                                            coord3s.append(coord3)
                                            intensities.append(intensity)
                                            returnNums.append(returnNum)

                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # distance
                                            coord1 = data_pc[bytePos:bytePos + 4]
                                            bytePos += 4

                                            # zenith
                                            coord2 = data_pc[bytePos:bytePos + 2]
                                            bytePos += 2

                                            # azimuth
                                            coord3 = data_pc[bytePos:bytePos + 2]
                                            bytePos += 2

                                            # intensity
                                            intensity = data_pc[bytePos:bytePos + 1]
                                            bytePos += 1

                                            zeroORoneORtwo = i % 3

                                            # timestamp
                                            timestamp_sec += float(not (zeroORoneORtwo)) * 0.000016666

                                            # return number
                                            returnNum += zeroORoneORtwo * 1

                                            timestamps.append(timestamp_sec)
                                            timestamp_types.append(timestamp_type)
                                            slot_ids.append(slot_id)
                                            lidar_ids.append(lidar_id)
                                            coord1s.append(coord1)
                                            coord2s.append(coord2)
                                            coord3s.append(coord3)
                                            intensities.append(intensity)
                                            returnNums.append(returnNum)

                        # duration check (exit point)
                        else:
                            self.started = False
                            self.isCapturing = False
                            break
                    # thread still running check (exit point)
                    else:
                        break

                # make sure some data was captured
                lenData = len(coord1s)
                if lenData > 0:

                    if self._showMessages: print(
                        "   " + self.sensorIP + self._format_spaces + self._format_spaces + "   -->     writing data to ASCII file: " + self.filePathAndName)
                    csvFile = open(self.filePathAndName, "w")

                    numPts = 0
                    nullPts = 0

                    # TODO: apply coordinate transformations to the raw X, Y, Z point cloud data based on the extrinsic parameters
                    # rotation definitions and the sequence they are applied is always a bit of a head scratcher, lots of different definitions
                    # Geospatial/Traditional Photogrammetry/Computer Vision/North America/Europe all use different approaches

                    # single return fimware
                    if self.firmwareType == 1:

                        # Cartesian
                        if self.dataType == 0:
                            csvFile.write("//X,Y,Z,Inten-sity,Time\n")
                            for i in range(0, lenData):
                                coord1 = round(float(struct.unpack('<i', coord1s[i])[0]) / 1000.0, 3)
                                coord2 = round(float(struct.unpack('<i', coord2s[i])[0]) / 1000.0, 3)
                                coord3 = round(float(struct.unpack('<i', coord3s[i])[0]) / 1000.0, 3)
                                if coord1 or coord2 or coord3:
                                    numPts += 1
                                    csvFile.write("{0:.3f}".format(coord1) \
                                                  + "," + "{0:.3f}".format(coord2) \
                                                  + "," + "{0:.3f}".format(coord3) \
                                                  + "," + str(int.from_bytes(intensities[i], byteorder='little')) \
                                                  + "," + "{0:.6f}".format(timestamps[i]) + "\n")
                                else:
                                    nullPts += 1

                        # Spherical
                        elif self.dataType == 1:
                            csvFile.write("//Distance,Zenith,Azimuth,Inten-sity,Time\n")
                            for i in range(0, lenData):
                                coord1 = round(float(struct.unpack('<I', coord1s[i])[0]) / 1000.0, 3)
                                coord2 = round(float(struct.unpack('<H', coord2s[i])[0]) / 100.0, 2)
                                coord3 = round(float(struct.unpack('<H', coord3s[i])[0]) / 100.0, 2)
                                if coord1:
                                    numPts += 1
                                    csvFile.write("{0:.3f}".format(coord1) \
                                                  + "," + "{0:.2f}".format(coord2) \
                                                  + "," + "{0:.2f}".format(coord3) \
                                                  + "," + str(int.from_bytes(intensities[i], byteorder='little')) \
                                                  + "," + "{0:.6f}".format(timestamps[i]) + "\n")
                                else:
                                    nullPts += 1

                    # multiple returns firmware
                    elif self.firmwareType == 2 or self.firmwareType == 3:

                        # Cartesian
                        if self.dataType == 0:
                            csvFile.write("//X,Y,Z,Inten-sity,Time,ReturnNum\n")
                            for i in range(0, lenData):
                                coord1 = round(float(struct.unpack('<i', coord1s[i])[0]) / 1000.0, 3)
                                coord2 = round(float(struct.unpack('<i', coord2s[i])[0]) / 1000.0, 3)
                                coord3 = round(float(struct.unpack('<i', coord3s[i])[0]) / 1000.0, 3)
                                if coord1 or coord2 or coord3:
                                    numPts += 1
                                    csvFile.write("{0:.3f}".format(coord1) \
                                                  + "," + "{0:.3f}".format(coord2) \
                                                  + "," + "{0:.3f}".format(coord3) \
                                                  + "," + str(int.from_bytes(intensities[i], byteorder='little')) \
                                                  + "," + "{0:.6f}".format(timestamps[i]) \
                                                  + "," + str(returnNums[i]) + "\n")
                                else:
                                    nullPts += 1

                        # Spherical
                        elif self.dataType == 1:
                            csvFile.write("//Distance,Zenith,Azimuth,Inten-sity,Time,ReturnNum\n")
                            for i in range(0, lenData):
                                coord1 = round(float(struct.unpack('<I', coord1s[i])[0]) / 1000.0, 3)
                                coord2 = round(float(struct.unpack('<H', coord2s[i])[0]) / 100.0, 2)
                                coord3 = round(float(struct.unpack('<H', coord3s[i])[0]) / 100.0, 2)
                                if coord1:
                                    numPts += 1
                                    csvFile.write("{0:.3f}".format(coord1) \
                                                  + "," + "{0:.2f}".format(coord2) \
                                                  + "," + "{0:.2f}".format(coord3) \
                                                  + "," + str(int.from_bytes(intensities[i], byteorder='little')) \
                                                  + "," + "{0:.6f}".format(timestamps[i]) \
                                                  + "," + str(returnNums[i]) + "\n")
                                else:
                                    nullPts += 1

                    self.numPts = numPts
                    self.nullPts = nullPts

                    if self._showMessages:
                        print("   " + self.sensorIP + self._format_spaces + self._format_spaces + "   -->     closed ASCII file: " + self.filePathAndName)
                        print(
                            "                    (points: " + str(numPts) + " good, " + str(nullPts) + " null, " + str(
                                numPts + nullPts) + " total)")
                    csvFile.close()

                else:
                    if self._showMessages: print(
                        "   " + self.sensorIP + self._format_spaces + "   -->     WARNING: no point cloud data was captured")

            else:
                if self._showMessages: print("   " + self.sensorIP + self._format_spaces + "   -->     Incorrect lidar packet version")

    def run_realtime_csv(self):

        # read point cloud data packet to get packet version and datatype
        # keep looping to 'consume' data that we don't want included in the captured point cloud data

        breakByCapture = False
        while True:

            if self.started:
                selectTest = select.select([self.d_socket], [], [], 0)
                if selectTest[0]:
                    data_pc, addr = self.d_socket.recvfrom(1500)
                    version = int.from_bytes(data_pc[0:1], byteorder='little')
                    self.dataType = int.from_bytes(data_pc[9:10], byteorder='little')
                    timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                    timestamp1 = self.getTimestamp(data_pc[10:18], timestamp_type)
                    self.updateStatus(data_pc[4:8])
                    if self.isCapturing:
                        self.startTime = timestamp1
                        breakByCapture = True
                        break
            else:
                break

        if breakByCapture:

            # check data packet is as expected (first byte anyways)
            if version == 5:

                # delayed start to capturing data check (secsToWait parameter)
                timestamp2 = self.startTime
                while True:
                    if self.started:
                        timeSinceStart = timestamp2 - self.startTime
                        if timeSinceStart <= self.secsToWait:
                            # read data from receive buffer and keep 'consuming' it
                            if select.select([self.d_socket], [], [], 0)[0]:
                                data_pc, addr = self.d_socket.recvfrom(1500)
                                timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                                timestamp2 = self.getTimestamp(data_pc[10:18], timestamp_type)
                                self.updateStatus(data_pc[4:8])
                        else:
                            self.startTime = timestamp2
                            break
                    else:
                        break

                if self._showMessages: print("   " + self.sensorIP + self._format_spaces + "   -->     CAPTURING DATA...")

                # duration adjustment (trying to get exactly 100,000 points / sec)
                if self.duration != 126230400:
                    if self.firmwareType == 1:
                        self.duration += (0.001 * (self.duration / 2.0))
                    elif self.firmwareType == 2:
                        self.duration += (0.0005 * (self.duration / 2.0))
                    elif self.firmwareType == 3:
                        self.duration += (0.00055 * (self.duration / 2.0))

                timestamp_sec = self.startTime

                if self._showMessages: print(
                    "   " + self.sensorIP + self._format_spaces + "   -->     writing real-time data to ASCII file: " + self.filePathAndName)
                csvFile = open(self.filePathAndName, "w", 1)

                numPts = 0
                nullPts = 0

                # write header info
                if self.firmwareType == 1:  # single return firmware
                    if self.dataType == 0:  # Cartesian
                        csvFile.write("//X,Y,Z,Inten-sity,Time\n")
                    elif self.dataType == 1:  # Spherical
                        csvFile.write("//Distance,Zenith,Azimuth,Inten-sity,Time\n")
                elif self.firmwareType == 2 or self.firmwareType == 3:  # double or triple return firmware
                    if self.dataType == 0:  # Cartesian
                        csvFile.write("//X,Y,Z,Inten-sity,Time,ReturnNum\n")
                    elif self.dataType == 1:  # Spherical
                        csvFile.write("//Distance,Zenith,Azimuth,Inten-sity,Time,ReturnNum\n")

                # main loop that captures the desired point cloud data
                while True:
                    if self.started:
                        timeSinceStart = timestamp_sec - self.startTime

                        if timeSinceStart <= self.duration:

                            # read data from receive buffer
                            if select.select([self.d_socket], [], [], 0)[0]:
                                data_pc, addr = self.d_socket.recvfrom(1500)

                                # version = int.from_bytes(data_pc[0:1], byteorder='little')
                                # slot_id = int.from_bytes(data_pc[1:2], byteorder='little')
                                # lidar_id = int.from_bytes(data_pc[2:3], byteorder='little')

                                # byte 3 is reserved

                                # update lidar status information
                                self.updateStatus(data_pc[4:8])

                                timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                                timestamp_sec = self.getTimestamp(data_pc[10:18], timestamp_type)

                                bytePos = 18

                                # single return firmware (most common)
                                if self.firmwareType == 1:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.00001

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            if coord2:
                                                # X coordinate
                                                coord1 = struct.unpack('<i', data_pc[bytePos:bytePos + 4])[0]
                                                bytePos += 8
                                                # Z coordinate
                                                coord3 = struct.unpack('<i', data_pc[bytePos:bytePos + 4])[0]
                                                bytePos += 4
                                                # intensity
                                                intensity = int.from_bytes(data_pc[bytePos:bytePos + 1],
                                                                           byteorder='little')
                                                bytePos += 1

                                                numPts += 1
                                                csvFile.write(
                                                    "{0:.3f}".format(float(coord1) / 1000.0) + "," + "{0:.3f}".format(
                                                        float(coord2) / 1000.0) + "," + "{0:.3f}".format(
                                                        float(coord3) / 1000.0) + "," + str(
                                                        intensity) + "," + "{0:.6f}".format(timestamp_sec) + "\n")
                                            else:
                                                nullPts += 1
                                                bytePos += 13

                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            if coord1:
                                                bytePos += 4
                                                # Zenith coordinate
                                                coord2 = struct.unpack('<H', data_pc[bytePos:bytePos + 2])[0]
                                                bytePos += 2
                                                # Azimuth coordinate
                                                coord3 = struct.unpack('<H', data_pc[bytePos:bytePos + 2])[0]
                                                bytePos += 2
                                                # intensity
                                                intensity = int.from_bytes(data_pc[bytePos:bytePos + 1],
                                                                           byteorder='little')
                                                bytePos += 1

                                                numPts += 1
                                                csvFile.write(
                                                    "{0:.3f}".format(float(coord1) / 1000.0) + "," + "{0:.2f}".format(
                                                        float(coord2) / 100.0) + "," + "{0:.2f}".format(
                                                        float(coord3) / 100.0) + "," + str(
                                                        intensity) + "," + "{0:.6f}".format(timestamp_sec) + "\n")
                                            else:
                                                nullPts += 1
                                                bytePos += 9

                                # double return firmware
                                elif self.firmwareType == 2:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.00001

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            zeroORtwo = i % 2

                                            # timestamp
                                            timestamp_sec += float(not (zeroORtwo)) * 0.00001

                                            # return number
                                            returnNum += zeroORtwo * 1

                                            if coord2:
                                                # X coordinate
                                                coord1 = struct.unpack('<i', data_pc[bytePos:bytePos + 4])[0]
                                                bytePos += 8
                                                # Z coordinate
                                                coord3 = struct.unpack('<i', data_pc[bytePos:bytePos + 4])[0]
                                                bytePos += 4
                                                # intensity
                                                intensity = int.from_bytes(data_pc[bytePos:bytePos + 1],
                                                                           byteorder='little')
                                                bytePos += 1

                                                numPts += 1
                                                csvFile.write(
                                                    "{0:.3f}".format(float(coord1) / 1000.0) + "," + "{0:.3f}".format(
                                                        float(coord2) / 1000.0) + "," + "{0:.3f}".format(
                                                        float(coord3) / 1000.0) + "," + str(
                                                        intensity) + "," + "{0:.6f}".format(timestamp_sec) + "," + str(
                                                        returnNum) + "\n")
                                            else:
                                                nullPts += 1
                                                bytePos += 13

                                                # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            zeroORtwo = i % 2

                                            # timestamp
                                            timestamp_sec += float(not (zeroORtwo)) * 0.00001

                                            # return number
                                            returnNum += zeroORtwo * 1

                                            if coord1:
                                                bytePos += 4
                                                # Zenith coordinate
                                                coord2 = struct.unpack('<H', data_pc[bytePos:bytePos + 2])[0]
                                                bytePos += 2
                                                # Azimuth coordinate
                                                coord3 = struct.unpack('<H', data_pc[bytePos:bytePos + 2])[0]
                                                bytePos += 2
                                                # intensity
                                                intensity = int.from_bytes(data_pc[bytePos:bytePos + 1],
                                                                           byteorder='little')
                                                bytePos += 1

                                                numPts += 1
                                                csvFile.write(
                                                    "{0:.3f}".format(float(coord1) / 1000.0) + "," + "{0:.2f}".format(
                                                        float(coord2) / 100.0) + "," + "{0:.2f}".format(
                                                        float(coord3) / 100.0) + "," + str(
                                                        intensity) + "," + "{0:.6f}".format(timestamp_sec) + "," + str(
                                                        returnNum) + "\n")
                                            else:
                                                nullPts += 1
                                                bytePos += 9


                                # triple return firmware
                                elif self.firmwareType == 3:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.000016666

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            zeroORoneORtwo = i % 3

                                            # timestamp
                                            timestamp_sec += float(not (zeroORoneORtwo)) * 0.000016666

                                            # return number
                                            returnNum += zeroORoneORtwo * 1

                                            if coord2:
                                                # X coordinate
                                                coord1 = struct.unpack('<i', data_pc[bytePos:bytePos + 4])[0]
                                                bytePos += 8
                                                # Z coordinate
                                                coord3 = struct.unpack('<i', data_pc[bytePos:bytePos + 4])[0]
                                                bytePos += 4
                                                # intensity
                                                intensity = int.from_bytes(data_pc[bytePos:bytePos + 1],
                                                                           byteorder='little')
                                                bytePos += 1

                                                numPts += 1
                                                csvFile.write(
                                                    "{0:.3f}".format(float(coord1) / 1000.0) + "," + "{0:.3f}".format(
                                                        float(coord2) / 1000.0) + "," + "{0:.3f}".format(
                                                        float(coord3) / 1000.0) + "," + str(
                                                        intensity) + "," + "{0:.6f}".format(timestamp_sec) + "," + str(
                                                        returnNum) + "\n")
                                            else:
                                                nullPts += 1
                                                bytePos += 13


                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            zeroORoneORtwo = i % 3

                                            # timestamp
                                            timestamp_sec += float(not (zeroORoneORtwo)) * 0.000016666

                                            # return number
                                            returnNum += zeroORoneORtwo * 1

                                            if coord1:
                                                bytePos += 4
                                                # Zenith coordinate
                                                coord2 = struct.unpack('<H', data_pc[bytePos:bytePos + 2])[0]
                                                bytePos += 2
                                                # Azimuth coordinate
                                                coord3 = struct.unpack('<H', data_pc[bytePos:bytePos + 2])[0]
                                                bytePos += 2
                                                # intensity
                                                intensity = int.from_bytes(data_pc[bytePos:bytePos + 1],
                                                                           byteorder='little')
                                                bytePos += 1

                                                numPts += 1
                                                csvFile.write(
                                                    "{0:.3f}".format(float(coord1) / 1000.0) + "," + "{0:.2f}".format(
                                                        float(coord2) / 100.0) + "," + "{0:.2f}".format(
                                                        float(coord3) / 100.0) + "," + str(
                                                        intensity) + "," + "{0:.6f}".format(timestamp_sec) + "," + str(
                                                        returnNum) + "\n")
                                            else:
                                                nullPts += 1
                                                bytePos += 9

                        # duration check (exit point)
                        else:
                            self.started = False
                            self.isCapturing = False
                            break
                    # thread still running check (exit point)
                    else:
                        break

                self.numPts = numPts
                self.nullPts = nullPts

                if self._showMessages:
                    print("   " + self.sensorIP + self._format_spaces + "   -->     closed ASCII file: " + self.filePathAndName)
                    print("                                (points: " + str(numPts) + " good, " + str(nullPts) + " null, " + str(numPts + nullPts) + " total)")

                csvFile.close()

            else:
                if self._showMessages: print("   " + self.sensorIP + self._format_spaces + "   -->     Incorrect lidar packet version")

    def run_realtime_bin(self):

        # read point cloud data packet to get packet version and datatype
        # keep looping to 'consume' data that we don't want included in the captured point cloud data

        breakByCapture = False

        #used to check if the sensor is a Mid-100
        deviceCheck = 0
        try:
            deviceCheck = int(self._deviceType[4:7])
        except:
            pass

        while True:

            if self.started:
                selectTest = select.select([self.d_socket], [], [], 0)
                if selectTest[0]:
                    data_pc, addr = self.d_socket.recvfrom(1500)
                    version = int.from_bytes(data_pc[0:1], byteorder='little')
                    self.dataType = int.from_bytes(data_pc[9:10], byteorder='little')
                    timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                    timestamp1 = self.getTimestamp(data_pc[10:18], timestamp_type)
                    self.updateStatus(data_pc[4:8])
                    if self.isCapturing:
                        self.startTime = timestamp1
                        breakByCapture = True
                        break
            else:
                break

        if breakByCapture:

            # check data packet is as expected (first byte anyways)
            if version == 5:

                # delayed start to capturing data check (secsToWait parameter)
                timestamp2 = self.startTime
                while True:
                    if self.started:
                        timeSinceStart = timestamp2 - self.startTime
                        if timeSinceStart <= self.secsToWait:
                            # read data from receive buffer and keep 'consuming' it
                            if select.select([self.d_socket], [], [], 0)[0]:
                                data_pc, addr = self.d_socket.recvfrom(1500)
                                timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                                timestamp2 = self.getTimestamp(data_pc[10:18], timestamp_type)
                                self.updateStatus(data_pc[4:8])
                            if select.select([self.i_socket], [], [], 0)[0]:
                                imu_data, addr2 = self.i_socket.recvfrom(50)
                        else:
                            self.startTime = timestamp2
                            break
                    else:
                        break

                if self._showMessages: print("   " + self.sensorIP + self._format_spaces + "   -->     CAPTURING DATA...")

                timestamp_sec = self.startTime

                if self._showMessages: print(
                    "   " + self.sensorIP + self._format_spaces + "   -->     writing real-time data to BINARY file: " + self.filePathAndName)
                binFile = open(self.filePathAndName, "wb")
                IMU_file = None

                IMU_reporting = False
                numPts = 0
                nullPts = 0
                imu_records = 0

                # write header info to know how to parse the data later
                binFile.write(str.encode("openpylivoxv2"))
                binFile.write(struct.pack('<h', self.firmwareType))
                binFile.write(struct.pack('<h', self.dataType))

                # main loop that captures the desired point cloud data
                while True:
                    if self.started:
                        timeSinceStart = timestamp_sec - self.startTime

                        if timeSinceStart <= self.duration:

                            # read points from data buffer
                            if select.select([self.d_socket], [], [], 0)[0]:
                                data_pc, addr = self.d_socket.recvfrom(1500)

                                # version = int.from_bytes(data_pc[0:1], byteorder='little')
                                # slot_id = int.from_bytes(data_pc[1:2], byteorder='little')
                                # lidar_id = int.from_bytes(data_pc[2:3], byteorder='little')

                                # byte 3 is reserved

                                # update lidar status information
                                self.updateStatus(data_pc[4:8])
                                dataType = int.from_bytes(data_pc[9:10], byteorder='little')
                                timestamp_type = int.from_bytes(data_pc[8:9], byteorder='little')
                                timestamp_sec = self.getTimestamp(data_pc[10:18], timestamp_type)

                                bytePos = 18

                                # single return firmware (relevant for Mid-40 and Mid-100)
                                # Horizon and Tele-15 sensors also fall under this 'if' statement
                                if self.firmwareType == 1:

                                    # Cartesian Coordinate System
                                    if dataType == 0:
                                        # to account for first point's timestamp being increment in the loop
                                        timestamp_sec -= 0.00001

                                        for i in range(0, 100):

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            if deviceCheck == 100:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 13])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                            else:
                                                if coord2:
                                                    numPts += 1
                                                    binFile.write(data_pc[bytePos:bytePos + 13])
                                                    binFile.write(struct.pack('<d', timestamp_sec))
                                                else:
                                                    nullPts += 1

                                            bytePos += 13

                                    # Spherical Coordinate System
                                    elif dataType == 1:
                                        # to account for first point's timestamp being increment in the loop
                                        timestamp_sec -= 0.00001

                                        for i in range(0, 100):

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            if coord1:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 9])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                            else:
                                                nullPts += 1

                                            bytePos += 9

                                    # Horizon and Tele-15 Cartesian (single return)
                                    elif dataType == 2:
                                        # to account for first point's timestamp being increment in the loop
                                        timestamp_sec -= 0.000004167
                                        for i in range(0, 96):

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            # timestamp
                                            timestamp_sec += 0.000004167

                                            if coord2:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 14])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                            else:
                                                nullPts += 1

                                            bytePos += 14

                                    # Horizon and Tele-15 Spherical (single return)
                                    elif dataType == 3:
                                        # to account for first point's timestamp being increment in the loop
                                        timestamp_sec -= 0.000004167
                                        for i in range(0, 96):

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            if coord1:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 10])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                            else:
                                                nullPts += 1

                                            bytePos += 10

                                    # Horizon and Tele-15 Cartesian (dual return)
                                    elif dataType == 4:
                                        # to account for first point's timestamp being increment in the loop
                                        timestamp_sec -= 0.000002083
                                        for i in range(0, 48):

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            # timestamp
                                            timestamp_sec += 0.000002083

                                            if coord2:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 28])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                            else:
                                                nullPts += 1

                                            bytePos += 28

                                    # Horizon and Tele-15 Spherical (dual return)
                                    elif dataType == 5:
                                        # to account for first point's timestamp being increment in the loop
                                        timestamp_sec -= 0.000002083
                                        for i in range(0, 48):

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            # timestamp
                                            timestamp_sec += 0.00001

                                            if coord1:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 16])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                            else:
                                                nullPts += 1

                                            bytePos += 16

                                # double return firmware (Mid-40 and Mid-100 only)
                                elif self.firmwareType == 2:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.00001

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            zeroORtwo = i % 2

                                            # timestamp
                                            timestamp_sec += float(not (zeroORtwo)) * 0.00001

                                            # return number
                                            returnNum += zeroORtwo * 1

                                            if deviceCheck == 100:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 13])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                                binFile.write(str.encode(str(returnNum)))
                                            else:
                                                if coord2:
                                                    numPts += 1
                                                    binFile.write(data_pc[bytePos:bytePos + 13])
                                                    binFile.write(struct.pack('<d', timestamp_sec))
                                                    binFile.write(str.encode(str(returnNum)))
                                                else:
                                                    nullPts += 1

                                            bytePos += 13

                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            zeroORtwo = i % 2

                                            # timestamp
                                            timestamp_sec += float(not (zeroORtwo)) * 0.00001

                                            # return number
                                            returnNum += zeroORtwo * 1

                                            if coord1:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 9])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                                binFile.write(str.encode(str(returnNum)))
                                            else:
                                                nullPts += 1

                                            bytePos += 9

                                # triple return firmware (Mid-40 and Mid-100 only)
                                elif self.firmwareType == 3:
                                    # to account for first point's timestamp being increment in the loop
                                    timestamp_sec -= 0.000016667

                                    # Cartesian Coordinate System
                                    if self.dataType == 0:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Y coordinate (check for non-zero)
                                            coord2 = struct.unpack('<i', data_pc[bytePos + 4:bytePos + 8])[0]

                                            zeroORoneORtwo = i % 3

                                            # timestamp
                                            timestamp_sec += float(not (zeroORoneORtwo)) * 0.000016666

                                            # return number
                                            returnNum += zeroORoneORtwo * 1

                                            if deviceCheck == 100:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 13])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                                binFile.write(str.encode(str(returnNum)))
                                            else:
                                                if coord2:
                                                    numPts += 1
                                                    binFile.write(data_pc[bytePos:bytePos + 13])
                                                    binFile.write(struct.pack('<d', timestamp_sec))
                                                    binFile.write(str.encode(str(returnNum)))
                                                else:
                                                    nullPts += 1

                                            bytePos += 13

                                    # Spherical Coordinate System
                                    elif self.dataType == 1:
                                        for i in range(0, 100):
                                            returnNum = 1

                                            # Distance coordinate (check for non-zero)
                                            coord1 = struct.unpack('<I', data_pc[bytePos:bytePos + 4])[0]

                                            zeroORoneORtwo = i % 3

                                            # timestamp
                                            timestamp_sec += float(not (zeroORoneORtwo)) * 0.000016666

                                            # return number
                                            returnNum += zeroORoneORtwo * 1

                                            if coord1:
                                                numPts += 1
                                                binFile.write(data_pc[bytePos:bytePos + 9])
                                                binFile.write(struct.pack('<d', timestamp_sec))
                                                binFile.write(str.encode(str(returnNum)))
                                            else:
                                                nullPts += 1

                                            bytePos += 9

                            #IMU data capture
                            if select.select([self.i_socket], [], [], 0)[0]:
                                imu_data, addr2 = self.i_socket.recvfrom(50)

                                # version = int.from_bytes(imu_data[0:1], byteorder='little')
                                # slot_id = int.from_bytes(imu_data[1:2], byteorder='little')
                                # lidar_id = int.from_bytes(imu_data[2:3], byteorder='little')

                                # byte 3 is reserved

                                # update lidar status information
                                # self.updateStatus(imu_data[4:8])

                                dataType = int.from_bytes(imu_data[9:10], byteorder='little')
                                timestamp_type = int.from_bytes(imu_data[8:9], byteorder='little')
                                timestamp_sec = self.getTimestamp(imu_data[10:18], timestamp_type)

                                bytePos = 18

                                # Horizon and Tele-15 IMU data packet
                                if dataType == 6:
                                    if not IMU_reporting:
                                        IMU_reporting = True
                                        path_file = Path(self.filePathAndName)
                                        filename = path_file.stem
                                        exten = path_file.suffix
                                        IMU_file = open(filename + "_IMU" + exten, "wb")
                                        IMU_file.write(str.encode("openpylivoxv2_IMU"))

                                    IMU_file.write(imu_data[bytePos:bytePos + 24])
                                    IMU_file.write(struct.pack('<d', timestamp_sec))
                                    imu_records += 1

                        # duration check (exit point)
                        else:
                            self.started = False
                            self.isCapturing = False
                            break
                    # thread still running check (exit point)
                    else:
                        break

                self.numPts = numPts
                self.nullPts = nullPts
                self.imu_records = imu_records

                if self._showMessages:
                    print("   " + self.sensorIP + self._format_spaces + "   -->     closed BINARY file: " + self.filePathAndName)
                    print("                                (points: " + str(numPts) + " good, " + str(nullPts) + " null, " + str(numPts + nullPts) + " total)")
                    if self._deviceType == "Horizon" or self._deviceType == "Tele-15":
                        print("                                (IMU records: " + str(imu_records) + ")")

                binFile.close()

                if IMU_reporting:
                    IMU_file.close()

            else:
                if self._showMessages: print("   " + self.sensorIP + self._format_spaces + "   -->     Incorrect packet version")

    def getTimestamp(self, data_pc, timestamp_type):

        # nanosecond timestamp
        if timestamp_type == 0 or timestamp_type == 1 or timestamp_type == 4:
            timestamp_sec = round(float(struct.unpack('<Q', data_pc[0:8])[0]) / 1000000000.0, 6)  # convert to seconds

        # UTC timestamp, microseconds past the hour
        elif timestamp_type == 3:
            timestamp_year = int.from_bytes(data_pc[0:1], byteorder='little')
            timestamp_month = int.from_bytes(data_pc[1:2], byteorder='little')
            timestamp_day = int.from_bytes(data_pc[2:3], byteorder='little')
            timestamp_hour = int.from_bytes(data_pc[3:4], byteorder='little')
            timestamp_sec = round(float(struct.unpack('<L', data_pc[4:8])[0]) / 1000000.0, 6)  # convert to seconds

            timestamp_sec += timestamp_hour * 3600.  # seconds into the day

            # TODO: check and adjust for hour, day, month and year crossovers

        return timestamp_sec

    # parse lidar status codes and update object properties, can provide real-time warning/error message display
    def updateStatus(self, data_pc):

        status_bits = str(bin(int.from_bytes(data_pc[0:1], byteorder='little')))[2:].zfill(8)
        status_bits += str(bin(int.from_bytes(data_pc[1:2], byteorder='little')))[2:].zfill(8)
        status_bits += str(bin(int.from_bytes(data_pc[2:3], byteorder='little')))[2:].zfill(8)
        status_bits += str(bin(int.from_bytes(data_pc[3:4], byteorder='little')))[2:].zfill(8)

        self.temp_status = int(status_bits[0:2], 2)
        self.volt_status = int(status_bits[2:4], 2)
        self.motor_status = int(status_bits[4:6], 2)
        self.dirty_status = int(status_bits[6:8], 2)
        self.firmware_status = int(status_bits[8:9], 2)
        self.pps_status = int(status_bits[9:10], 2)
        self.device_status = int(status_bits[10:11], 2)
        self.fan_status = int(status_bits[11:12], 2)
        self.self_heating_status = int(status_bits[12:13], 2)
        self.ptp_status = int(status_bits[13:14], 2)
        self.time_sync_status = int(status_bits[14:16], 2)
        self.system_status = int(status_bits[30:], 2)

        # check if the system status in NOT normal
        if self.system_status:
            if self._showMessages:
                if self.system_status == 1:
                    if self.temp_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     * WARNING: temperature *")
                    if self.volt_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     * WARNING: voltage *")
                    if self.motor_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     * WARNING: motor *")
                    if self.dirty_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     * WARNING: dirty or blocked *")
                    if self.device_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     * WARNING: approaching end of service life *")
                    if self.fan_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     * WARNING: fan *")
                elif self.system_status == 2:
                    if self.temp_status == 2:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     *** ERROR: TEMPERATURE ***")
                    if self.volt_status == 2:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     *** ERROR: VOLTAGE ***")
                    if self.motor_status == 2:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     *** ERROR: MOTOR ***")
                    if self.firmware_status == 1:
                        print("   " + self.sensorIP + self._format_spaces + "   -->     *** ERROR: ABNORMAL FIRMWARE ***")

    # returns latest status Codes from within the point cloud data packet
    def statusCodes(self):

        return [self.system_status, self.temp_status, self.volt_status, self.motor_status, self.dirty_status,
                self.firmware_status, self.pps_status, self.device_status, self.fan_status, self.self_heating_status,
                self.ptp_status, self.time_sync_status]

    def stop(self):

        self.started = False
        self.thread.join()


class openpylivoxv2(object):    # Standard protocol commands (for non-Mid360)
    _CMD_QUERY =                  bytes.fromhex((b'AA010F0000000004D70002AE8A8A7B').decode('ascii'))
    _CMD_HEARTBEAT =              bytes.fromhex((b'AA010F0000000004D7000338BA8D0C').decode('ascii'))
    _CMD_DISCONNECT =             bytes.fromhex((b'AA010F0000000004D70006B74EE77C').decode('ascii'))
    _CMD_READ_EXTRINSIC =         bytes.fromhex((b'AA010F0000000004D70102EFBB9162').decode('ascii'))
    _CMD_GET_FAN =                bytes.fromhex((b'AA010F0000000004D701054C2EF5FC').decode('ascii'))
    _CMD_GET_IMU =                bytes.fromhex((b'AA010F0000000004D70109676243F5').decode('ascii'))

    _CMD_RAIN_FOG_ON =            bytes.fromhex((b'AA011000000000B809010301D271D049').decode('ascii'))
    _CMD_RAIN_FOG_OFF =           bytes.fromhex((b'AA011000000000B8090103004441D73E').decode('ascii'))
    _CMD_LIDAR_START =            bytes.fromhex((b'AA011000000000B8090100011122FD62').decode('ascii'))
    _CMD_LIDAR_POWERSAVE =        bytes.fromhex((b'AA011000000000B809010002AB73F4FB').decode('ascii'))
    _CMD_LIDAR_STANDBY =          bytes.fromhex((b'AA011000000000B8090100033D43F38C').decode('ascii'))
    _CMD_DATA_STOP =              bytes.fromhex((b'AA011000000000B809000400B4BD5470').decode('ascii'))
    _CMD_DATA_START =             bytes.fromhex((b'AA011000000000B809000401228D5307').decode('ascii'))
    _CMD_CARTESIAN_CS =           bytes.fromhex((b'AA011000000000B809000500F58C4F69').decode('ascii'))
    _CMD_SPHERICAL_CS =           bytes.fromhex((b'AA011000000000B80900050163BC481E').decode('ascii'))
    _CMD_FAN_ON =                 bytes.fromhex((b'AA011000000000B80901040115E79106').decode('ascii'))
    _CMD_FAN_OFF =                bytes.fromhex((b'AA011000000000B80901040083D79671').decode('ascii'))
    _CMD_LIDAR_SINGLE_1ST =       bytes.fromhex((b'AA011000000000B80901060001B5A043').decode('ascii'))
    _CMD_LIDAR_SINGLE_STRONGEST = bytes.fromhex((b'AA011000000000B8090106019785A734').decode('ascii'))
    _CMD_LIDAR_DUAL =             bytes.fromhex((b'AA011000000000B8090106022DD4AEAD').decode('ascii'))
    _CMD_IMU_DATA_ON =            bytes.fromhex((b'AA011000000000B80901080119A824AA').decode('ascii'))
    _CMD_IMU_DATA_OFF =           bytes.fromhex((b'AA011000000000B8090108008F9823DD').decode('ascii'))

    _CMD_REBOOT =                 bytes.fromhex((b'AA011100000000FC02000A000004477736').decode('ascii'))

    _CMD_DYNAMIC_IP =             bytes.fromhex((b'AA011400000000A8240008000000000068F8DD50').decode('ascii'))
    _CMD_WRITE_ZERO_EO =          bytes.fromhex((b'AA012700000000B5ED01010000000000000000000000000000000000000000000000004CDEA4E7').decode('ascii'))
    
    # [HAP] Mid360 High-Accuracy Protocol commands
    # Port usage: 56000 for discovery, 56100 for commands, 56300 for point cloud data
    # Command IDs are different from standard protocol
    _HAP_PORT_DISCOVERY = 56000
    _HAP_PORT_COMMAND = 56100
    _HAP_PORT_DATA = 56300
    
    # Common template for building HAP commands
    def _build_hap_command(self, cmd_id, cmd_type, data=b''):
        # HAP command format: sof(1) + version(1) + length(2) + seq_num(4) + cmd_id(2) + cmd_type(1) + sender_type(1) + resv(6) + crc16(2) + crc32(4) + data
        sof = b'\xAA'            # Start of frame
        version = b'\x00'        # Protocol version 0
        data_len = len(data)
        length = struct.pack('<H', 24 + data_len)  # 24 bytes header + data
        seq_num = struct.pack('<I', self._seq_num)  # Sequence number
        self._seq_num = (self._seq_num + 1) & 0xFFFFFFFF  # Increment and wrap
        cmd_id_bytes = struct.pack('<H', cmd_id)
        cmd_type_byte = struct.pack('B', cmd_type)   # 0x00: REQ, 0x01: ACK
        sender_type = b'\x00'    # 0x00: Host computer
        resv = b'\x00' * 6       # 6 bytes reserved
        
        # Calculate CRC16 for header
        header = sof + version + length + seq_num + cmd_id_bytes + cmd_type_byte + sender_type + resv
        crc16 = struct.pack('<H', self._crc16(header))
        
        # Calculate CRC32 for entire frame
        frame = header + crc16 + data
        crc32 = struct.pack('<I', self._crc32(frame))
        
        # Combine everything
        command = frame + crc32
        return command

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
        # [HAP] Added sequence number counter for Mid-360 protocol commands
        self._seq_num = 0
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
        # [HAP] Updated to handle both standard protocol and HAP (High-Accuracy Protocol) for Mid360
        # HAP uses port 56000 for discovery instead of 55000
        
        # Try standard protocol first (port 55000)
        serverSock_INIT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock_INIT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSock_INIT.bind(("0.0.0.0", 55000))

        # [HAP] Create socket for HAP protocol
        serverSock_HAP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock_HAP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            serverSock_HAP.bind(("0.0.0.0", self._HAP_PORT_DISCOVERY))
        except:
            if self._showMessages:
                print("   [HAP] Warning: Unable to bind to port 56000 for Mid360 HAP protocol")
            serverSock_HAP = None
            
        # Broadcast discovery command for both protocols
        discoveryCmd = self._build_hap_command(0x0000, 0)  # [HAP] cmd_id 0x0000 is discovery
        broadcastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcastSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # [HAP] Send discovery broadcast on HAP port
        if serverSock_HAP:
            broadcastSock.sendto(discoveryCmd, ("255.255.255.255", self._HAP_PORT_DISCOVERY))
        
        # Also send standard protocol discovery command
        broadcastSock.sendto(self._CMD_QUERY, ("255.255.255.255", 65000))
        
        foundDevice = select.select([serverSock_INIT], [], [], 0.5)[0]
        
        # [HAP] Check for HAP responses
        foundHapDevice = []
        if serverSock_HAP:
            foundHapDevice = select.select([serverSock_HAP], [], [], 0.5)[0]

        IPs = []
        Serials = []
        ipRangeCodes = []
        sensorTypes = []

        # Process standard protocol responses
        if foundDevice:
            readData = True
            while readData:
                try:
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
                except socket.timeout:
                    readData = False
                except:
                    readData = False

        # [HAP] Process HAP protocol responses
        if foundHapDevice:
            readData = True
            while readData:
                try:
                    binData, addr = serverSock_HAP.recvfrom(60)  # HAP responses might be longer
                    
                    if len(addr) == 2:
                        if addr[1] == self._HAP_PORT_DISCOVERY:
                            # Parse HAP discovery response
                            if len(binData) >= 28:  # Ensure we have enough data to parse
                                # For HAP response, format is:
                                # ret_code(1) + dev_type(1) + serial_number(16) + lidar_ip(4) + cmd_port(2)
                                ret_code = binData[24]
                                if ret_code == 0:  # Success
                                    dev_type = binData[25]
                                    serial_number = binData[26:42].decode('utf-8').strip('\x00')
                                    ip_parts = [str(int(binData[42+i])) for i in range(4)]
                                    lidar_ip = '.'.join(ip_parts)
                                    
                                    # Check if this IP is already in our list
                                    existsAlready = False
                                    for i in range(0, len(IPs)):
                                        if lidar_ip == IPs[i]:
                                            existsAlready = True
                                            break
                                            
                                    if not existsAlready:
                                        # [HAP] For Mid-360, we mark the sensor type accordingly
                                        sensorTypes.append("Mid-360")
                                        IPs.append(lidar_ip)
                                        Serials.append(serial_number)
                                        # Use 0 as default ipRangeCode for HAP devices
                                        ipRangeCodes.append(0)
                except socket.timeout:
                    readData = False
                except:
                    readData = False

        serverSock_INIT.close()
        if serverSock_HAP:
            serverSock_HAP.close()
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
        self._cmdSocket.sendto(self._CMD_DISCONNECT, (self._sensorIP, 65000))

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
            
    def connect(self, computerIP, sensorIP, dataPort, cmdPort, imuPort, sensor_name_override = ""):

        numFound = 0

        if not self._isConnected:

            self._computerIP = self._checkIP(computerIP)
            self._sensorIP = self._checkIP(sensorIP)
            self._dataPort = self._checkPort(dataPort)
            self._cmdPort = self._checkPort(cmdPort)
            self._imuPort = self._checkPort(imuPort)

            if self._computerIP and self._sensorIP and self._dataPort != -1 and self._cmdPort != -1 and self._imuPort != -1:
                num_spaces = 15 - len(self._sensorIP)
                for i in range(num_spaces):
                    self._format_spaces += " "
                unique_serialNums, unique_sensors, sensor_IPs = self._reinit()
                numFound = len(unique_sensors)
                time.sleep(0.1)

                for i in range(len(sensor_IPs)):
                    if self._sensorIP == sensor_IPs[i][0]:
                        self._deviceType = sensor_IPs[i][1]

                if sensor_name_override:
                    self._deviceType = sensor_name_override

                self._dataPort, self._cmdPort, self._imuPort = self._bindPorts()
                
                # [HAP] Check if we're connecting to a Mid-360 device
                is_mid360 = (self._deviceType == "Mid-360")
                
                connection_successful = False
                
                if is_mid360:
                    # [HAP] Connect using HAP protocol for Mid-360 (port 56100 for commands)
                    if self._showMessages: 
                        print("   " + self._sensorIP + self._format_spaces + "   <--     connecting using HAP protocol (Mid-360)")
                    
                    # Create parameter configuration data for HAP connection
                    # Format key_value list format with key 0x0006 (point cloud data config)
                    pc_data_host_cfg = struct.pack('<BBBBI', 
                        int(IP_parts[0]), int(IP_parts[1]), int(IP_parts[2]), int(IP_parts[3]),  # Host IP
                        self._dataPort)  # Host data port
                    
                    # Combine key + length + value
                    pc_data_config = struct.pack('<HH', 0x0006, len(pc_data_host_cfg)) + pc_data_host_cfg
                    
                    # Build full command with parameter configuration (cmd_id=0x0100)
                    # Format: key_num(2) + rsvd(2) + key_value_list
                    key_num = 1  # We're setting one parameter
                    cmd_data = struct.pack('<HH', key_num, 0) + pc_data_config  # key_num, reserved, key_value_list
                    
                    # Create the command packet
                    connect_request = self._build_hap_command(0x0100, 0, cmd_data)  # cmd_id 0x0100 is Parameter Configuration
                    
                    # Send the connection request
                    self._cmdSocket.sendto(connect_request, (self._sensorIP, self._HAP_PORT_COMMAND))
                    
                    # Check for proper response
                    if select.select([self._cmdSocket], [], [], 1.0)[0]:
                        binData, addr = self._cmdSocket.recvfrom(64)
                        if len(binData) >= 25:  # Ensure minimum response length
                            ret_code = binData[24]  # Return code is first byte of data section
                            if ret_code == 0:  # Success
                                connection_successful = True
                                # Set up heartbeat for HAP
                                heartbeat_cmd = self._build_hap_command(0x0103, 0)  # cmd_id 0x0103 is heartbeat
                                self._heartbeat = _heartbeatThread(1, self._cmdSocket, self._sensorIP, self._HAP_PORT_COMMAND, 
                                                                   heartbeat_cmd, self._showMessages, self._format_spaces)
                                time.sleep(0.15)
                else:
                    # Standard protocol connection
                    IP_parts = self._computerIP.split(".")
                    IPhex = str(hex(int(IP_parts[0]))).replace('0x', '').zfill(2)
                    IPhex += str(hex(int(IP_parts[1]))).replace('0x', '').zfill(2)
                    IPhex += str(hex(int(IP_parts[2]))).replace('0x', '').zfill(2)
                    IPhex += str(hex(int(IP_parts[3]))).replace('0x', '').zfill(2)
                    dataHexAll = str(hex(int(self._dataPort))).replace('0x', '').zfill(4)
                    dataHex = dataHexAll[2:] + dataHexAll[:-2]
                    cmdHexAll = str(hex(int(self._cmdPort))).replace('0x', '').zfill(4)
                    cmdHex = cmdHexAll[2:] + cmdHexAll[:-2]
                    imuHexAll = str(hex(int(self._imuPort))).replace('0x', '').zfill(4)
                    imuHex = imuHexAll[2:] + imuHexAll[:-2]
                    cmdString = "AA011900000000DC580001" + IPhex + dataHex + cmdHex + imuHex
                    binString = bytes(cmdString, encoding='utf-8')
                    crc32checksum = self._crc32fromStr(binString)
                    cmdString += crc32checksum
                    binString = bytes(cmdString, encoding='utf-8')

                    connect_request = bytes.fromhex((binString).decode('ascii'))
                    self._cmdSocket.sendto(connect_request, (self._sensorIP, 65000))

                    # check for proper response from connection request
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(16)
                        _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                        if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "1":
                            ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                            if ret_code == 0:
                                connection_successful = True
                                self._heartbeat = _heartbeatThread(1, self._cmdSocket, self._sensorIP, 65000, 
                                                                   self._CMD_HEARTBEAT, self._showMessages, self._format_spaces)
                                time.sleep(0.15)
                                self._query()
                
                if connection_successful:
                    self._isConnected = True
                    if self._showMessages: 
                        print("Connected to the Livox " + self._deviceType + " at IP: " + self._sensorIP + 
                              " (ID: " + str(self._ipRangeCode) + ")")
                else:
                    if self._showMessages: 
                        print("FAILED to connect to the Livox " + self._deviceType + " at IP: " + self._sensorIP)
            else:
                if self._showMessages: print("Invalid connection parameter(s)")
        else:
            if self._showMessages: print("Already connected to the Livox " + self._deviceType + " at IP: " + self._sensorIP)

        return numFound

    def auto_connect(self, manualComputerIP=""):

        numFound = 0

        if not manualComputerIP:
            self._auto_computerIP()
        else:
            self._computerIP = manualComputerIP

        if self._computerIP:

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

            status_message = ""

            if len(unique_serialNums) > 0:
                if self._showMessages:
                    status_message = "\nUsing computer IP address: " + self._computerIP + "\n\n"
                for i in range(0,len(unique_serialNums)):
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
                    if unique_sensors[i] != "NA":
                        status_message += "   *** Discovered a Livox sensor ***\n"
                        status_message += "           Type: " + unique_sensors[i] + "\n"
                        status_message += "         Serial: " + unique_serialNums[i] + "\n"
                        status_message += "          IP(s): " + IPs_mess + "\n"

            if len(unique_sensors) > 0 and unique_sensors[0] != "NA":
                status_message = status_message[:-1]
                print(status_message)
                if self._showMessages:
                    print("Attempting to auto-connect to the Livox " + unique_sensors[0] + " with S/N: " + unique_serialNums[0])                # [HAP] Check if this is a Mid-360 sensor
                if unique_sensors[0] == "Mid-360":
                    # [HAP] Use different ports for Mid-360
                    # Mid-360 uses HAP protocol with different port numbers
                    self._showMessages = False
                    numFound = self.connect(self._computerIP, lidarSensorIPs[0], self._HAP_PORT_DATA, self._HAP_PORT_COMMAND, 0)
                    self._deviceType = unique_sensors[0]
                    self.resetShowMessages()
                    
                    if self._showMessages: print(
                        "Connected to the Livox " + self._deviceType + " at IP: " + self._sensorIP + " (ID: " + str(self._ipRangeCode) + ")")
                        
                elif unique_sensors[0] == "Mid-100":
                    sensor_IPs = None
                    sensor_IDs = None
                    for i in range(len(IP_groups)):
                        ind_IPs = IP_groups[i].split(',')
                        ind_IDs = ID_groups[i].split(',')
                        for j in range(len(ind_IPs)):
                            if lidarSensorIPs[0] == ind_IPs[j]:
                                sensor_IPs = ind_IPs
                                sensor_IDs = ind_IDs

                    sensorM = openpylivoxv2(self._init_showMessages)
                    sensorR = openpylivoxv2(self._init_showMessages)

                    for i in range(3):
                        if int(sensor_IDs[i]) == 1:
                            self.connect(self._computerIP, sensor_IPs[i], 0, 0, 0, "Mid-100 (L)")
                            for j in range(3):
                                if int(sensor_IDs[j]) == 2:
                                    sensorM.connect(self._computerIP, sensor_IPs[j], 0, 0, 0, "Mid-100 (M)")
                                    self._mid100_sensors.append(sensorM)
                                    for k in range(3):
                                        if int(sensor_IDs[k]) == 3:
                                            numFound = sensorR.connect(self._computerIP, sensor_IPs[k], 0, 0, 0, "Mid-100 (R)")
                                            self._mid100_sensors.append(sensorR)
                                            break
                                    break
                            break
                else:
                    self._showMessages = False
                    numFound = self.connect(self._computerIP, lidarSensorIPs[0], 0, 0, 0)
                    self._deviceType = unique_sensors[0]
                    self.resetShowMessages()

                    if self._showMessages: print(
                        "Connected to the Livox " + self._deviceType + " at IP: " + self._sensorIP + " (ID: " + str(self._ipRangeCode) + ")")

        else:
            if self._showMessages: print("*** ERROR: Failed to auto determine the computer IP address ***")

        return numFound

    def _disconnect(self):

        if self._isConnected:
            self._isConnected = False
            self._isData = False
            if self._captureStream is not None:
                self._captureStream.stop()
                self._captureStream = None
            time.sleep(0.1)
            self._isWriting = False

            try:
                self._disconnectSensor()
                self._heartbeat.stop()
                time.sleep(0.2)
                self._heartbeat = None

                self._dataSocket.close()
                self._cmdSocket.close()
                if self._showMessages: print("Disconnected from the Livox " + self._deviceType + " at IP: " + self._sensorIP)

            except:
                if self._showMessages: print("*** Error trying to disconnect from the Livox " + self._deviceType + " at IP: " + self._sensorIP)
        else:
            if self._showMessages: print("Not connected to the Livox " + self._deviceType + " at IP: " + self._sensorIP)

    def disconnect(self):
        self._disconnect()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._disconnect()

    def _reboot(self):

        if self._isConnected:
            self._isConnected = False
            self._isData = False
            if self._captureStream is not None:
                self._captureStream.stop()
                self._captureStream = None
            time.sleep(0.1)
            self._isWriting = False

            try:
                self._rebootSensor()
                self._heartbeat.stop()
                time.sleep(0.2)
                self._heartbeat = None

                self._dataSocket.close()
                self._cmdSocket.close()
                if self._showMessages: print("Rebooting the Livox " + self._deviceType + " at IP: " + self._sensorIP)

            except:
                if self._showMessages: print("*** Error trying to reboot from the Livox " + self._deviceType + " at IP: " + self._sensorIP)
        else:
            if self._showMessages: print("Not connected to the Livox " + self._deviceType + " at IP: " + self._sensorIP)

    def reboot(self):
        self._reboot()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._reboot()

    def _lidarSpinUp(self):

        if self._isConnected:
            self._waitForIdle()
            
            # Check if this is a Mid-360 device using HAP protocol
            if self._deviceType == "Mid-360":
                # [HAP] For Mid-360, use HAP protocol to start lidar
                cmd_data = struct.pack('<BBI', 0x00, 0x01, 0x00)  # State control, set to SAMPLING mode
                start_command = self._build_hap_command(0x0100, 0, cmd_data)  # cmd_id 0x0100 is Parameter Configuration
                self._cmdSocket.sendto(start_command, (self._sensorIP, self._HAP_PORT_COMMAND))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent lidar spin up request (HAP)")

                # Check for proper response
                if select.select([self._cmdSocket], [], [], 0.1)[0]:
                    binData, addr = self._cmdSocket.recvfrom(64)
                    # Extract the return code from HAP response
                    if len(binData) >= 24 and binData[0] == 0xAA:  # Check for HAP SOF (0xAA)
                        ret_code = binData[20] if len(binData) > 20 else 1  # First byte of data section
                        if ret_code == 0:
                            pass  # Success
                        elif ret_code == 1:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to spin up the lidar")
                        else:
                            if self._showMessages: print(
                                "   " + self._sensorIP + self._format_spaces + "   -->     lidar is spinning up, please wait...")
                    else:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect lidar spin up response")
            else:
                # Original protocol for other Livox devices
                self._cmdSocket.sendto(self._CMD_LIDAR_START, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent lidar spin up request")

                # check for proper response from lidar start request
                if select.select([self._cmdSocket], [], [], 0.1)[0]:
                    binData, addr = self._cmdSocket.recvfrom(16)
                    _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                    if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "0":
                        ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                        # if ret_code == 0:
                            # if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     lidar is ready")
                            # time.sleep(0.1)
                        if ret_code == 1:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to spin up the lidar")
                        elif ret_code == 2:
                            if self._showMessages: print(
                                "   " + self._sensorIP + self._format_spaces + "   -->     lidar is spinning up, please wait...")
                    else:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect lidar spin up response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def lidarSpinUp(self):
        self._lidarSpinUp()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._lidarSpinUp()

        while True:
            time.sleep(0.1)
            states = []
            states.append(self._heartbeat.work_state)

            for i in range(len(self._mid100_sensors)):
                states.append(self._mid100_sensors[i]._heartbeat.work_state)

            stopper = False
            for i in range(len(states)):
                if states[i] == 1:
                    stopper = True
                else:
                    stopper = False

            if stopper:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     lidar is ready")
                for i in range(len(self._mid100_sensors)):
                    if self._mid100_sensors[i]._showMessages: print("   " + self._mid100_sensors[i]._sensorIP + self._mid100_sensors[i]._format_spaces + "   -->     lidar is ready")
                time.sleep(0.1)
                break    
    
    def _lidarSpinDown(self):

        if self._isConnected:
            self._waitForIdle()
            
            # Check if this is a Mid-360 device using HAP protocol
            if self._deviceType == "Mid-360":
                # [HAP] For Mid-360, use HAP protocol to stop lidar
                cmd_data = struct.pack('<BBI', 0x00, 0x02, 0x00)  # State control, set to IDLE mode
                stop_command = self._build_hap_command(0x0100, 0, cmd_data)  # cmd_id 0x0100 is Parameter Configuration
                self._cmdSocket.sendto(stop_command, (self._sensorIP, self._HAP_PORT_COMMAND))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent lidar spin down request (HAP)")

                # Check for proper response
                if select.select([self._cmdSocket], [], [], 0.1)[0]:
                    binData, addr = self._cmdSocket.recvfrom(64)
                    # Extract the return code from HAP response
                    if len(binData) >= 24 and binData[0] == 0xAA:  # Check for HAP SOF (0xAA)
                        ret_code = binData[20] if len(binData) > 20 else 1  # First byte of data section
                        if ret_code == 0:
                            self._isData = False
                            if self._captureStream is not None:
                                self._captureStream.stop()
                                self._captureStream = None
                            self._isWriting = False
                            time.sleep(0.1)
                        elif ret_code == 1:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to spin down the lidar")
                    else:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect lidar spin down response")
            else:
                # Original protocol for other Livox devices
                self._cmdSocket.sendto(self._CMD_LIDAR_POWERSAVE, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent lidar spin down request")

                # check for proper response from lidar stop request
                if select.select([self._cmdSocket], [], [], 0.1)[0]:
                    binData, addr = self._cmdSocket.recvfrom(16)
                    _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                    if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "0":
                        ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                        if ret_code == 1:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to spin down the lidar")
                        else:
                            self._isData = False
                            if self._captureStream is not None:
                                self._captureStream.stop()
                                self._captureStream = None
                            self._isWriting = False
                            time.sleep(0.1)
                    else:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect lidar spin down response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def lidarSpinDown(self):
        self._lidarSpinDown()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._lidarSpinDown()

    def _lidarStandBy(self):

        if self._isConnected:
            self._waitForIdle()
            self._cmdSocket.sendto(self._CMD_LIDAR_STANDBY, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent lidar stand-by request")

            # check for proper response from lidar stand-by request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "0":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set lidar to stand-by")
                    else:
                        self._isData = False
                        if self._captureStream is not None:
                            self._captureStream.stop()
                            self._captureStream = None
                        self._isWriting = False
                        time.sleep(0.1)
                else:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect lidar stand-by response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def lidarStandBy(self):
        self._lidarStandBy()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._lidarStandBy()    
    
    def dataStart(self):

        if self._isConnected:
            if not self._isData:
                self._captureStream = _dataCaptureThread(self._sensorIP, self._dataSocket, "", 0, 0, 0, 0, self._showMessages, self._format_spaces, self._deviceType)
                time.sleep(0.12)
                self._waitForIdle()
                
                # Check if this is a Mid-360 device using HAP protocol
                if self._deviceType == "Mid-360":
                    # [HAP] Start point cloud data for Mid-360
                    # Configure point cloud data output
                    cmd_data = struct.pack('<BBII', 0x0D, 0x01, 0x01, 0x01)  # Enable point cloud data output with default type
                    data_config_cmd = self._build_hap_command(0x0100, 0, cmd_data)
                    self._cmdSocket.sendto(data_config_cmd, (self._sensorIP, self._HAP_PORT_COMMAND))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start data stream request (HAP)")
                    
                    # Check for proper response
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(64)
                        # Extract the return code from HAP response
                        if len(binData) >= 24 and binData[0] == 0xAA:  # Check for HAP SOF (0xAA)
                            ret_code = binData[20] if len(binData) > 20 else 1  # First byte of data section
                            if ret_code == 0:
                                self._isData = True
                            else:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to start data stream")
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                time.sleep(0.1)
                                self._isData = False
                        else:
                            if self._showMessages:
                                print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect start data stream response")
                else:
                    # Original protocol for other Livox devices
                    self._cmdSocket.sendto(self._CMD_DATA_START, (self._sensorIP, 65000))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start data stream request")

                    # check for proper response from data start request
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(16)
                        _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                        if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "4":
                            ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                            if ret_code == 1:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to start data stream")
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                time.sleep(0.1)
                                self._isData = False
                            else:
                                self._isData = True
                        else:
                            if self._showMessages:
                                print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect start data stream response")
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     data stream already started")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)    
    
    def _dataStart_RT(self):

        if self._isConnected:
            if not self._isData:
                self._captureStream = _dataCaptureThread(self._sensorIP, self._dataSocket, "", 1, 0, 0, 0, self._showMessages, self._format_spaces, self._deviceType)
                time.sleep(0.12)
                self._waitForIdle()
                
                # Check if this is a Mid-360 device using HAP protocol
                if self._deviceType == "Mid-360":
                    # [HAP] Start point cloud data for Mid-360 with real-time ASCII output
                    # Configure point cloud data output
                    cmd_data = struct.pack('<BBII', 0x0D, 0x01, 0x01, 0x01)  # Enable point cloud data output
                    data_config_cmd = self._build_hap_command(0x0100, 0, cmd_data)
                    self._cmdSocket.sendto(data_config_cmd, (self._sensorIP, self._HAP_PORT_COMMAND))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start data stream request (HAP)")
                    
                    # Check for proper response
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(64)
                        # Extract the return code from HAP response
                        if len(binData) >= 24 and binData[0] == 0xAA:  # Check for HAP SOF (0xAA)
                            ret_code = binData[20] if len(binData) > 20 else 1  # First byte of data section
                            if ret_code == 0:
                                self._isData = True
                            else:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to start data stream")
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                time.sleep(0.1)
                                self._isData = False
                        else:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect start data stream response")
                else:
                    # Original protocol for other Livox devices
                    self._cmdSocket.sendto(self._CMD_DATA_START, (self._sensorIP, 65000))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start data stream request")

                    # check for proper response from data start request
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(16)
                        _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                        if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "4":
                            ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                            if ret_code == 1:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to start data stream")
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                time.sleep(0.1)
                                self._isData = False
                            else:
                                self._isData = True
                        else:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect start data stream response")
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     data stream already started")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def dataStart_RT(self):
        self._dataStart_RT()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._dataStart_RT()    
    
    def _dataStart_RT_B(self):

        if self._isConnected:
            if not self._isData:
                self._captureStream = _dataCaptureThread(self._sensorIP, self._dataSocket, self._imuSocket, "", 2, 0, 0, 0, self._showMessages, self._format_spaces, self._deviceType)
                time.sleep(0.12)
                self._waitForIdle()
                
                # Check if this is a Mid-360 device using HAP protocol
                if self._deviceType == "Mid-360":
                    # [HAP] Start point cloud data for Mid-360 with real-time binary output
                    # Configure point cloud data output
                    cmd_data = struct.pack('<BBII', 0x0D, 0x01, 0x01, 0x01)  # Enable point cloud data output
                    data_config_cmd = self._build_hap_command(0x0100, 0, cmd_data)
                    self._cmdSocket.sendto(data_config_cmd, (self._sensorIP, self._HAP_PORT_COMMAND))
                    
                    # Enable IMU data if available
                    if self._imuSocket:
                        imu_cmd_data = struct.pack('<BBII', 0x0D, 0x01, 0x02, 0x01)  # Enable IMU data output
                        imu_config_cmd = self._build_hap_command(0x0100, 0, imu_cmd_data)
                        self._cmdSocket.sendto(imu_config_cmd, (self._sensorIP, self._HAP_PORT_COMMAND))
                    
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start data stream request (HAP)")
                    
                    # Check for proper response
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(64)
                        # Extract the return code from HAP response
                        if len(binData) >= 24 and binData[0] == 0xAA:  # Check for HAP SOF (0xAA)
                            ret_code = binData[20] if len(binData) > 20 else 1  # First byte of data section
                            if ret_code == 0:
                                self._isData = True
                            else:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to start data stream")
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                time.sleep(0.1)
                                self._isData = False
                        else:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect start data stream response")
                else:
                    # Original protocol for other Livox devices
                    self._cmdSocket.sendto(self._CMD_DATA_START, (self._sensorIP, 65000))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start data stream request")

                    # check for proper response from data start request
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(16)
                        _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                        if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "4":
                            ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                            if ret_code == 1:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to start data stream")
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                time.sleep(0.1)
                                self._isData = False
                            else:
                                self._isData = True
                        else:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect start data stream response")
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     data stream already started")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def dataStart_RT_B(self):
        self._dataStart_RT_B()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._dataStart_RT_B()    
    
    def _dataStop(self):

        if self._isConnected:
            if self._isData:
                self._waitForIdle()
                
                # Check if this is a Mid-360 device using HAP protocol
                if self._deviceType == "Mid-360":
                    # [HAP] Stop point cloud data for Mid-360
                    # Disable point cloud data output
                    cmd_data = struct.pack('<BBII', 0x0D, 0x00, 0x01, 0x01)  # Disable point cloud data output
                    data_stop_cmd = self._build_hap_command(0x0100, 0, cmd_data)
                    self._cmdSocket.sendto(data_stop_cmd, (self._sensorIP, self._HAP_PORT_COMMAND))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent stop data stream request (HAP)")
                    
                    # Check for proper response
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(64)
                        # Extract the return code from HAP response
                        if len(binData) >= 24 and binData[0] == 0xAA:  # Check for HAP SOF (0xAA)
                            ret_code = binData[20] if len(binData) > 20 else 1  # First byte of data section
                            if ret_code == 0:
                                self._isData = False
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                    self._captureStream = None
                                self._isWriting = False
                                time.sleep(0.1)
                            else:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to stop data stream")
                        else:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect stop data stream response")
                else:
                    # Original protocol for other Livox devices
                    self._cmdSocket.sendto(self._CMD_DATA_STOP, (self._sensorIP, 65000))
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent stop data stream request")

                    # check for proper response from data stop request
                    if select.select([self._cmdSocket], [], [], 0.1)[0]:
                        binData, addr = self._cmdSocket.recvfrom(16)
                        _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                        if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "4":
                            ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                            if ret_code == 1:
                                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to stop data stream")
                            else:
                                self._isData = False
                                if self._captureStream is not None:
                                    self._captureStream.stop()
                                    self._captureStream = None
                                self._isWriting = False
                                time.sleep(0.1)
                        else:
                            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect stop data stream response")
            else:
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     data stream already stopped")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def dataStop(self):
        self._dataStop()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._dataStop()

    def setDynamicIP(self):

        if self._isConnected:
            self._waitForIdle()
            self._cmdSocket.sendto(self._CMD_DYNAMIC_IP, (self._sensorIP, 65000))

            # check for proper response from dynamic IP request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "8":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 0:
                        if self._showMessages: print("Changed IP from " + self._sensorIP + " to dynamic IP (DHCP assigned)")
                        self.disconnect()

                        if self._showMessages: print("\n********** PROGRAM ENDED - MUST REBOOT SENSOR **********\n")
                        sys.exit(4)
                    else:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to change to dynamic IP (DHCP assigned)")
                else:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to change to dynamic IP (DHCP assigned)")

        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setStaticIP(self, ipAddress):

        if self._isConnected:
            ipRange = ""
            if self._ipRangeCode == 1:
                ipRange = "192.168.1.11 to .80"
            elif self._ipRangeCode == 2:
                ipRange = "192.168.1.81 to .150"
            elif self._ipRangeCode == 3:
                ipRange = "192.168.1.151 to .220"
            ipAddress = self._checkIP(ipAddress)
            if ipAddress:
                IP_parts = ipAddress.split(".")
                IPhex1 = str(hex(int(IP_parts[0]))).replace('0x', '').zfill(2)
                IPhex2 = str(hex(int(IP_parts[1]))).replace('0x', '').zfill(2)
                IPhex3 = str(hex(int(IP_parts[2]))).replace('0x', '').zfill(2)
                IPhex4 = str(hex(int(IP_parts[3]))).replace('0x', '').zfill(2)
                formattedIP = IP_parts[0].strip() + "." + IP_parts[1].strip() + "." + IP_parts[2].strip() + "." + \
                              IP_parts[3].strip()
                cmdString = "AA011400000000a824000801" + IPhex1 + IPhex2 + IPhex3 + IPhex4
                binString = bytes(cmdString, encoding='utf-8')
                crc32checksum = self._crc32fromStr(binString)
                cmdString += crc32checksum
                binString = bytes(cmdString, encoding='utf-8')

                staticIP_request = bytes.fromhex((binString).decode('ascii'))
                self._waitForIdle()
                self._cmdSocket.sendto(staticIP_request, (self._sensorIP, 65000))

                # check for proper response from static IP request
                if select.select([self._cmdSocket], [], [], 0.1)[0]:
                    binData, addr = self._cmdSocket.recvfrom(16)
                    _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                    if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "8":
                        ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')

                        if ret_code == 0:
                            if self._showMessages: print("Changed IP from " + self._sensorIP + " to a static IP of " + formattedIP)
                            self.disconnect()

                            if self._showMessages: print("\n********** PROGRAM ENDED - MUST REBOOT SENSOR **********\n")
                            sys.exit(5)
                        else:
                            if self._showMessages: print(
                                "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to change static IP (must be " + ipRange + ")")
                    else:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to change static IP (must be " + ipRange + ")")
            else:
                if self._showMessages: print(
                    "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to change static IP (must be " + ipRange + ")")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def _setCartesianCS(self):

        if self._isConnected:
            self._waitForIdle()
            self._cmdSocket.sendto(self._CMD_CARTESIAN_CS, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent change to Cartesian coordinates request")

            # check for proper response from change coordinate system request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "5":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set Cartesian coordinate output")
                    elif ret_code == 0:
                        self._coordSystem = 0
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect change coordinate system response (Cartesian)")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setCartesianCS(self):
        self._setCartesianCS()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._setCartesianCS()

    def _setSphericalCS(self):

        if self._isConnected:
            self._waitForIdle()
            self._cmdSocket.sendto(self._CMD_SPHERICAL_CS, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent change to Spherical coordinates request")

            # check for proper response from change coordinate system request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "General" and cmd_id == "5":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set Spherical coordinate output")
                    elif ret_code == 0:
                        self._coordSystem = 1
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect change coordinate system response (Spherical)")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setSphericalCS(self):
        self._setSphericalCS()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._setSphericalCS()

    def readExtrinsic(self):

        if self._isConnected:
            self._waitForIdle()
            self._cmdSocket.sendto(self._CMD_READ_EXTRINSIC, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent read extrinsic parameters request")

            # check for proper response from read extrinsics request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(40)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "2":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     FAILED to read extrinsic parameters")
                    elif ret_code == 0:
                        roll = struct.unpack('<f', binData[12:16])[0]
                        pitch = struct.unpack('<f', binData[16:20])[0]
                        yaw = struct.unpack('<f', binData[20:24])[0]
                        x = float(struct.unpack('<i', binData[24:28])[0]) / 1000.
                        y = float(struct.unpack('<i', binData[28:32])[0]) / 1000.
                        z = float(struct.unpack('<i', binData[32:36])[0]) / 1000.

                        self._x = x
                        self._y = y
                        self._z = z
                        self._roll = roll
                        self._pitch = pitch
                        self._yaw = yaw

                        # called only to print the extrinsic parameters to the screen if .showMessages(True)
                        ack = self.extrinsicParameters()
                else:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     incorrect read extrinsics response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setExtrinsicToZero(self):

        if self._isConnected:
            self._waitForIdle()
            self._cmdSocket.sendto(self._CMD_WRITE_ZERO_EO, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent set extrinsic parameters to zero request")

            # check for proper response from write extrinsics request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "1":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set extrinsic parameters to zero")
                    elif ret_code == 0:
                        self.readExtrinsic()
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect set extrinsics to zero response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setExtrinsicTo(self, x, y, z, roll, pitch, yaw):

        if self._isConnected:
            goodValues = True
            try:
                xi = int(np.floor(x * 1000.))  # units of millimeters
                yi = int(np.floor(y * 1000.))  # units of millimeters
                zi = int(np.floor(z * 1000.))  # units of millimeters
                rollf = float(roll)
                pitchf = float(pitch)
                yawf = float(yaw)

            except:
                goodValues = False
                if self._showMessages: print(
                    "*** Error - one or more of the extrinsic values specified are not of the correct type ***")

            if goodValues:
                h_x = str(binascii.hexlify(struct.pack('<i', xi)))[2:-1]
                h_y = str(binascii.hexlify(struct.pack('<i', yi)))[2:-1]
                h_z = str(binascii.hexlify(struct.pack('<i', zi)))[2:-1]
                h_roll = str(binascii.hexlify(struct.pack('<f', rollf)))[2:-1]
                h_pitch = str(binascii.hexlify(struct.pack('<f', pitchf)))[2:-1]
                h_yaw = str(binascii.hexlify(struct.pack('<f', yawf)))[2:-1]

                cmdString = "AA012700000000b5ed0101" + h_roll + h_pitch + h_yaw + h_x + h_y + h_z
                binString = bytes(cmdString, encoding='utf-8')
                crc32checksum = self._crc32fromStr(binString)
                cmdString += crc32checksum
                binString = bytes(cmdString, encoding='utf-8')
                setExtValues = bytes.fromhex((binString).decode('ascii'))

                self._waitForIdle()
                self._cmdSocket.sendto(setExtValues, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent set extrinsic parameters request")

                # check for proper response from write extrinsics request
                if select.select([self._cmdSocket], [], [], 0.1)[0]:
                    binData, addr = self._cmdSocket.recvfrom(16)
                    _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                    if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "1":
                        ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                        if ret_code == 1:
                            if self._showMessages: print(
                                "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set extrinsic parameters")
                        elif ret_code == 0:
                            self.readExtrinsic()
                    else:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     incorrect set extrinsic parameters response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def _updateUTC(self, year, month, day, hour, microsec):

        if self._isConnected:

            yeari = int(year) - 2000
            if yeari < 0 or yeari > 255:
                yeari = 0

            monthi = int(month)
            if monthi < 1 or monthi > 12:
                monthi = 1

            dayi = int(day)
            if dayi < 1 or dayi > 31:
                dayi = 1

            houri = int(hour)
            if houri < 0 or houri > 23:
                houri = 0

            seci = int(microsec)
            if seci < 0 or seci > int(60 * 60 * 1000000):
                seci = 0

            year_b = str(binascii.hexlify(struct.pack('<B', yeari)))[2:-1]
            month_b = str(binascii.hexlify(struct.pack('<B', monthi)))[2:-1]
            day_b = str(binascii.hexlify(struct.pack('<B', dayi)))[2:-1]
            hour_b = str(binascii.hexlify(struct.pack('<B', houri)))[2:-1]
            sec_b = str(binascii.hexlify(struct.pack('<I', seci)))[2:-1]

            # test case Sept 10, 2020 at 17:15 UTC  -->  AA0117000000006439010A14090A1100E9A435D0337994
            cmdString = "AA0117000000006439010A" + year_b + month_b + day_b + hour_b + sec_b
            binString = bytes(cmdString, encoding='utf-8')
            crc32checksum = self._crc32fromStr(binString)
            cmdString += crc32checksum
            binString = bytes(cmdString, encoding='utf-8')
            setUTCValues = bytes.fromhex((binString).decode('ascii'))

            self._waitForIdle()
            self._cmdSocket.sendto(setUTCValues, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent update UTC request")

            # check for proper response from update UTC request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "10":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to update UTC values")
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect update UTC values response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def updateUTC(self, year, month, day, hour, microsec):
        self._updateUTC(year, month, day, hour, microsec)
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._updateUTC(year, month, day, hour, microsec)

    def _setRainFogSuppression(self, OnOff):

        if self._isConnected:
            self._waitForIdle()
            if OnOff:
                self._cmdSocket.sendto(self._CMD_RAIN_FOG_ON, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent turn on rain/fog suppression request")
            else:
                self._cmdSocket.sendto(self._CMD_RAIN_FOG_OFF, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent turn off rain/fog suppression request")

            # check for proper response from change rain/fog suppression request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "3":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set rain/fog suppression value")
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect set rain/fog suppression response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setRainFogSuppression(self, OnOff):
        self._setRainFogSuppression(OnOff)
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._setRainFogSuppression(OnOff)

    def _setFan(self, OnOff):

        if self._isConnected:
            self._waitForIdle()
            if OnOff:
                self._cmdSocket.sendto(self._CMD_FAN_ON, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent turn on fan request")
            else:
                self._cmdSocket.sendto(self._CMD_FAN_OFF, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent turn off fan request")

            # check for proper response from change fan request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "4":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set fan value")
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect set fan response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setFan(self, OnOff):
        self._setFan(OnOff)
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._setFan(OnOff)

    def _getFan(self):

        if self._isConnected:
            self._waitForIdle()

            self._cmdSocket.sendto(self._CMD_GET_FAN, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent get fan state request")

            # check for proper response from get fan request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(17)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "5":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to get fan state value")
                    elif ret_code == 0:
                        value = struct.unpack('<B', binData[12:13])[0]
                        print("   " + self._sensorIP + self._format_spaces + "   -->     fan state: " + str(value))
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect get fan state response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def getFan(self):
        self._getFan()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._getFan()

    def setLidarReturnMode(self, Mode_ID):

        if self._isConnected:
            self._waitForIdle()
            # single first return
            if Mode_ID == 0:
                self._cmdSocket.sendto(self._CMD_LIDAR_SINGLE_1ST, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent single first return lidar mode request")
            # single strongest return
            elif Mode_ID == 1:
                self._cmdSocket.sendto(self._CMD_LIDAR_SINGLE_STRONGEST, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent single strongest return lidar mode request")
            # dual returns
            elif Mode_ID == 2:
                self._cmdSocket.sendto(self._CMD_LIDAR_DUAL, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent dual return lidar mode request")

            # check for proper response from change lidar mode request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "6":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set lidar mode value")
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect set lidar mode response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def setIMUdataPush(self, OnOff):

        if self._isConnected:
            self._waitForIdle()

            if OnOff:
                self._cmdSocket.sendto(self._CMD_IMU_DATA_ON, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent start IMU data push request")
            else:
                self._cmdSocket.sendto(self._CMD_IMU_DATA_OFF, (self._sensorIP, 65000))
                if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent stop IMU data push request")

            # check for proper response from start/start IMU data push request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(16)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "8":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to set IMU data push value")
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect set IMU data push response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)

    def getIMUdataPush(self):

        if self._isConnected:
            self._waitForIdle()

            self._cmdSocket.sendto(self._CMD_GET_IMU, (self._sensorIP, 65000))
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   <--     sent get IMU push state request")

            # check for proper response from get IMU request
            if select.select([self._cmdSocket], [], [], 0.1)[0]:
                binData, addr = self._cmdSocket.recvfrom(17)
                _, ack, cmd_set, cmd_id, ret_code_bin = self._parseResp(binData)

                if ack == "ACK (response)" and cmd_set == "Lidar" and cmd_id == "9":
                    ret_code = int.from_bytes(ret_code_bin[0], byteorder='little')
                    if ret_code == 1:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     FAILED to get IMU push state value")
                    elif ret_code == 0:
                        value = struct.unpack('<B', binData[12:13])[0]
                        print("   " + self._sensorIP + self._format_spaces + "   -->     IMU push state: " + str(value))
                else:
                    if self._showMessages: print(
                        "   " + self._sensorIP + self._format_spaces + "   -->     incorrect get IMU push state response")
        else:
            if self._showMessages: print("Not connected to Livox sensor at IP: " + self._sensorIP)


    def saveDataToCSV(self, filePathAndName, secsToWait, duration):

        if self._isConnected:
            if self._isData:
                if self._firmware != "UNKNOWN":
                    try:
                        firmwareType = self._SPECIAL_FIRMWARE_TYPE_DICT[self._firmware]
                    except:
                        firmwareType = 1

                    if duration < 0:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, negative duration")
                    else:
                        # max duration = 4 years - 1 sec
                        if duration >= 126230400:
                            if self._showMessages: print(
                                "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, duration too big")
                        else:

                            if secsToWait < 0:
                                if self._showMessages: print(
                                    "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, negative time to wait")
                            else:
                                # max time to wait = 15 mins
                                if secsToWait > 900:
                                    if self._showMessages: print(
                                        "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, time to wait too big")
                                else:

                                    if filePathAndName == "":
                                        if self._showMessages: print(
                                            "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, file path and name missing")
                                    else:

                                        if filePathAndName[-4:].upper() != ".CSV":
                                            filePathAndName += ".csv"

                                        self._isWriting = True
                                        self._captureStream.filePathAndName = filePathAndName
                                        self._captureStream.secsToWait = secsToWait
                                        self._captureStream.duration = duration
                                        self._captureStream.firmwareType = firmwareType
                                        self._captureStream._showMessages = self._showMessages
                                        time.sleep(0.1)
                                        self._captureStream.isCapturing = True
                else:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     unknown firmware version")
            else:
                if self._showMessages: print(
                    "   " + self._sensorIP + self._format_spaces + "   -->     WARNING: data stream not started, no CSV file created")

    def closeCSV(self):
        if self._isConnected:
            if self._isWriting:
                if self._captureStream is not None:
                    self._captureStream.stop()
                self._isWriting = False

    def _saveDataToFile(self, filePathAndName, secsToWait, duration):

        if self._isConnected:
            if self._isData:
                if self._firmware != "UNKNOWN":
                    try:
                        firmwareType = self._SPECIAL_FIRMWARE_TYPE_DICT[self._firmware]
                    except:
                        firmwareType = 1

                    if duration < 0:
                        if self._showMessages: print(
                            "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, negative duration")
                    else:
                        # max duration = 4 years - 1 sec
                        if duration >= 126230400:
                            if self._showMessages: print(
                                "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, duration too big")
                        else:

                            if secsToWait < 0:
                                if self._showMessages: print(
                                    "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, negative time to wait")
                            else:
                                # max time to wait = 15 mins
                                if secsToWait > 900:
                                    if self._showMessages: print(
                                        "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, time to wait too big")
                                else:

                                    if filePathAndName == "":
                                        if self._showMessages: print(
                                            "   " + self._sensorIP + self._format_spaces + "   -->     * ISSUE: saving data, file path and name missing")
                                    else:

                                        self._isWriting = True
                                        self._captureStream.filePathAndName = filePathAndName
                                        self._captureStream.secsToWait = secsToWait
                                        self._captureStream.duration = duration
                                        self._captureStream.firmwareType = firmwareType
                                        self._captureStream._showMessages = self._showMessages
                                        time.sleep(0.1)
                                        self._captureStream.isCapturing = True
                else:
                    if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     unknown firmware version")
            else:
                if self._showMessages: print(
                    "   " + self._sensorIP + self._format_spaces + "   -->     WARNING: data stream not started, no data file created")

    def saveDataToFile(self, filePathAndName, secsToWait, duration):
        path_file = Path(filePathAndName)
        filename = path_file.stem
        exten = path_file.suffix
        self._saveDataToFile(filePathAndName, secsToWait, duration)
        for i in range(len(self._mid100_sensors)):
            new_file = ""
            if i == 0:
                new_file = filename + "_M" + exten
            elif i == 1:
                new_file = filename + "_R" + exten

            self._mid100_sensors[i]._saveDataToFile(new_file, secsToWait, duration)

    def _closeFile(self):
        if self._isConnected:
            if self._isWriting:
                if self._captureStream is not None:
                    self._captureStream.stop()
                self._isWriting = False

    def closeFile(self):
        self._closeFile()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._closeFile()

    def _resetShowMessages(self):
        self._showMessages = self._init_showMessages

    def resetShowMessages(self):
        self._resetShowMessages()
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._resetShowMessages()

    def _connectionParameters(self):
        if self._isConnected:
            return [self._computerIP, self._sensorIP, str(self._dataPort), str(self._cmdPort), str(self._imuPort)]

    def connectionParameters(self):
        sensorIPs = []
        dataPorts = []
        cmdPorts = []
        imuPorts = []

        params = self._connectionParameters()
        sensorIPs.append(params[1])
        dataPorts.append(params[2])
        cmdPorts.append(params[3])
        imuPorts.append(params[4])

        for i in range(len(self._mid100_sensors)):
            params = self._mid100_sensors[i]._connectionParameters()
            sensorIPs.append(params[1])
            dataPorts.append(params[2])
            cmdPorts.append(params[3])
            imuPorts.append(params[4])

        if self._showMessages:
            print("      Computer IP Address:    " + params[0])
            print("      Sensor IP Address(es):  " + str(sensorIPs))
            print("      Data Port Number(s):    " + str(dataPorts))
            print("      Command Port Number(s): " + str(cmdPorts))
            if self._deviceType == "Horizon" or self._deviceType == "Tele-15":
                print("      IMU Port Number(s):     " + str(imuPorts))

        return [params[0], sensorIPs, dataPorts, cmdPorts, imuPorts]

    def extrinsicParameters(self):
        if self._isConnected:
            if self._showMessages:
                print("      x: " + str(self._x) + " m")
                print("      y: " + str(self._y) + " m")
                print("      z: " + str(self._z) + " m")
                print("      roll: " + "{0:.2f}".format(self._roll) + " deg")
                print("      pitch: " + "{0:.2f}".format(self._pitch) + " deg")
                print("      yaw: " + "{0:.2f}".format(self._yaw) + " deg")

            return [self._x, self._y, self._z, self._roll, self._pitch, self._yaw]

    def firmware(self):
        if self._isConnected:
            if self._showMessages:
                print("   " + self._sensorIP + self._format_spaces + "   -->     F/W Version: " + self._firmware)
                for i in range(len(self._mid100_sensors)):
                    print("   " + self._mid100_sensors[i]._sensorIP + self._mid100_sensors[i]._format_spaces + "   -->     F/W Version: " + self._mid100_sensors[i]._firmware)

            return self._firmware

    def serialNumber(self):
        if self._isConnected:
            if self._showMessages: print("   " + self._sensorIP + self._format_spaces + "   -->     Serial # " + self._serial)

            return self._serial

    def showMessages(self, new_value):
        self._showMessages = bool(new_value)
        for i in range(len(self._mid100_sensors)):
            self._mid100_sensors[i]._showMessages = bool(new_value)

    def lidarStatusCodes(self):
        if self._isConnected:
            if self._captureStream is not None:
                codes = self._captureStream.statusCodes()
                if self._showMessages:
                    sys_mess = "UNKNOWN"
                    if codes[0] == 0:
                        sys_mess = "OK"
                    elif codes[0] == 1:
                        sys_mess = "* WARNING *"
                    elif codes[0] == 2:
                        sys_mess = "*** ERROR ***"

                    temp_mess = "UNKNOWN"
                    if codes[1] == 0:
                        temp_mess = "OK"
                    elif codes[1] == 1:
                        temp_mess = "High/Low Warning"
                    elif codes[1] == 2:
                        temp_mess = "Extremely High/Low Error"

                    volt_mess = "UNKNOWN"
                    if codes[2] == 0:
                        volt_mess = "OK"
                    elif codes[2] == 1:
                        volt_mess = "High Warning"
                    elif codes[2] == 2:
                        volt_mess = "Extremely High Error"

                    motor_mess = "UNKNOWN"
                    if codes[3] == 0:
                        motor_mess = "OK"
                    elif codes[3] == 1:
                        motor_mess = "Warning State"
                    elif codes[3] == 2:
                        motor_mess = "Error State"

                    dirty_mess = "UNKNOWN"
                    if codes[4] == 0:
                        dirty_mess = "OK"
                    elif codes[4] == 1:
                        dirty_mess = "Dirty/Blocked Warning"

                    firmware_mess = "UNKNOWN"
                    if codes[5] == 0:
                        firmware_mess = "OK"
                    elif codes[5] == 1:
                        firmware_mess = "Abnormal Error"

                    pps_mess = "UNKNOWN"
                    if codes[6] == 0:
                        pps_mess = "OK, but not detected"
                    elif codes[6] == 1:
                        pps_mess = "OK"

                    device_mess = "UNKNOWN"
                    if codes[7] == 0:
                        device_mess = "OK"
                    elif codes[7] == 1:
                        device_mess = "Approaching End of Service Life Warning"

                    fan_mess = "UNKNOWN"
                    if codes[8] == 0:
                        fan_mess = "OK"
                    elif codes[8] == 1:
                        fan_mess = "Fan Warning"

                    heating_mess = "UNKNOWN"
                    if codes[9] == 0:
                        heating_mess = "Low Temp. Heating ON"
                    elif codes[9] == 1:
                        heating_mess = "Low Temp. Heating OFF"

                    ptp_mess = "UNKNOWN"
                    if codes[10] == 0:
                        ptp_mess = "No 1588 Signal"
                    elif codes[10] == 1:
                        ptp_mess = "1588 Signal OK"

                    time_sync_mess = "UNKNOWN"
                    if codes[11] == 0:
                        time_sync_mess = "Internal clock sync."
                    elif codes[11] == 1:
                        time_sync_mess = "PTP 1588 sync."
                    elif codes[11] == 2:
                        time_sync_mess = "GPS sync."
                    elif codes[11] == 3:
                        time_sync_mess = "PPS sync."
                    elif codes[11] == 4:
                        time_sync_mess = "Abnormal time sync."

                    print("      System Status:         " + sys_mess)
                    print("      Temperature Status:    " + temp_mess)
                    print("      Voltage Status:        " + volt_mess)
                    print("      Motor Status:          " + motor_mess)
                    print("      Clean Status:          " + dirty_mess)
                    print("      Firmware Status:       " + firmware_mess)
                    print("      PPS Status:            " + pps_mess)
                    print("      Device Status:         " + device_mess)
                    print("      Fan Status:            " + fan_mess)
                    print("      Self Heating Status:   " + heating_mess)
                    print("      PTP Status:            " + ptp_mess)
                    print("      Time Sync. Status:     " + time_sync_mess)

                return codes

            else:
                if self._showMessages:
                    print("      System Status:         UNKNOWN")
                    print("      Temperature Status:    UNKNOWN")
                    print("      Voltage Status:        UNKNOWN")
                    print("      Motor Status:          UNKNOWN")
                    print("      Dirty Status:          UNKNOWN")
                    print("      Firmware Status:       UNKNOWN")
                    print("      PPS Status:            UNKNOWN")
                    print("      Device Status:         UNKNOWN")
                    print("      Fan Status:            UNKNOWN")
                    print("      Self Heating Status:   UNKNOWN")
                    print("      PTP Status:            UNKNOWN")
                    print("      Time Sync. Status:     UNKNOWN")

                return [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    def _doneCapturing(self):
        # small sleep to ensure this command isn't continuously called if in a while True loop
        time.sleep(0.01)
        if self._captureStream is not None:
            if self._captureStream.duration != 126230400:
                return not (self._captureStream.started)
            else:
                return True
        else:
            return True

    def doneCapturing(self):
        stop = []
        stop.append(self._doneCapturing())
        for i in range(len(self._mid100_sensors)):
            stop.append(self._mid100_sensors[i]._doneCapturing())

        return all(stop)
