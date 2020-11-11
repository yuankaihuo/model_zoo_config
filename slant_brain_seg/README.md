# SLANT Brain Segmentation - MLCommons-Box

MLCommons-Box derived from [SLANT: Deep Whole Brain High Resolution Segmentation](https://github.com/MASILab/SLANTbrainSeg).

Please refer to the above link for the original work.

## Quick Start

This quick-start guide shows how to run this MLCommons-Box with default configs in a Docker environment.

### Get the Runner

Install the `mlcommons-box-docker` package in your python environment. This is a "runner" that can help you run the "boxes" in Docker.

```sh
pip3 install mlcommons-box-docker
```

### Get the Box

This directory is the root of "the box".

```sh
clone the example
cd box_examples/slant_brain_seg
```

### Run the Tasks

Call the runner with the default platform and task configs included with this box. Issue one "run" for each task.

```sh
mlcommons_box_docker run \
  --mlbox=. \
  --platform=./config_dir/docker.yaml \
  --task=./run/download.yaml

mlcommons_box_docker run \
  --mlbox=. \
  --platform=./config_dir/docker.yaml \
  --task=./run/pre_process.yaml

mlcommons_box_docker run \
  --mlbox=. \
  --platform=./config_dir/docker.yaml \
  --task=./run/run_test.yaml

mlcommons_box_docker run \
  --mlbox=. \
  --platform=./config_dir/docker.yaml \
  --task=./run/post_process.yaml

mlcommons_box_docker run \
  --mlbox=. \
  --platform=./config_dir/docker.yaml \
  --task=./run/gen_results.yaml
```
