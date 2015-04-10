#!/usr/bin/python

# A non-destructive utility to help you sort new batches of photos into your
# organizational structure (whatever that may be).
#
# For each file in the input directory, checks if the file exists in the main
# image directory. If it does (anywhere in the file structure), does nothing;
# if it's a new image, it will be copied into a TODO folder in your main image
# directory. You can then sort the images into folders manually.

import sys
import os
import hashlib
import shutil
import pickle

if (len(sys.argv) != 3):
    print 'Usage: ' + sys.argv[0] + ' <new_image_directory> <main_image_directory>'
    exit(1)

inputDirectory = sys.argv[1]
outputDirectory = sys.argv[2]

todoDirectory = os.path.join(outputDirectory, 'TODO')
if os.path.exists(todoDirectory):
    print 'Exiting: this script needs to use ' + todoDirectory + ', but it already exists.'
    exit(1)

os.makedirs(todoDirectory)

# Hash files we already have
fileHashes = {}

# If we already hashed the existing files, load from the hash
savedHashFilename = os.path.join(outputDirectory, '.photosort')
if os.path.exists(savedHashFilename):
    with open(savedHashFilename, 'rb') as savedFile:
        fileHashes = pickle.load(savedFile)

# Hash new files
for root, dirs, files in os.walk(outputDirectory):
    for filename in files:
        if filename.startswith('.'):
            continue
        fullName = os.path.join(root, filename)
        if fullName not in fileHashes.values():
            fileHashes[hashlib.md5(open(fullName).read()).hexdigest()] = fullName

# Save our hash so we don't have to do it again
with open(savedHashFilename, 'wb') as savedFile:
    pickle.dump(fileHashes, savedFile)

for root, dirs, files in os.walk(inputDirectory):
    for filename in files:
        if filename.startswith('.'):
            continue
        fullName = os.path.join(root, filename)
        fileHash = hashlib.md5(open(fullName).read()).hexdigest()
        if (fileHash in fileHashes):
            print fullName.ljust(50) + ' Already exists as ' + fileHashes[fileHash]
        else:
            print fullName.ljust(45) + ' NEW'
            shutil.copy2(fullName, os.path.join(todoDirectory, filename))
