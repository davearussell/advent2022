#! /bin/bash -eu

MYDIR=$(realpath $(dirname $0))

day=$(date +%d)
new_dir=${MYDIR}/day${day}
solve_py=${new_dir}/solve.py
url=https://adventofcode.com/$(date +%Y/day/%d)/input

mkdir -p ${new_dir}
cat > ${solve_py} <<EOF
#! /usr/bin/python3
import sys


def main(input_file):
    pass


if __name__ == '__main__':
    main(sys.argv[1])
EOF
chmod +x ${solve_py}

curl ${url} --cookie "session=${ADVENT_OF_CODE_SESSION}" > ${new_dir}/input.txt

git -C ${MYDIR} add ${new_dir}
git -C ${MYDIR} commit -m "day ${day} puzzle"
