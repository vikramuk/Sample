#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright (c) 2007 Brandon Sterne
# Licensed under the MIT license.
# http://brandon.sternefamily.net/files/mit-license.txt
# Python AES implementation

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


import sys, hashlib, string, getpass
from copy import copy
from random import randint
import time
from operator import itemgetter


# The actual Rijndael specification includes variable block size, but
# AES uses a fixed block size of 16 bytes (128 bits)

# Additionally, AES allows for a variable key size, though this implementation
# of AES uses only 256-bit cipher keys (AES-256)

sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]

sboxInv = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]

rcon = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb
        ]

# create a key from a user-supplied password using SHA-256
def passwordToKey(password):
    sha256 = hashlib.sha256()
    sha256.update(password)
    key = []
    for c in list(sha256.digest()):
        key.append(ord(c))
    return key



def row_shift(l,r):
	
	for loop in range(0,r):
        	first_element = l[0]
        	l.pop(0)
        	l.append(first_element)
	return l

# aesEncrypt - encrypt a single block of plaintext
def aesEncrypt(plaintext, key):
	aes_key = keyexpansion(key)
	key = aes_key
	block = copy(plaintext)
	key_bits = key[:16]
	temp_xor = []
	#print "Plain Text", block
	#print "Key:", key_bits
	#print "Block:", block 

	for xor_plaintext_key in range(0,16):
		
		temp_xor_variable = block[xor_plaintext_key] ^ key_bits[xor_plaintext_key]
		temp_xor.append(temp_xor_variable)
	
	block = temp_xor
	#print "XOR SBOX", block
	temp_xor = []
	key_counter = 16
	key_upto = key_counter + 16

	for round in range(0,14):
		key_bits = []
		key_bits = key[key_counter:key_upto]

		for element in block:
			
			element = hex(element)		
			element = element.replace('0x','')
			try:
				leftmost = element[0]
			except Exception as error:
				leftmost = 0
			try:
				rightmost = element[1]
			except Exception as error:
				rightmost = 0
		
			if leftmost == 0:
				matrix_element = (16 * int(leftmost)) + int(rightmost, 16)
			elif rightmost == 0:
				 matrix_element = (16 * int(leftmost, 16)) + int(rightmost)
			else:
				matrix_element = (16 * int(leftmost, 16)) + int(rightmost, 16)
	
			#print leftmost, rightmost
			#print hex(sbox[matrix_element])
			temp_xor.append(sbox[matrix_element])	

		block = temp_xor
		temp_xor = []

		#print block
		#print leftmost
		#print rightmost
		
		print block

		first_row = [0,4,8,12]
		first_row = itemgetter(*first_row)(block)

		second_row = [1,5,9,13]
                second_row = itemgetter(*second_row)(block)
		third_row = [2,6,10,14]
                third_row = itemgetter(*third_row)(block)
		fourth_row = [3,7,11,15]
                fourth_row = itemgetter(*fourth_row)(block)

		first_row =  list(first_row)
		second_row = list(second_row)
		third_row =  list(third_row)
		fourth_row = list(fourth_row)
		
		first_row = row_shift(first_row,0)		
		second_row = row_shift(second_row,1)
		third_row = row_shift(third_row,2)
		fourth_row = row_shift(fourth_row,3)

		#print first_row
		#print second_row
		#print third_row
		#print fourth_row

#################################################################################
#GF Function(MIX COLUMN)

		if round == 13:
			block = []
			for i in range(0,4):
				block.append(first_row[i])
				block.append(second_row[i])
				block.append(third_row[i])
				block.append(fourth_row[i]) 

		else:
			block = []
			temp_list = []		
	

			for i in range(0,4):
	
				element_1 = gal_mul(first_row[i],2)  ^ gal_mul(second_row[i],3)	 ^ gal_mul(third_row[i],1) ^ gal_mul(fourth_row[i],1)	
				block.append(element_1)

				element_2 = gal_mul(first_row[i],1)  ^ gal_mul(second_row[i],2)  ^ gal_mul(third_row[i],3) ^ gal_mul(fourth_row[i],1) 
				block.append(element_2)

				element_3 = gal_mul(first_row[i],1)  ^ gal_mul(second_row[i],1)  ^ gal_mul(third_row[i],2) ^ gal_mul(fourth_row[i],3) 
				block.append(element_3)

				element_4 = gal_mul(first_row[i],3)  ^ gal_mul(second_row[i],1)  ^ gal_mul(third_row[i],1) ^ gal_mul(fourth_row[i],2) 
				block.append(element_4)


##Add Round Key
	        for add_round_key in range(0,16):

        	        temp_xor_variable = block[add_round_key] ^ key_bits[xor_plaintext_key]
                	temp_list.append(temp_xor_variable)


		block = []
		block = temp_list
		print block
		key_counter = key_counter + 16
		key_upto = key_upto + 16

	#print temp_xor
    	# START HERE
    	return block

def gal_mul(list_element, b):

	counter = 0
	product = 0
	
	while counter < 8:
		if (b & 1) == 1:
			product ^= list_element
		
		hi_bit = (list_element & 0x80)
		list_element <<= 1
		
		if hi_bit == 0x80:
			list_element ^= 0x1b
			
		b >>= 1
		counter += 1	

	return product % 256
		
# aesDecrypt - decrypt a single block of ciphertext
def aesDecrypt(ciphertext, key):
    block = copy(ciphertext)
    # START HERE
    return block

# return 16-byte block from an open file
# pad to 16 bytes with null chars if needed
def getBlock(fp):
    raw = fp.read(16)
    # reached end of file
    if len(raw) == 0:
        return ""
    # container for list of bytes
    block = []
    for c in list(raw):
        block.append(ord(c))
    # if the block is less than 16 bytes, pad the block
    # with the string representing the number of missing bytes
    if len(block) < 16:
        padChar = 16-len(block)
        while len(block) < 16:
            block.append(padChar)
    return block

# encrypt - wrapper function to allow encryption of arbitray length
# plaintext using Output Feedback (OFB) mode


def schedule_core(input_byte, i):
	sbox_output = []
	rcon_output = []
	a=0	
	first_element = input_byte[0]
	input_byte.pop(0)
	input_byte.append(first_element)

	for byte_sbox in input_byte:
		sbox_output.insert(a,sbox[int(byte_sbox)])
		a += 1
	left_most = sbox_output[0]
	rcon_value = rcon[i]

	output = left_most ^ rcon_value

	sbox_output.pop(0)
	sbox_output.insert(0,output)

	return sbox_output


def keyexpansion(aesKey):

	#aesKey = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]	
	#aesKey = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1E,0x1F]
	expanded_key = []
	counter = 0
	i = 1
	temp = []
	for byte in aesKey:
		expanded_key.append(byte)
	
	for expansion in range(0,7):

		temp = []
               	counter = 0
		#print expanded_key
	        length_ = len(expanded_key)
        	index_position = int(length_) - 4
		
		#for element in range(0,4):
		temp = expanded_key[index_position:]
		
		schedule_core_output = schedule_core(temp,i)
		temp = []
		temp = schedule_core_output
		i += 1
		#print i	
		position = length_ + 1
		xor_position = position - 32		

		for increment_position in range(xor_position - 1,xor_position + 3):
			
			XOR_Value = expanded_key[increment_position] ^ temp[counter]
			#print XOR_Value
			expanded_key.insert(position,XOR_Value)
			position += 1
			counter  += 1

#		if i == 2:
#			print length_
#			print temp
#			print expanded_key
#			sys.exit()
		#print expanded_key
		#sys.exit()
##########################################################################################################

# For Next 12 bytes
		for element in range(0,3):
              
                	temp = []
                	counter = 0

                	length_ = len(expanded_key)
                	index_position = int(length_) - 4

			#for element in range(0,4):
                        temp = expanded_key[index_position:]
				
	                position = length_ + 1
        	        xor_position = position - 32

                	for increment_position in range(xor_position - 1,xor_position + 3):
	
        	                XOR_Value = expanded_key[increment_position] ^ temp[counter]
                	        #print XOR_Value
                        	expanded_key.insert(position,XOR_Value)
                        	position += 1
                        	counter  += 1

		#print expanded_key
		#sys.exit()
		if len(expanded_key) >= 240:
			hexdecimal_expanded_key = []
			for element in expanded_key:
				element = hex(element)
				#element = format(element,'x')
				hexdecimal_expanded_key.append(element)
			
			return expanded_key



##################################################################################################################
# Next 4 Bytes
               	temp = []
                counter = 0
	
		sbox_output = []
	
               	length_ = len(expanded_key)
                index_position = int(length_) - 4

                #for element in range(0,4):
                
		temp = expanded_key[index_position:]

	        for byte_sbox in temp:
        	        sbox_output.insert(counter,sbox[int(byte_sbox)])
			counter += 1

		position = length_ + 1
             	xor_position = position - 32
		counter = 0
               	for increment_position in range(xor_position - 1,xor_position + 3):

                	XOR_Value = expanded_key[increment_position] ^ sbox_output[counter]
                                #print XOR_Value
                    	expanded_key.insert(position,XOR_Value)
                  	position += 1
                      	counter  += 1

		

		#for element in sbox_output:
		#	expanded_key.append(element)
	
                
		#hexdecimal_expanded_key = []
                #for element in expanded_key:
               # 	element = hex(element)
                #                #element = format(element,'x')
                #        hexdecimal_expanded_key.append(element)

		#print hexdecimal_expanded_key
		#sys.exit()

###################################################################################################################
# For next 12 Bytes

                for element in range(0,3):

                        temp = []
                        counter = 0

                        length_ = len(expanded_key)
                        index_position = int(length_) - 4

                        for element in range(0,4):
                                temp = expanded_key[index_position:]

                        position = length_ + 1
                        xor_position = position - 32

                        for increment_position in range(xor_position - 1,xor_position + 3):

                                XOR_Value = expanded_key[increment_position] ^ temp[counter]
                                #print XOR_Value
                                expanded_key.insert(position,XOR_Value)
                                position += 1
                                counter  += 1

		#print expanded_key
		#sys.exit()

#######################################################################################################################

def encrypt(myInput, password, outputfile=None):
    block = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # plaintext
    ciphertext = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # ciphertext
    # Initialization Vector
    IV = []
    for i in range(16):
        IV.append(randint(0, 255))

    # convert password to AES 256-bit key
    aesKey = passwordToKey(password)
    #aesKey = keyexpansion(aesKey)
    
    # create handle for file to be encrypted
    try:
        fp = open(myInput, "rb")
    except:
        print "pyAES: unable to open input file -", myInput
        sys.exit()

    # create handle for encrypted output file
    if outputfile is not None:
        try:
            outfile = open(outputfile,"w")
        except:
            print "pyAES: unable to open output file -", outputfile
            sys.exit()
    else:
        filename = myInput+".aes"
        try:
            outfile = open(filename,"w")
        except:
            print "pyAES: unable to open output file -", filename
            sys.exit()

    # write IV to outfile
    for byte in IV:
        outfile.write(chr(byte))

    # get the file size (bytes) 
    # if the file size is a multiple of the block size, we'll need 
    # to add a block of padding at the end of the message
    fp.seek(0,2)
    filesize = fp.tell()
    # put the file pointer back at the beginning of the file
    fp.seek(0)

    # begin reading in blocks of input to encrypt
    firstRound = True
    block = getBlock(fp)
 
    while block != "":
        if firstRound:
            blockKey = aesEncrypt(IV, aesKey)
            firstRound = False
        else:
            blockKey = aesEncrypt(blockKey, aesKey)

        for i in range(16):
            ciphertext[i] = block[i] ^ blockKey[i]

	#ciphertext=aesEncrypt(block,aesKey)

        # write ciphertext to outfile
        for c in ciphertext:
            outfile.write(chr(c))

        # grab next block from input file
        block = getBlock(fp)
    # if the message ends on a block boundary, we need to add an
    # extra block of padding
    if filesize % 16 == 0:
        outfile.write(16*chr(16))
    # close file pointers
    fp.close()
    outfile.close()

# decrypt - wrapper function to allow decryption of arbitray length
# ciphertext using Output Feedback (OFB) mode
def decrypt(myInput, password, outputfile=None):
    block = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # ciphertext
    plaintext = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # plaintext container

    # convert password to AES 256-bit key
    aesKey = passwordToKey(password)
    #aesKey = keyexpansion(aesKey)

    
    # create handle for file to be encrypted
    try:
        fp = open(myInput, "rb")
    except:
        print "pyAES: unable to open input file -", myInput
        sys.exit()

    # create handle for file to be decrypted
    try:
        fp = open(myInput, "rb")
    except:
        print "pyAES: unable to open input file -", myInput
        sys.exit()

    # create handle for decrypted output file
    if outputfile is not None:
        try:
            outfile = open(outputfile,"w")
        except:
            print "pyAES: unable to open output file -", filename
            sys.exit()
    else:
        if myInput[-4:] == ".aes":
            filename = myInput[:-4]
            print "Using", filename, "for output file name."
        else:
            filename = raw_input("output file name: ")
        try:
            outfile = open(filename,"w")
        except:
            print "pyAES: unable to open output file -", filename
            sys.exit()

    # recover Initialization Vector, the first block in file
    IV = getBlock(fp)

    # get the file size (bytes) in order to handle the
    # padding at the end of the file
    fp.seek(0,2)
    filesize = fp.tell()
    # put the file pointer back at the first block of ciphertext
    fp.seek(16)

    # begin reading in blocks of input to decrypt
    firstRound = True
    block = getBlock(fp)
    while block != "":
        if firstRound:
            blockKey = aesEncrypt(IV, aesKey)
            firstRound = False
        else:
            blockKey = aesEncrypt(blockKey, aesKey)

        for i in range(16):
            plaintext[i] = block[i] ^ blockKey[i]

        # if we're in the last block of text -> throw out the
        # number of bytes represented by the last byte in the block
        if fp.tell() == filesize:
            plaintext = plaintext[0:-(plaintext[-1])]

        # write ciphertext to outfile
        for c in plaintext:
            outfile.write(chr(c))

        # grab next block from input file
        block = getBlock(fp)
    # close file pointers
    fp.close()
    outfile.close()

def printUsage():
    print "./pyAES.py [-e <input file> | -d <input file>] [(optional) -o <output file>]"
    print "You will be prompted for a password after you specify the encryption/decryption args.\n"
    sys.exit()

# gather command line arguments and validate input
def main():
    # containers for command line arguments
    inputfile = None
    outputfile = None

    for a in range(len(sys.argv)):
        if sys.argv[a] == "-e":
            try:
                inputfile = sys.argv[a+1]
            except:
                inputfile = raw_input("File to encrypt: ")
        elif sys.argv[a] == "-d":
            try:
                inputfile = sys.argv[a+1]
            except:
                inputfile = raw_input("File to decrypt: ")
        if sys.argv[a] == "-o":
            try:
                outputfile = sys.argv[a+1]
            except:
                pass
    # print help message
    if ("-h" in sys.argv) or ("--help" in sys.argv):
        printUsage()
    if inputfile is None:
        print "Error: please specify options for encryption or decryption."
        printUsage()
    # encrypt file per user instructions
    if "-e" in sys.argv:
        password = getpass.getpass("Password: ")
        print "Encrypting file:", inputfile
        if outputfile is not None:
            encrypt(inputfile, password, outputfile)
        else:
            encrypt(inputfile, password)
        print "Encryption complete."
    # decrypt file per user instructions
    elif "-d" in sys.argv:
        password = getpass.getpass("Password: ")
        print "Decrypting file:", inputfile
        if outputfile is not None:
            decrypt(inputfile, password, outputfile)
        else:
            decrypt(inputfile, password)
        print "Decryption complete."

if __name__ == "__main__":
    main()
