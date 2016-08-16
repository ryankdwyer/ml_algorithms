import utils
import sys

if __name__ == "__main__":
    dirPath = sys.argv[1]
    label = sys.argv[2]
    outputFile = sys.argv[3]

    utils.concatFilesInDir(dirPath, label, outputFile)
