# Image manipulation
#
# You'll need Python 2.7 and must install these packages:
#
#   numpy, PyOpenGL, Pillow
#
# Note that file loading and saving (with 'l' and 's') do not work on
# Mac OSX, so you will have to change 'imgFilename' below, instead, if
# you want to work with different images.
#
# Note that images, when loaded, are converted to the YCbCr
# colourspace, and that you should manipulate only the Y component of
# each pixel when doing intensity changes.


import sys, os, numpy, math

try: # Pillow
  from PIL import Image
except:
  print 'Error: Pillow has not been installed.'
  sys.exit(0)

try: # PyOpenGL
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print 'Error: PyOpenGL has not been installed.'
  sys.exit(0)



# Globals

windowWidth  = 600 # window dimensions
windowHeight =  800

localHistoRadius = 5  # distance within which to apply local histogram equalization



# Current image

imgDir      = 'images'
imgFilename = 'strawberries.png'

currentImage = Image.open( os.path.join( imgDir, imgFilename ) ).convert( 'YCbCr' ).transpose( Image.FLIP_TOP_BOTTOM )
tempImage    = None



# File dialog (doesn't work on Mac OSX)

if sys.platform != 'darwin':
  import Tkinter, tkFileDialog
  root = Tkinter.Tk()
  root.withdraw()



# Apply brightness and contrast to tempImage and store in
# currentImage.  The brightness and constrast changes are always made
# on tempImage, which stores the image when the left mouse button was
# first pressed, and are stored in currentImage, so that the user can
# see the changes immediately.  As long as left mouse button is held
# down, tempImage will not change.

def applyBrightnessAndContrast( brightness, contrast ):

  width  = currentImage.size[0]
  height = currentImage.size[1]

  srcPixels = tempImage.load()
  dstPixels = currentImage.load()

  # YOUR CODE HERE
  
  for x in range(0,currentImage.width):                     #for loop to run through all x values of image
    for y in range(0,currentImage.height):                  #for loop to run through all y values of image
      I, Cb, Cr = srcPixels[x,y]                            #creating three variables for each channel
      I = contrast*I + brightness                           #modifying Y channel to adjust brightness and contrast using formula in class notes
      dstPixels[x,y] = (I, Cb, Cr)                          #displaying modified pixel
      

  print 'adjust brightness = %f, contrast = %f' % (brightness,contrast)

  

# Perform local histogram equalization on the current image using the given radius.

def performHistoEqualization( radius ):

  pixels = currentImage.load()
  width  = currentImage.size[0]
  height = currentImage.size[1]

  # YOUR CODE HERE
  
  for x in range(1,currentImage.width-1):                   #for loop to run through all x values of image
    for y in range(1,currentImage.height-1):                #for loop to run through all y values of image
                                                            #excludes all border pixels as it is not possible to look up all neighbours for border pixels

#pixSeed represents the pixel that is going to be modified
#pix? represents the neighbouring pixel that will be used for when calculating local histogram
      pixSeed, b, c = pixels[x,y]                         
      pix1, b, c = pixels[x-1,y+1]
      pix2, b, c = pixels[x,y+1]
      pix3, b, c = pixels[x+1,y+1]
      pix4, b, c = pixels[x-1,y]
      pix5, b, c = pixels[x+1,y]
      pix6, b, c = pixels[x-1,y-1]
      pix7, b, c = pixels[x,y-1]
      pix8, b, c = pixels[x+1,y-1]
      
#setting pixSeed values to local histogram value
      pixSeed = (pix1 + pix2 + pix3 + pix4 + pix5 + pix6 + pix7 + pix8 +pixSeed)/9
#displaying new image
      pixels[x,y] = (pixSeed, b, c)

#for x in range(1,currentImage.width-1):
#    for y in range(1,currentImage.height-1):
#      if x == 0:
#        if y == 0:
#          pixSeed, b, c = pixels[x,y]
#          pix2, b, c = pixels[x,y+1]
#          pix3, b, c = pixels[x+1,y+1]
#          pix5, b, c = pixels[x+1,y]
#          pix1 = pix2
#	  pix4 = pixSeed
#	  pix6 = pixSeed
#	  pix7 = pixSeed
#	  pix8 = pix5
#	elif y == currentImage.height:
#          pixSeed, b, c = pixels[x,y]
#          pix5, b, c = pixels[x+1,y]
#          pix7, b, c = pixels[x,y-1]
#          pix8, b, c = pixels[x+1,y-1]
#          pix3 = pix5
#          pix1 = pixSeed
#          pix2 = pixSeed
#          pix4 = pixSeed
#          pix6 = pix7
#        else:
#          pixSeed, b, c = pixels[x,y]
#          pix1, b, c = pixels[x-1,y+1]
#          pix2, b, c = pixels[x,y+1]
#          pix3, b, c = pixels[x+1,y+1]
#          pix4, b, c = pixels[x-1,y]
#          pix5, b, c = pixels[x+1,y]
#          pix6 = pix4
#          pix7 = pixSeed
#          pix8 = pix5
#      if x == currentImage.width:
#        if y = 0:
#          pixSeed, b, c = pixels[x,y]
#          pix1, b, c = pixels[x-1,y+1]
#          pix2, b, c = pixels[x,y+1]
#          pix4, b, c = pixels[x-1,y]
#          pix6 = pix4
#          pix7 = pixSeed
#          pix8 = pixSeed
#          pix5 = pixSeed
#          pix3 = pix2
#        elif y== currentImage.height:
#          pixSeed, b, c = pixels[x,y]
#          pix4, b, c = pixels[x-1,y]
#          pix6, b, c = pixels[x-1,y-1]
#          pix7, b, c = pixels[x,y-1]
#          pix1 = pix4
#          pix2 = pixSeed
#          pix3 = pixSeed
#          pix5 = pixSeed
#          pix8 = pix7
#        else:
#          pixSeed, b, c = pixels[x,y]
#          pix1, b, c = pixels[x-1,y+1]
#          pix2, b, c = pixels[x,y+1]
#          pix4, b, c = pixels[x-1,y]
#          pix6, b, c = pixels[x-1,y-1]
#          pix7, b, c = pixels[x,y-1]
#          pix8 = pix 7
#          pix5 = pixSeed
#          pix3 = pix2
#      if y == 0:
#        if x > 0 and x < currentImage.width:
#          pixSeed, b, c = pixels[x,y]
#          pix1, b, c = pixels[x-1,y+1]
#          pix2, b, c = pixels[x,y+1]
#          pix3, b, c = pixels[x+1,y+1]
#          pix4, b, c = pixels[x-1,y]
#          pix5, b, c = pixels[x+1,y]
#          pix6 = pix4
#          pix7 = pixSeed
#          pic8 = pix5
#      if y == currentImage.height:
#        if x > 0 and x < currentImage.width:
#          pixSeed, b, c = pixels[x,y]
#          pix4, b, c = pixels[x-1,y]
#          pix5, b, c = pixels[x+1,y]
#          pix6, b, c = pixels[x-1,y-1]
#          pix7, b, c = pixels[x,y-1]
#          pix8, b, c = pixels[x+1,y-1]
#          pix1= pix4
#          pix2 = pixSeed
#          pix3 = pix5
#      if x > 0 and x < currentImage.width and y >0 and y < currentImage.height:
#        pixSeed, b, c = pixels[x,y]
#        pix1, b, c = pixels[x-1,y+1]
#        pix2, b, c = pixels[x,y+1]
#        pix3, b, c = pixels[x+1,y+1]
#        pix4, b, c = pixels[x-1,y]
#        pix5, b, c = pixels[x+1,y]
#        pix6, b, c = pixels[x-1,y-1]
#        pix7, b, c = pixels[x,y-1]
#        pix8, b, c = pixels[x+1,y-1]
#
#          
#      pixSeed, b, c = pixels[x,y]
#      pix1, b, c = pixels[x-1,y+1]
#      pix2, b, c = pixels[x,y+1]
#      pix3, b, c = pixels[x+1,y+1]
#      pix4, b, c = pixels[x-1,y]
#      pix5, b, c = pixels[x+1,y]
#      pix6, b, c = pixels[x-1,y-1]
#      pix7, b, c = pixels[x,y-1]
#      pix8, b, c = pixels[x+1,y-1]
#
#      pixSeed = pixSeed/9 
#      pix1 = pix1/9
#      pix2 = pix2/9
#      pix3 = pix3/9
#      pix4 = pix4/9
#      pix5 = pix5/9
#      pix6 = pix6/9
#      pix8 = pix8/9
#      pixels[x,y] = (pixSeed, b, c)
      
         


  
  print 'perform local histogram equalization with radius %d' % radius



# Scale the tempImage by the given factor and store it in
# currentImage.  Use backward projection.  This is called when the
# mouse is moved with the right button held down.

def scaleImage( factor ):

  width  = currentImage.size[0]
  height = currentImage.size[1]

  srcPixels = tempImage.load()
  dstPixels = currentImage.load()

  # YOUR CODE HERE
#  [orgWidth, orgHeight] = tempImage.size       # find inital size of image
#  width = (orgWidth*factor)                    #calculate new image width
#  height = (orgHeight*factor)                  #calculate new image height
#  currentImage = Image.new('YCbCr', (width,height))  #create new image of with new width and height

#  for x in range (width):                      #nested for loop to go through all pixels and set a value
#    for y in range (height):
      
  
    
  print 'scale image by %f' % factor

  

# Set up the display and draw the current image

def display():

  # Clear window

  glClearColor ( 1, 1, 1, 0 )
  glClear( GL_COLOR_BUFFER_BIT )

  # rebuild the image

  img = currentImage.convert( 'RGB' )

  width  = img.size[0]
  height = img.size[1]

  # Find where to position lower-left corner of image

  baseX = (windowWidth-width)/2
  baseY = (windowHeight-height)/2

  glWindowPos2i( baseX, baseY )

  # Get pixels and draw

  imageData = numpy.array( list( img.getdata() ), numpy.uint8 )

  glDrawPixels( width, height, GL_RGB, GL_UNSIGNED_BYTE, imageData )

  glutSwapBuffers()


  
# Handle keyboard input

def keyboard( key, x, y ):

  global localHistoRadius

  if key == '\033': # ESC = exit
    sys.exit(0)

  elif key == 'l':
    if sys.platform != 'darwin':
      path = tkFileDialog.askopenfilename( initialdir = imgDir )
      if path:
        loadImage( path )

  elif key == 's':
    if sys.platform != 'darwin':
      outputPath = tkFileDialog.asksaveasfilename( initialdir = '.' )
      if outputPath:
        saveImage( outputPath )

  elif key == 'h':
    performHistoEqualization( localHistoRadius )

  elif key in ['+','=']:
    localHistoRadius = localHistoRadius + 1
    print 'radius =', localHistoRadius

  elif key in ['-','_']:
    localHistoRadius = localHistoRadius - 1
    if localHistoRadius < 1:
      localHistoRadius = 1
    print 'radius =', localHistoRadius

  else:
    print 'key =', key    # DO NOT REMOVE THIS LINE.  It will be used during automated marking.

  glutPostRedisplay()



# Load and save images.
#
# Modify these to load to the current image and to save the current image.
#
# DO NOT CHANGE THE NAMES OR ARGUMENT LISTS OF THESE FUNCTIONS, as
# they will be used in automated marking.


def loadImage( path ):

  global currentImage

  currentImage = Image.open( path ).convert( 'YCbCr' ).transpose( Image.FLIP_TOP_BOTTOM )


def saveImage( path ):

  global currentImage

  currentImage.transpose( Image.FLIP_TOP_BOTTOM ).convert('RGB').save( path )
  


# Handle window reshape


def reshape( newWidth, newHeight ):

  global windowWidth, windowHeight

  windowWidth  = newWidth
  windowHeight = newHeight

  glutPostRedisplay()



# Mouse state on initial click

button = None
initX = 0
initY = 0



# Handle mouse click/release

def mouse( btn, state, x, y ):

  global button, initX, initY, tempImage

  if state == GLUT_DOWN:
    tempImage = currentImage.copy()
    button = btn
    initX = x
    initY = y
  elif state == GLUT_UP:
    tempImage = None
    button = None

  glutPostRedisplay()

  

# Handle mouse motion

def motion( x, y ):

  if button == GLUT_LEFT_BUTTON:

    diffX = x - initX
    diffY = y - initY

    applyBrightnessAndContrast( 255 * diffX/float(windowWidth), 1 + diffY/float(windowHeight) )

  elif button == GLUT_RIGHT_BUTTON:

    initPosX = initX - float(windowWidth)/2.0
    initPosY = initY - float(windowHeight)/2.0
    initDist = math.sqrt( initPosX*initPosX + initPosY*initPosY )
    if initDist == 0:
      initDist = 1

    newPosX = x - float(windowWidth)/2.0
    newPosY = y - float(windowHeight)/2.0
    newDist = math.sqrt( newPosX*newPosX + newPosY*newPosY )

    scaleImage( newDist / initDist )

  glutPostRedisplay()
  


# Run OpenGL

glutInit()
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
glutInitWindowSize( windowWidth, windowHeight )
glutInitWindowPosition( 50, 50 )

glutCreateWindow( 'imaging' )

glutDisplayFunc( display )
glutKeyboardFunc( keyboard )
glutReshapeFunc( reshape )
glutMouseFunc( mouse )
glutMotionFunc( motion )

glutMainLoop()
