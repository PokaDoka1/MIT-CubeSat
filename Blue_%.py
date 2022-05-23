# Imports
import cv2
import numpy as np

# Read image
img = cv2.imread("C:\\Users\\PokaDoka\\Pictures\\leaves\\both.jpg")

# Here, you define your target color as
# a tuple of three values: RGB

green = [111,33,164]

dog = []

# You define an interval that covers the values
# in the tuple and are below and above them by 20
diff = 100

for color in green:
    if diff + color > 255:
         dog.append(255)
    else:
        dog.append(diff + color)

print(dog)

# Be aware that opencv loads image in BGR format,
# that's why the color values have been adjusted here:
boundaries = [([green[2], green[1], green[0]], [dog[2],dog[1], dog[0]])]

# Scale your BIG image into a small one:
scalePercent = 0.3

# Calculate the new dimensions
width = int(img.shape[1] * scalePercent)
height = int(img.shape[0] * scalePercent)
newSize = (width, height)

# Resize the image:
img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)

# for each range in your boundary list:
for (lower, upper) in boundaries:

    # You get the lower and upper part of the interval:
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)

    # cv2.inRange is used to binarize (i.e., render in white/black) an image
    # All the pixels that fall inside your interval [lower, uipper] will be white
    # All the pixels that do not fall inside this interval will
    # be rendered in black, for all three channels:
    mask = cv2.inRange(img, lower, upper)

    # Now, you AND the mask and the input image
    # All the pixels that are white in the mask will
    # survive the AND operation, all the black pixels
    # will remain black
    output = cv2.bitwise_and(img, img, mask=mask)

    # You can use the mask to count the number of white pixels.
    # Remember that the white pixels in the mask are those that
    # fall in your defined range, that is, every white pixel corresponds
    # to a green pixel. Divide by the image size and you got the
    # percentage of green pixels in the original image:
    ratio_green = cv2.countNonZero(mask)/(img.size/3)
    print(f"ratio green: {ratio_green}")

    # This is the color percent calculation, considering the resize I did earlier.
    colorPercent = (ratio_green * 100)

    # Print the color percent, use 2 figures past the decimal point

    print('blue pixel percentage:', np.round(colorPercent, 2))

    if colorPercent > 99:
        print(f"Water most likely detected with {colorPercent:.2f}% ")
    else:
        print(f"plastic detected with {100 - colorPercent:.2f}%")
