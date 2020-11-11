import argparse
from distutils import dir_util
import enum
import logging
import logging.config
import os
import time

logger = logging.getLogger(__name__)


class Task(str, enum.Enum):
    download = 'download'
    pre_process = 'pre_process'
    run_test = 'run_test'
    post_process = 'post_process'
    gen_results = 'gen_results'


def download(task_args):
    logger.info("Starting task: '{}'".format(Task.download))
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '--input-dir', type=str, default=None, help="Input directory.")
    parser.add_argument('--output_dir', '--output-dir', type=str, default=None, help="Output directory.")
    args = parser.parse_args(args=task_args)
    input_dir = args.input_dir
    output_dir = args.output_dir
    os.system("wget -O {}/test_volume.nii.gz --no-check-certificate https://www.nitrc.org/frs/download.php/10666/test_volume.nii.gz".format(input_dir))



def pre_process(task_args):
    logger.info("Starting task: '{}'".format(Task.pre_process))
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '--input-dir', type=str, default=None, help="Input directory.")
    parser.add_argument('--output_dir', '--output-dir', type=str, default=None, help="Output directory.")
    args = parser.parse_args(args=task_args)
    input_dir = args.input_dir
    output_dir = args.output_dir
    dir_util.copy_tree(input_dir, "/INPUTS")
    start = time.time()
    os.system("/extra/run_Deep_brain_preprocessing")
    end = time.time()
    logger.info("*******preprocessing time: {:.6f} seconds".format(end - start))
    dir_util.copy_tree("/OUTPUTS", output_dir)


def run_test(task_args):
    logger.info("Starting task: '{}'".format(Task.run_test))
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '--input-dir', type=str, default=None, help="Input directory.")
    parser.add_argument('--output_dir', '--output-dir', type=str, default=None, help="Output directory.")
    args = parser.parse_args(args=task_args)
    input_dir = args.input_dir
    output_dir = args.output_dir
    dir_util.copy_tree(input_dir, "/INPUTS")
    dir_util.copy_tree(output_dir, "/OUTPUTS")
    start = time.time()
    os.system("bash {}/run_all_batches.sh".format(output_dir))
    end = time.time()
    logger.info("*******segmentation time: {:.6f} seconds".format(end - start))
    dir_util.copy_tree("/OUTPUTS", output_dir)


def post_process(task_args):
    logger.info("Starting task: '{}'".format(Task.post_process))
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '--input-dir', type=str, default=None, help="Input directory.")
    parser.add_argument('--output_dir', '--output-dir', type=str, default=None, help="Output directory.")
    args = parser.parse_args(args=task_args)
    input_dir = args.input_dir
    output_dir = args.output_dir
    dir_util.copy_tree(input_dir, "/INPUTS")
    dir_util.copy_tree(output_dir, "/OUTPUTS")
    start = time.time()
    os.system("/extra/run_Deep_brain_postprocessing")
    end = time.time()
    logger.info("*******postprocessing time: {:.6f} seconds".format(end - start))
    dir_util.copy_tree("/OUTPUTS", output_dir)


def gen_results(task_args):
    logger.info("Starting task: '{}'".format(Task.gen_results))
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '--input-dir', type=str, default=None, help="Input directory.")
    parser.add_argument('--output_dir', '--output-dir', type=str, default=None, help="Output directory.")
    args = parser.parse_args(args=task_args)
    input_dir = args.input_dir
    output_dir = args.output_dir
    dir_util.copy_tree(input_dir, "/INPUTS")
    dir_util.copy_tree(output_dir, "/OUTPUTS")
    os.system("/extra/generate_light_PDF")
    os.system("/extra/generate_volume_stat")
    dir_util.copy_tree("/OUTPUTS", output_dir)


def main():
    """SLANT main function"""
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('mlbox_task', type=str, help="Task to run.")
        parser.add_argument('--log_dir', '--log-dir', type=str, required=True, help="Logging directory.")
        box_args, task_args = parser.parse_known_args()

        logger_config = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "standard": {"format": "%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s"},
            },
            "handlers": {
                "file_handler": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "standard",
                    "filename": os.path.join(box_args.log_dir, "mlbox_slant_brain_seg_{}.log".format(box_args.mlbox_task))
                }
            },
            "loggers": {
                "": {"level": "INFO", "handlers": ["file_handler"]},
                "__main__": {"level": "INFO", "propagate": "yes", "handlers": ["file_handler"]}
            }
        }
        logging.config.dictConfig(logger_config)

        if box_args.mlbox_task == Task.download:
            download(task_args)
        elif box_args.mlbox_task == Task.pre_process:
            pre_process(task_args)
        elif box_args.mlbox_task == Task.run_test:
            run_test(task_args)
        elif box_args.mlbox_task == Task.post_process:
            post_process(task_args)
        elif box_args.mlbox_task == Task.gen_results:
            gen_results(task_args)
        else:
            raise ValueError("Unknown task: {}".format(box_args.mlbox_task))
    except Exception as err:
        logger.exception(err)

if __name__ == "__main__":
    main()