'''
Dependency of PINGMapper: https://github.com/CameronBodine/PINGMapper

Repository: https://github.com/CameronBodine/PINGVerter
PyPi: https://pypi.org/project/pingverter/ 

Developed by Cameron S. Bodine

###############
Acknowledgments
###############

None of this work would have been possible without the following repositories:

PyHum: https://github.com/dbuscombe-usgs/PyHum
SL3Reader: https://github.com/halmaia/SL3Reader
sonarlight: https://github.com/KennethTM/sonarlight


MIT License

Copyright (c) 2024 Cameron S. Bodine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os, sys
import numpy as np

# RSD structur
rsdStruct = np.dtype([
    ("test", "<u4"),
])

class gar(object):

    #===========================================================================
    def __init__(self, inFile: str, nchunk: int=0, exportUnknown: bool=False):
        
        '''
        '''

        self.humFile = None
        self.sonFile = inFile
        self.nchunk = nchunk
        self.exportUnknown = exportUnknown

        self.magicNum = 3085556358



        self.extension = os.path.basename(inFile).split('.')[-1]

        self.son_struct = rsdStruct

        self.humDat = {} # Store general sonar recording metadata

        self.son8bit = True

        return
    
    # ======================================================================
    def _getFileLen(self):
        self.file_len = os.path.getsize(self.sonFile)

        return
    
    # ======================================================================
    def _fread_dat(self,
            infile,
            num,
            typ):
        '''
        Helper function that reads binary data in a file.

        ----------------------------
        Required Pre-processing step
        ----------------------------
        Called from self._getHumDat(), self._cntHead(), self._decodeHeadStruct(),
        self._getSonMeta(), self._loadSonChunk()

        ----------
        Parameters
        ----------
        infile : file
            DESCRIPTION - A binary file opened in read mode at a pre-specified
                            location.
        num : int
            DESCRIPTION - Number of bytes to read.
        typ : type
            DESCRIPTION - Byte type

        -------
        Returns
        -------
        List of decoded binary data

        --------------------
        Next Processing Step
        --------------------
        Returns list to function it was called from.
        '''

        buffer = infile.read(num)
        data = np.frombuffer(buffer, dtype=typ)

        return data
    
    
    # ======================================================================
    def _parseFileHeader(self):
        '''
        '''

        self.headBytes = 20480 # Hopefully a fixed value for all RSD files
        chanInfoLen = 1069 # It is not clear there is helful info in channel information...

        # Get the file header structure
        headStruct, firstHeadBytes = self._getFileHeaderStruct()

        print('\n\n\nheadStruct:')
        for v in headStruct:
            print(v)
        
        # Read the header
        file = open(self.sonFile, 'rb') # Open the file
        file.seek(0)

        # Get the data
        buffer = file.read(firstHeadBytes)

        # Read the data
        header = np.frombuffer(buffer=buffer, dtype=headStruct)

        out_dict = {}
        for name, typ in header.dtype.fields.items():
            out_dict[name] = header[name][0].item()

        for k,v in out_dict.items():
            print(k, v)

        self.file_header = out_dict


        return
    
    # ======================================================================
    def _getFileHeaderStruct(self):
        '''

        ffh: field - file header
        ffi: field - file information
        fci: field - channel information
        fcnt: field count
        '''


        # headBytes = 20480
        # firstHeadBytes = 35
        headStruct = [] 

        toCheck = {
            6:[('header_fcnt', '<u1')], #06: number of fields in header structure
            4:[('ffh_0', '<u1'), ('magic_number', '<u4')], #04: field 0 "magic_number", length 4
            10:[('ffh_1', '<u1'), ('format_version', '<u2')], #0a: field 1 "format_version", length 2
            20:[('ffh_2', '<u1'), ('channel_count', '<u4')], #14: field 2 "channel_count", length 4
            25:[('ffh_3', '<u1'), ('max_channel_count', '<u1')], #19: field 3 "max_channel_count", length 1
            47:[('ffh_4', '<u1'), ('ffh_4_actlen', '<u1'), ('ffi_fcnt', '<u1')], #2f: field 4 "file information", length 7; #actual length; #number of "file information" field 
            55: [('ffh_5', '<u1'), ('ffh_5_actlen', '<u2'), ('chan_cnt', '<u1'), ('fci_acnt', '<u1')], #37: "channel information", length 7; 
        }

        fileInfoToCheck = {
            2: [('ffi_0', '<u1'), ('unit_software_version', '<u2')], #02: "file information" field 0
            12: [('ffi_1', '<u1'), ('unit_id_type', '<u4')], #0c: "file information" field 1
            18: [('ffi_2', '<u1'), ('unit_product_number', '<u2')], #12: "file information" field 2    
            28: [('ffi_3', '<u1'), ('date_time_of_recording', '<u4')], #1c: "file information" field 3
        }

        # chanInfoToCheck = {
        #     3: [('fci_0_data_info', '<u1'), ('fci_0_acnt', '<u1'), ('fci_0_actlen', '<u1'), ('fci_channel_id', '<u1')], #03: Channel data info
        #     15: [('fci_1', '<u1'), ('fci_1_actlen', '<u1'), ('fci_first_chunk_offset', '<u8')], #0f: first chunk offset
        #     23: [('fci_2', '<u1'), ('fci_2_actlen', '<u2'), ('fci_2_acnt', '<u1'), ('fci_2_actlen2', '<u2')], #17 prop_chan_info

        
        # }

        chanDataInfoToCheck = {

        }

        file = open(self.sonFile, 'rb') # Open the file
        lastPos = 0 # Track last position in file

        foundChanInfo = False

        # while lastPos < firstHeadBytes - 1:
        while not foundChanInfo:
            # lastPos = file.tell()
            # print('lastPos:', lastPos)
            byte = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte

            if byte == 47:
                # File Information
                structDict = fileInfoToCheck

                for v in toCheck[byte]:
                    headStruct.append(v)

                length = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte
                field_cnt = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte

                fidx = 0
                while fidx < field_cnt:
                    byte = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte
                    if byte in structDict:
                        elen = 0
                        for v in structDict[byte]:

                            headStruct.append(v)
                            
                            # Get length of element
                            elen += (np.dtype(v[-1]).itemsize)

                        # Move forward elen amount
                        cpos = file.tell()
                        npos = cpos + elen - 1

                        file.seek(npos)
                        fidx += 1
                    else:
                        print('{} not in sonar header. Terminating.'.format(byte))
                        print('Offset: {}'.format(file.tell()))
                        sys.exit()

                # lastPos = headBytes
            
            # elif byte == 55:
            #     # File Information

            #     for v in toCheck[byte]:
            #         headStruct.append(v)

            #     length = self._fread_dat(file, 2, '<u2')[0] # Decode the spacer byte
            #     chan_cnt = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte
            #     field_cnt_0 = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte

            #     chanidx = 0
            #     fidx_0 = 0

            #     # Iterate each channel
            #     while chanidx < chan_cnt:
            #         # Iterate each field
            #         while fidx_0 < field_cnt_0:
            #             byte = self._fread_dat(file, 1, 'B')[0] # Decode the spacer byte

            #             if byte in chanInfoToCheck:
            #                 for v in chanInfoToCheck[byte]:
            #                     # Add chanidx to field name
            #                     field_name = '{}_{}'.format(v[0], chanidx)
            #                     v = (field_name, v[1])

            #                     headStruct.append(v)

            #             fidx_0 += 1

            #         chanidx += 1
                
            #     lastPos = headBytes

            elif byte == 55:
                foundChanInfo = True                            

            else:
                if byte in toCheck:
                    elen = 0
                    for v in toCheck[byte]:
                        headStruct.append(v)

                        # Get length of element
                        elen += (np.dtype(v[-1]).itemsize)
                    
                    # Move forward elen amount
                    cpos = file.tell()
                    npos = cpos + elen - 1

                    file.seek(npos)

            lastPos = file.tell()
            print('lastPos:', lastPos)        

        return headStruct, lastPos-1
    
    # ======================================================================
    def _parsePingHeader(self,):
        '''
        '''

        self.son_struct = self._getPingHeaderStruct()


        return
    
    # ======================================================================
    def _getPingHeaderStruct(self, ):
        '''
        fpf: field - ping field
        fps: field - ping state
        '''

        headBytes = self.headBytes # Header length

        headStruct = [] 

        pingHeaderToCheck = {
            6:[('header_fcnt', '<u1')], #06: number of fields in header structure
            4:[('fpf_0', '<u1'), ('magic_number', '<u4')], #04: field 0 "magic_number", length 4
            15:[('fpf_1', '<u1'), ('fpf_1_len', '<u1'), ('fpf_1_fcnt', '<u1'),
                ('fps_0', '<u1'), ('state', '<u1'),
                ('fps_1', '<u1'), ('data_info', '<u1'), ('data_info_cnt', '<u1'), ('data_info_len', '<u1'), ('channel_id', '<u1')], #0f: state data structure
            20:[('SP14', '<u1'), ('sequence_cnt', '<u4')], #14: sequence_count
            28:[('SP1c', '<u1'), ('data_crc', '<u4')], #1c: data crc
            34:[('SP22', '<u1'), ('data_size', '<u4')], #22: data size
            44:[('SP2c', '<u1'), ('recording_time_ms', '<u4')], #2c recording time offset
        }

        pingBodyHeaderToCheck = {
            -1:[('record_body_fcnt', '<u1')],
            1:[('SP1', '<u1'), ('channel_id', '<u1')], #01 channe_id
            11:[('SP0b', '<u1'), ('bottom_depth', '<u3')], #0b bottom depth
            19:[('SP13', '<u1'), ('drawn_bottom_depth', '<u3')], #13 drawn bottom depth
            25:[('SP19', '<u1'), ('first_sample_depth', '<u1')], #19 first sample depth
            35:[('SP23', '<u1'), ('last_sample_depth', '<u1')], #23 last sample depth
            41:[('SP29', '<u1'), ('gain', '<u1')], #29 gain
            49:[('SP31', '<u1'), ('sample_status', '<u1')], #31 sample status
            60:[('SP3c', '<u1'), ('sample_cnt', '<u4')], #3c sample count
            65:[('SP41', '<u1'), ('shade_avail', '<u1')], #41 shade available
            76:[('SP4c', '<u1'), ('scposn_lat', '<u4')], #4c latitude
            84:[('SP54', '<u1'), ('scposn_lon', '<u4')], #54 longitude
            92:[('SP5c', '<u1'), ('water_temp', '<f4')], #5c temperature
            97:[('SP61', '<u1'), ('beam', '<u1')], #61 beam
        }

        # magic number 86 DA E9 B7 == 3085556358

    # ======================================================================
    def __str__(self):
        '''
        Generic print function to print contents of sonObj.
        '''
        output = "Lowrance Class Contents"
        output += '\n\t'
        output += self.__repr__()
        temp = vars(self)
        for item in temp:
            output += '\n\t'
            output += "{} : {}".format(item, temp[item])
        return output