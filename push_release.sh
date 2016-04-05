#! /bin/bash
VERSION=`python setup.py --version | sed 's/\([0-9]*\.[0-9]*\.[0-9]*\).*$$/\1/'`

read -p "This will tag a release as '$VERSION' Continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Done!"
  git tag -a $VERSION -m "Version $VERSION"
  git push --tags
fi