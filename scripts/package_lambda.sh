#!/usr/bin/env bash
set -o errexit
# set -o pipefail
set -o nounset

func_dir=$1
func_name=`echo ${func_dir} | sed 's:.*/::'`
root_dir=`git rev-parse --show-toplevel`

poetry install --sync -C $func_dir --without dev
mkdir -p $root_dir/tmp/dist/lambda-package

venv_dir=`poetry env info --path -C $func_dir`
cp -R $venv_dir/lib/python*/site-packages/* $root_dir/tmp/dist/lambda-package/ 1>/dev/null
cp -R $func_dir/src $root_dir/tmp/dist/lambda-package/ 1>/dev/null

cd $root_dir/tmp/dist/lambda-package
zip -r $root_dir/tmp/dist/$func_name.zip .