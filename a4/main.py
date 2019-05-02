# Image compression
#
# You'll need Python 2.7 and must install these packages:
#
#   scipy, numpy
#
# You can run this *only* on PNM images, which the netpbm library is used for.
#
# You can also display a PNM image using the netpbm library as, for example:
#
#   python netpbm.py images/cortex.pnm


import sys, os, math, time, netpbm
import numpy as np
import struct


# Text at the beginning of the compressed file, to identify it


headerText = 'my compressed image - v1.0'



# Compress an image


def compress( inputFile, outputFile ):

  # Read the input file into a numpy array of 8-bit values
  #
  # The img.shape is a 3-type with rows,columns,channels, where
  # channels is the number of component in each pixel.  The img.dtype
  # is 'uint8', meaning that each component is an 8-bit unsigned
  # integer.

  img = netpbm.imread( inputFile ).astype('uint8')
  
  # Compress the image
  #
  # REPLACE THIS WITH YOUR OWN CODE TO FILL THE 'outputBytes' ARRAY
  # Note that single-channel images will have ahape' with only two
  # components: the y dimensions and the x dimension.  So you will
  # have to detect this and set the number of channels accordingly.
  # Furthermore, single-channel images must be indexed as img[y,x]
  # instead of img[y,x,1].  You'll need two pieces of similar code:
  # one piece for the single-channel case and one piece for the
  # multi-channel case.

  startTime = time.time()   
  outputBytes = bytearray()


  #Declorations 
  dictionary = {struct.pack('h', x): x+255 for x in range(-255, 256)} #creating dictionary
  currentList = ""
  newList = ""
  dictSize = len(dictionary)



  if (len(img.shape) == 2): #for single channel images 
    for y in range(img.shape[0]):
      for x in range(img.shape[1]):
   
        currentVal = img[y,x] #value of current pixel 
        lastVal = img[y,x-1] #value of last pixel (predicted value)
        errorVal = str(int(currentVal) - int(lastVal)) #error in predicted value
        errorVal = struct.pack('h', int(errorVal)) #storing error in string
        newList = currentList + errorVal #add error value to current list of pixels

        if (newList in dictionary): #if newList is in dictionary
          currentList = newList #newList becomes currentList
        
        else: 
          if (currentList != ""): #if current list is not empty
            if (dictSize < 65536): #if dictionary is not full
              dictionary[newList] = dictSize # add new list to dictionary
              dictSize +=1 #increment dictSize
            #add two byte of currentList to outputBytes  
            outputBytes.append(currentList[0]) 
            outputBytes.append(currentList[1])
            
          currentList = errorVal #sets currentList to errorVal because currentList has now been added to dictionary


  else: #for multi channel images
    for y in range(img.shape[0]):
      for x in range(img.shape[1]):
      #for y in range(img.shape[0]):
        for c in range(img.shape[2]):      

          currentVal = img[y,x,c] #value of current pixel 
          lastVal = img[y,x-1,c] #value of last pixel (predicted value)
          errorVal = str(int(currentVal) - int(lastVal)) #error in predicted value
          errorVal = struct.pack('h', int(errorVal)) #storing error in string
          newList = currentList + errorVal #add error value to current list of pixels

          if (newList in dictionary): #if newList is in dictionary
            currentList = newList #newList becomes currentList
        
          else: 
            if (currentList != ""):
              if (dictSize < 65536): #if dictionary is not full
                dictionary[newList] = dictSize 
                dictSize +=1 
              outputBytes.append(currentList[0])
              outputBytes.append(currentList[1])
            
            currentList = errorVal #sets currentList to errorVal 

  
  
  endTime = time.time()

  # Output the bytes
  #
  # Include the 'headerText' to identify the type of file.  Include
  # the rows, columns, channels so that the image shape can be
  # reconstructed.
  if (len(img.shape) == 2):
    outputFile.write( '%s\n'       % headerText )
    outputFile.write( '%d %d\n' % (img.shape[0], img.shape[1]) )
    outputFile.write( outputBytes )
    inSize  = img.shape[0] * img.shape[1]
    outSize = len(outputBytes)

  else:
    outputFile.write( '%s\n'       % headerText )
    outputFile.write( '%d %d %d\n' % (img.shape[0], img.shape[1], img.shape[2]) )
    outputFile.write( outputBytes )
    inSize  = img.shape[0] * img.shape[1] * img.shape[2]
    outSize = len(outputBytes)

  # Print information about the compression
  

  sys.stderr.write( 'Input size:         %d bytes\n' % inSize )
  sys.stderr.write( 'Output size:        %d bytes\n' % outSize )
  sys.stderr.write( 'Compression factor: %.2f\n' % (inSize/float(outSize)) )
  sys.stderr.write( 'Compression time:   %.2f seconds\n' % (endTime - startTime) )
  
# Uncompress an image

def uncompress( inputFile, outputFile ):

  # Check that it's a known file

  if inputFile.readline() != headerText + '\n':
    sys.stderr.write( "Input is not in the '%s' format.\n" % headerText )
    sys.exit(1)
    
  # Read the rows, columns, and channels.  

  rows, columns, channels = [ int(x) for x in inputFile.readline().split() ]

  # Read the raw bytes.

  inputBytes = bytearray(inputFile.read())

  # Build the image
  #
  # REPLACE THIS WITH YOUR OWN CODE TO CONVERT THE 'inputBytes' ARRAY INTO AN IMAGE IN 'img'.

  startTime = time.time()

  img = np.empty( [rows,columns,channels], dtype=np.uint8 )

  byteIter = iter(inputBytes)

  dictionary = {x+255:struct.pack('h', x) for x in range(-255, 256)} #Set up dictionary
  dictSize = len(dictionary)

  list1 = []
  
  dictLookUP = dictionary[next(byteIter)] #dictionary lookup 
  dictLookUP = struct.unpack('h',dictionary[next(byteIter)])[0] #unpacking
  list1.append(dictLookUP) #append to list1
  dictLookUP = struct.pack('h', dictLookUP) #pack up again
  
  for i in byteIter:
    if i in dictionary:
      lookUp = dictionary[next(byteIter)] #loop up
      dictionary[dictSize] = dictLookUP + (dictionary[next(byteIter)][0:2]) #unpack
      dictLookUP = lookUp
      lookUp = struct.unpack('h',dictionary[next(byteIter)])[0]
      list1.append(lookUp)
    elif i == dictSize:
      lookUp = dictLookUP + (dictionary[byteIter][0:2])

      dictSize += 1
          

      #byteIter[i] = entry
      #dictionary[dictSize] = dictLookUP + entry[0]
      #dictSize += 1
      
  
  i =0
  for y in range(rows):
    for x in range(columns):
      for c in range(channels):
        #code would go here to deal with the fact that
        #pixels are still in the predicted state not there true values
  
        img[y,x,c] = list1[1]
        i +=1
  print len(list1)
  endTime = time.time()

  # Output the image

  netpbm.imsave( outputFile, img )

  sys.stderr.write( 'Uncompression time: %.2f seconds\n' % (endTime - startTime) )

  

  
# The command line is 
#
#   main.py {flag} {input image filename} {output image filename}
#
# where {flag} is one of 'c' or 'u' for compress or uncompress and
# either filename can be '-' for standard input or standard output.


if len(sys.argv) < 4:
  sys.stderr.write( 'Usage: main.py c|u {input image filename} {output image filename}\n' )
  sys.exit(1)

# Get input file
 
if sys.argv[2] == '-':
  inputFile = sys.stdin
else:
  try:
    inputFile = open( sys.argv[2], 'rb' )
  except:
    sys.stderr.write( "Could not open input file '%s'.\n" % sys.argv[2] )
    sys.exit(1)

# Get output file

if sys.argv[3] == '-':
  outputFile = sys.stdout
else:
  try:
    outputFile = open( sys.argv[3], 'wb' )
  except:
    sys.stderr.write( "Could not open output file '%s'.\n" % sys.argv[3] )
    sys.exit(1)

# Run the algorithm

if sys.argv[1] == 'c':
  compress( inputFile, outputFile )
elif sys.argv[1] == 'u':
  uncompress( inputFile, outputFile )
else:
  sys.stderr.write( 'Usage: main.py c|u {input image filename} {output image filename}\n' )
  sys.exit(1)
