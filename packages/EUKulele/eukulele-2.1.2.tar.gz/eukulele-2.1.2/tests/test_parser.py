import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--level-hierarchy',nargs="+")

args = parser.parse_args()
print(type(args.level_hierarchy))

