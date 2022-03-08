from PIL import Image 
from IPython.display import display 
import random
import json

#square = ["Blue", "Green", "Orange", "Red", "Yellow", "House"] 
#squareWeights = [0, 0, 0, 0, 0, 100]
# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Blue", "Orange", "Purple", "Red", "Yellow"] 
backroundWeights = [30, 40, 15, 5, 10]

circle = ["Blue", "Green", "Orange", "Red", "Yellow"] 
circleWeights = [30, 40, 15, 5, 10]

square = ["Blue", "Green", "Orange", "Red", "Paint"] 
squareWeights = [5, 0, 0, 5, 90]

# Dictionary variable for each trait. 
# Eech trait corresponds to its file name

backgroundFiles = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
}

circleFiles = {
    "Blue": "blue-circle",
    "Green": "green-circle",
    "Orange": "orange-circle",
    "Red": "red-circle",
    "Yellow": "yellow-circle"   
}

squareFiles = {
    "Blue": "blue-square",
    "Green": "green-square",
    "Orange": "orange-square",
    "Red": "red-square",
    #"Yellow": "yellow-square", 
    "Paint": "paint-square", 
          
}

## Generate Traits

TOTAL_IMAGES = 30 # Number of random unique images we want to generate

allImages = [] 

# A recursive function to generate unique image combinations
def createNewImage():
    
    newImage = {} #

    # For each trait category, select a random trait based on the weightings 
    newImage ["Background"] = random.choices(background, backroundWeights)[0]
    newImage ["Circle"] = random.choices(circle, circleWeights)[0]
    newImage ["Square"] = random.choices(square, squareWeights)[0]
    
    if newImage in allImages:
        return createNewImage()
    else:
        return newImage
    
    
# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 
    
    newTraitImage = createNewImage()
    
    allImages.append(newTraitImage)
    

# Returns true if all images are unique
def allImagesUnique(allImages):
    seen = list()
    return not any(i in seen or seen.append(i) for i in allImages)

print("Are all images unique?", allImagesUnique(allImages))

# Add token Id to each image
i = 0
for item in allImages:
    item["tokenId"] = i
    i = i + 1

print(allImages)

# Get Trait Counts

background_count = {}
for item in background:
    background_count[item] = 0
    
circle_count = {}
for item in circle:
    circle_count[item] = 0

square_count = {}
for item in square:
    square_count[item] = 0

for image in allImages:
    background_count[image["Background"]] += 1
    circle_count[image["Circle"]] += 1
    square_count[image["Square"]] += 1
    
print(background_count)
print(circle_count)
print(square_count)

#### Generate Metadata for all Traits 
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(allImages, outfile, indent=4)

#### Generate Images    
for item in allImages:

    im1 = Image.open(f'./trait-layers/backgrounds/{backgroundFiles[item["Background"]]}.jpg').convert('RGBA')
    im2 = Image.open(f'./trait-layers/circles/{circleFiles[item["Circle"]]}.png').convert('RGBA')
    im3 = Image.open(f'./trait-layers/squares/{squareFiles[item["Square"]]}.png').convert('RGBA')

    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)

    #Convert to RGB
    rgb_im = com2.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + "test.png")

#### Generate Metadata for each Image    

f = open('./metadata/all-traits.json',) 
data = json.load(f)


createNewImage()
allImagesUnique(allImages)