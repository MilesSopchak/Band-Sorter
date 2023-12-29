"""
CSAPX Lab 3: Battle of the Bands
Given a list of bands and the number of votes they recived, find the most mediocre band (i.e. the band with the median amount of votes).

$ python3 bands.py [slow|fast] input-file

Author: Miles Sopchak
"""

from dataclasses import dataclass
import sys  # argv
import time  # clock
import random  # random

from typing import List  # List

@dataclass
class Band:
   """
   bandName (str): Name of the Band.
   votes (int): Total number of votes the band recived.
   """
   bandName: str
   votes: int

def readBandFile(filename: str) -> list[Band]:
    """
    Read bands from a file into a list of Band dataclass objects.
    :param filename: The name of the file.
    :return: A list of Band
    """
    bands = list()
    with open(filename, encoding="utf-8" ) as f:
        for line in f:
            fields = line.split('\t')
            bands.append(Band(
               bandName = fields[0],
               votes = int(fields[1])
            ))
    return bands

def _split(bands: list[Band], pivot: int) \
   -> tuple[list[Band], list[Band], list[Band]]:
   """
       Splits a list of Band dataclass objects into 3 lists based on a pivot.
       One list of everything less than the pivot,
       one list of elements equal to the pivot,
       and one list of elements greater than the pivot
       :param bands: a list of Band dataclass objects to split
       :param pivot: a Band dataclass object to split the list bands by
       :return: three lists of bands, one less than, one equal to, and one greater than the pivot
   """
   less, equal, greater = [], [], []
   for b in bands:
      if b.votes < pivot.votes:
         less.append(b)
      elif b.votes > pivot.votes:
         greater.append(b)
      else:
         equal.append(b)
   return less, equal, greater

def quickSort(bands: list[Band]) -> list[Band]:
   """
   Sorts a list of Band dataclass objects by their votes
   :param bands: list of Band dataclass objects to sort
   :return: a sorted list of Band dataclass objects
   """
   if len(bands) == 0:
      return []
   else:
      pivot = bands[0]
      less, equal, greater = _split(bands, pivot)
      return quickSort(less) + equal + quickSort(greater)

def quickSelect(bands: list[Band]) -> Band:
   """
   Finds the Band dataclass object that if bands were sorted, would be in the middle
   :param bands: a list of Band dataclass objects to find the center of
   :return: The Band dataclass object at the center of bands if it were sorted
   """
   k = len(bands)//2
   if (k == 0):
      return None
   else:
      pivot = bands[0]
      less, equal, greater = _split(bands, pivot)
      while True:
         if (k < len(less)):
            pivot = less[0]
            less, equal, greater = _split(less, pivot)
         elif (k >= len(less) + len(equal)):
            k = k - len(less) - len(equal)
            pivot = greater[0]
            less, equal, greater = _split(greater, pivot)
         else:
            return equal[k - len(less)]

def main() -> None:
   """
   The main function.
   :return: None
   """
   bands = readBandFile(str(sys.argv[2]))
   print("Search type: " + str(sys.argv[1]))
   print("Number of bands: " + str(len(bands)))
   if (str(sys.argv[1]) == "slow"):
      start = time.perf_counter()
      mband = str(quickSort(bands)[len(bands)//2])
      runtime = time.perf_counter() - start
   else:
      start = time.perf_counter()
      mband = str(quickSelect(bands))
      runtime = time.perf_counter() - start
   print("Elapsed time: " + str(runtime) + " seconds")
   print('Most Mediocre Band: ' + str(mband))
   

if __name__ == '__main__':
   main()
