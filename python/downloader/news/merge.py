import shutil
import glob


def mergeLists(newspaper):
    outfilename = "../../data/news/"+newspaper+"/"+newspaper+"-8yr.csv"

    with open(outfilename, 'wb') as outfile:
        for filename in glob.glob('../../data/news/'+newspaper+'/lists/*'):
            if filename == outfilename:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)


if __name__ == '__main__':
    mergeLists('eight')
